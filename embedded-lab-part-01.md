# Introduction

This assignment is divided into two parts where you will evaluate and attack the security of an embedded device.

The assignment can be developed in a team of up to 4 members (exceptions must be approved). See the assignment submission dates in Moodle.

In your submission, describe the procedures you followed. Please explain noteworthy or unexpected observations. Don’t forget to address all the questions and targets in the assignment description. Provide details on how you arrived at the conclusions/results (do not just paste the result). **All submissions must**:

1. Be in a ZIP file with the following format: `<student_id_1>_<student_id_2>..<student_id_n>.zip`.
2. Include all of the code used and relevant additional documentation (in any form that makes sense for you).
3. Have a `README.md` file that links and describes all information and files delivered. It should describe the relevant compilation/invocation for the relevant code used to extract information and the answer to **ALL** questions asked in the assignment description. **It must also include the Arduino identification number.**
4. A `TARGETS` folder must be present with a `secrets.csv` file that has a single line containing the following comma-separated information:
 	1. Arduino ID;
	2. Dans' password;
	3. Alans' password;
	4. c&c password;
	5. Final secret;
	6. c&c password MD5 (the hash you recovered from the decrypted signature);
	7. PROGMEM firmware SHA-256.
6. All other target information must be present in the `TARGETS` folder, organized into a `target-<n>` sub-folder per target (see **Submission integrity & anti-fabrication** below).

## Discussion

The assignment includes an individual discussion during lab classes, where every group member must
demonstrate understanding of the work delivered. The rubric produces the **team** report grade;
each member's final mark for the assignment is that team grade multiplied by their own **discussion
factor**:

| Level | Factor | What it looks like |
| ----- | ------ | ------------------ |
| Independent mastery | 1.00 | Explains the work and the reasoning (the *why*), answers follow-up questions, and can re-derive a step live on your own board/tag. |
| Solid | 0.85 | Explains the work and most of the reasoning; minor gaps are closed with light prompting. |
| Partial | 0.70 | Describes *what* was done but is shallow on *why*; needs significant prompting. |
| Superficial | 0.50 | Recites the report but cannot answer data-bound or "why" questions. |
| None | 0.00 | Absent without justification, silent, or clearly did not do or understand the work. |

Notes:

- The factor is individual, so members of the same team can receive different final marks.
- Questions are drawn from across all targets, not only the parts you personally wrote, so be ready to explain any of them.
- Expect questions bound to your own board/tag (the "Answer this" prompts in each target) and possibly a request to reproduce a step live.
- Because the assignment requires at least 9.5/20, a low discussion factor can drop a member below the pass threshold for that assignment.


## Submission integrity & anti-fabrication

Each Arduino you were assigned carries its **own** unique passwords, keys and secrets. Your report must therefore be backed by evidence produced *from your own board*, not by a plausible-sounding narrative. Three rules apply to every target:

1. **Raw data before conclusions.** Any plot or graph you present must be accompanied by the raw data file it was drawn from **and** the script that turns that data into the plot. Running the script on the data must reproduce the figure. A plot without reproducible source data scores **0** for that target's artifact.
2. **Per-target proof-of-work artifact.** Each target below requires the listed artifact, placed under `TARGETS/target-<n>/`, plus a short answer to the target's data-bound question. **A target whose artifact is missing, fabricated, or fails verification against your assigned board scores 0 for that target, regardless of how well the narrative is written.**
3. **AI-use disclosure (allowed, but you must disclose).** You may use AI assistants as a learning and debugging aid. You **must** include a `TARGETS/AI-DISCLOSURE.md` file stating which tools you used and for what. The artifacts and their derivation must be your team's own work on your own device. Undisclosed or misrepresented AI use is an academic-integrity violation.

The required proof-of-work artifact and the data-bound question are stated with each target in its description below (look for the **Required artifact** and **Answer this** notes).


> **AI-usage disclosure (this document).** Parts of this assignment description, including the per-target anti-fabrication scaffolding and some wording, were drafted and reviewed with the help of AI assistants. All content was reviewed and validated by the teaching team, who remain responsible for it.


## Criteria

The assignment will be graded using the following rubric. Please use this detailed rubric as guidance to create a good, detailed report. If the assignment is deemed unacceptable in a given criterion, a 0 will be given to that respective criterion.

