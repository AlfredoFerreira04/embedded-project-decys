# Embedded Lab

## Part I

### Target 1: Developer password

**Relevant Artifacts:**

All artifacts for this target are located under [./TARGETS/target-1/](./TARGETS/target-1/).

- Timing attack tool: [serial_pruning.cpp](./TARGETS/target-1/serial_pruning.cpp)
- Raw timing measurements: [./tool-outputs/](./TARGETS/target-1/tool-outputs/)
  - Length-sweep results
  - Character-by-position timing measurements
- Plots:
  - XXX

**Method / Explanation:**

//to-do: describe the relevant compilation/invocation for the relevant code used to extract information

**Questions:**

**1. What length did you infer?**

**Answer:** The inferred developer password length is 13 characters.

**Evidence:**

Three independent length sweeps were performed using candidates consisting of repeated X characters. The measurements exhibit a consistent timing discontinuity at a candidate length of 13 characters.

| Candidate length | Mean response time |
| ---------------: | -----------------: |
|               12 |            4340 µs |
|               13 |            5515 µs |
|               14 |            4909 µs |

The three measurements obtained for the 13-character candidate were 5512 µs, 5535 µs, and 5498 µs, resulting in a mean response time of approximately 5515 µs. The transition from 12 to 13 characters produces an increase of approximately 1175 µs. This increase was consistently reproduced across all three sweeps, indicating that it is systematic rather than attributable to measurement noise.

The anomalous measurement of 442010 µs observed for the 1-character candidate in the initial sweep was excluded from the analysis. Subsequent measurements for the same candidate were approximately 3914–3915 µs, indicating that the initial measurement was an outlier.

Based on the repeatable timing discontinuity at 13 characters, the developer password length was therefore inferred to be 13 characters.

**2. What was the timing margin of the winning character at each position?**

**Answer:** *To-do*

**3. Which position had the *smallest* margin, and why?**

**Answer:** *To-do*

### Target 2: The dumped firmware in a binary file

**Relevant Artifacts:**

//to-do

**Explanation:**

//to-do: describe the relevant compilation/invocation for the relevant code used to extract information

**Questions:**

    **1. What is the SHA-256 and byte length of your PROGMEM dump?**

    **Answer:** *To-do*

    **2.  What offset does your developer password appear?**

    **Answer:** *To-do*

### Target 3: Confidential strings

**Relevant Artifacts:**

All artifacts for this target are located under [./TARGETS/target-3/](./TARGETS/target-3/).

- Annotated Asset List: [asset_list.md](./TARGETS/target-3/asset_list.md)
- Full Strings Output: [full_strings_output.txt](./TARGETS/target-3/full_strings_output.txt)
  - Shell Script: [strings.sh](./TARGETS/target-3/strings.sh) (used to obtain full strings output from [binaries](./TARGETS/target-2/memory_dumps))

**Explanation:**

To obtain the byte offsets:
rita@LAPTOP-UFF3P787:/mnt/c/Users/micro/Documents/ISEP/MESCC/2ANO/DECYS/embedded-lab-1/embedded-project-decys/TARGETS/target-2$ grep -obUaP "danprzjzumfgn" memory_dumps_old/memory_0.bin
862:danprzjzumfgn
27977:danprzjzumfgn
rita@LAPTOP-UFF3P787:/mnt/c/Users/micro/Documents/ISEP/MESCC/2ANO/DECYS/embedded-lab-1/embedded-project-decys/TARGETS/target-2$ grep -obUaP "alancywupdjmydfadoaqvshshkgucnfwvvoqhjbxrdgndhfmhryjzn"  memory_d
umps_old/memory_0.bin
28006:alancywupdjmydfadoaqvshshkgucnfwvvoqhjbxrdgndhfmhryjzn

**Questions:**

  **1. What is the second maintenance password?**

  **Answer:** `alancywupdjmydfadoaqvshshkgucnfwvvoqhjbxrdgndhfmhryjzn`

  **2.  What byte offset does it sit relative to the developer password, and how long are the base64 blobs?**

  **Answer:** +29bytes. In `memory_0.bin`, `danprzjzumfgn` starts at offset 27977 and Alan’s password starts at offset 28006.

## Part II

### Target 4: Identify the cryptographic data

### Target 5: c&c password

### Target 6: Crack the OTP generator

### Target 7: Final secret