Instructors will only help you with general hints and procedures to carry on your analysis. **At any point during the assignment, you can ask the instructor for hints specific to the solution. These requests must be performed by email, and will be considered during grading.**

| **Criteria**                   | **weight**       | **Exemplary**  **(100%)**                                    | **Accomplished**  **(75%)**                                  | **Satisfactory**   **(50%)**                                 | **Poor**  **(25%)**                                          |
| ------------------------------ | ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Organization and  Language** | 10%              | Good organization, easy  to follow and relate to the assignment activities.  No major language  (Grammar, Usage, Mechanics, Spelling) errors. | Organized, but points  are somewhat jumpy or hard to follow.  Only one or two important  language errors. | Some organization; points  jump around; hard to follow.  More than two important  errors. | Poorly organized; no  logical progression; hard to connect with assignment activities and logical flow.  Numerous errors  distract from understanding. |
| **Targets 1-7**                | 90%  (~13% each) | The target was provided  independently (little to no help specific to the solution); approach followed  is of good quality, clear, with precise instructions and a good amount of  background. | The target was provided  somewhat independently (some help specific to the solution); approach followed  is good, mostly clear, with precise instructions and most relevant  background. | The target was provided  with significant help; or approach is not the best or missing some important  points and background. | The target was provided  with significant help; and procedure unclear or most missing important points  and background. |

This rubric produces the **team** report grade. Each member's final mark for the assignment is that grade multiplied by their individual **discussion factor** (see the **Discussion** section).

## Arduino Hardware Issues

If you detect a problem with the Arduino assigned to you, please contact your instructor **as soon as possible to resolve the issue**.

# Insecure vending machine

Our company acquired a new vending machine for our High Tech building.
The machine has a service for automatic restocking, so it needs to be connected to the internet.
Due to the signed contract, this connection can't be taken down because it also allows the vending machine company to ensure the coherence between products bought and products available.

Since we cannot have a compromised machine with internet access near our high-tech projects, our cyber teams decided to start investigating that machine.

The investigation team has done some preliminary work, and you are tasked with exploiting the supposedly identified vulnerabilities.

# PART 1: Initial targets

## Development password
We saw the maintenance guy open a dev console. Let's see how secure the access to it is.
From our initial investigations, we believe input isn't being properly handled. Looks like password validation has different delays, depending on the input password.
Maybe we can try a **timing attack** to obtain as many credentials as possible.

**TARGET 1: Developer password**

How did you infer the password?
If you used a timing attack, plot the timing graphs for the first and second letters
If not, how long did it take to crack it?
>Hint:
>1. If you perform a timing attack, start by inferring length (length comparison is done before anything else)
>Due to *hardware constraints* you can assume that at most 20 characters are used, and only lowercase a-z characters
>2. If you don't find the right tool for the job and decide to create it yourself, make it abstract enough so further programming of the communication with the target is easy. Either way, you have the freedom to do as you want

**Required artifact (under `TARGETS/target-1/`).** Raw timing measurements as a data file (candidate character × position × repeated samples) **and** the script that produces your timing plots from it.

**Answer this (from *your* board).** What length did you infer, what was the timing margin of the winning character at each position, and which position had the *smallest* margin, and why?



## Firmware
We need to get the flashed firmware to do any analysis.
The development console may help with that.

**TARGET 2: The dumped firmware in a binary file**

**Required artifact (under `TARGETS/target-2/`).** The dumped binaries, with the SHA-256 of each.

**Answer this (from *your* board).** What is the SHA-256 and byte length of your PROGMEM dump, and at what offset does your developer password appear?


## Confidential Information
While our reverse engineering team is investigating the firmware, we can already extract information. What information is there to extract?

**TARGET 3: Confidential strings**
>Hint:
>The first analysis of any firmware involves looking at the strings present to infer the possibly hardcoded assets and other information about the system. We need all relevant information, as well as why it is relevant.

**Required artifact (under `TARGETS/target-3/`).** The full `strings` output plus your annotated list of assets.

**Answer this (from *your* board).** What is the second maintenance password, at what byte offset does it sit relative to the developer password, and how long are the base64 blobs?



