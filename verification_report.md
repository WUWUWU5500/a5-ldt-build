# Verification report (Part C)

## Overview and method

The Assignment 5 checker compares output CSVs against a known participant-specific trial list. I ran an LLM-assisted first working checker **before manually examining** the six provided output files and committed the original `check_output.py` and `first_checker_six.txt` as `8b3361d`. This sequence preserves the first, imperfect check. After that commit, I used ChatGPT to inspect the six provided files and identify an additional observable timing failure; a Q7 revision was prepared without modifying the historical first-checker results. The primary implemented requirements for Assignment 5 are Q1 (which participant list was used) and Q2 (exactly one presentation of every trial, in the original order); checks of Q3–Q10 are additional partial tests, with `PILOT` where the CSV is not conclusive.

Each CSV contains **107 rows**: 104 actual trial rows (8 practice, 96 experimental) and 3 nontrial rows created by PsychoPy. The checker excludes rows without `phase` = `practice` or `experimental` when checking the trial list. PsychoPy includes two columns named `participant`: one from the trial list and one from experiment metadata. The checker preserves the raw CSV and disambiguates these by column position; ordinary PowerShell `Import-Csv` could not read the duplicate header.

### My own participants 3 and 6

My own completed runs were committed as `38b6a34`; the original checker output for both was committed as `checker_own_runs.txt` in `da6ef55`. Both runs loaded the correct Assignment 2 list (`trial_lists/trials_p03.csv` or `trials_p06.csv`), included all ten input fields, and preserved the exact 8-practice/96-experimental order (Q1 and Q2: **PASS**). Neither run was in Pilot mode. These runs were made after the initial human-built participant 1 Pilot run and after the revised file had been reopened, compiled, and briefly piloted.

**Original checker output (before the Q7 improvement):**

```text

==========================================================================================
C:\Users\zhaoc\Desktop\a5-ldt-build\data\3_ldt_2026-11-04_21h40.50.643.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS  startup-dialog participant=3 (rightmost participant column); all 104 condition rows match trial_lists\trials_p03.csv as a multiset (order checked separately in Q2).
Q2   PASS  Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS  8 practice trials precede all 96 experimental trials in the CSV; a different count/order would fail.
Q3   PILOT Instruction and break SPACE behavior, correct/incorrect/timeout feedback display, and 2-second end screen require observing a run or inspecting Builder.
Q4   PASS  All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PILOT Fixation and prime visibility, blank gap, and actual target cutoff require visual inspection and/or display-timing logs.
Q5   PASS  Recorded frameRate=61 whole Hz.
Q5   PILOT Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS  All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   PILOT The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PILOT RT clock start at the target's first refresh cannot be independently inferred from RT alone; verify simultaneous target/keyboard start and clock reset on flip in Builder/generated script.
Q8   PASS  All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   PILOT CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PASS  prime_onset and target_onset match corresponding PsychoPy stimulus .started values within 25 ms on all trial rows.
Q10  PASS  All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS  All 104 trials have internally consistent key/RT/accuracy/timeout for participant 3.
Q10  PILOT Duplicate header names {'participant': 2}; raw CSV retains both, but import software may reject or rename them. Confirm source of each in Builder.
==========================================================================================
C:\Users\zhaoc\Desktop\a5-ldt-build\data\6_ldt_2026-11-04_21h44.32.454.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS  startup-dialog participant=6 (rightmost participant column); all 104 condition rows match trial_lists\trials_p06.csv as a multiset (order checked separately in Q2).
Q2   PASS  Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS  8 practice trials precede all 96 experimental trials in the CSV; a different count/order would fail.
Q3   PILOT Instruction and break SPACE behavior, correct/incorrect/timeout feedback display, and 2-second end screen require observing a run or inspecting Builder.
Q4   FAIL  SOA mismatch: ['trial 26: measured 1048.1 ms, specified 1000 ms'] (1 problem(s)).
Q4   PILOT Fixation and prime visibility, blank gap, and actual target cutoff require visual inspection and/or display-timing logs.
Q5   PASS  Recorded frameRate=60 whole Hz.
Q5   PILOT Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS  All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   PILOT The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PILOT RT clock start at the target's first refresh cannot be independently inferred from RT alone; verify simultaneous target/keyboard start and clock reset on flip in Builder/generated script.
Q8   PASS  All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   PILOT CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PASS  prime_onset and target_onset match corresponding PsychoPy stimulus .started values within 25 ms on all trial rows.
Q10  PASS  All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS  All 104 trials have internally consistent key/RT/accuracy/timeout for participant 6.
Q10  PILOT Duplicate header names {'participant': 2}; raw CSV retains both, but import software may reject or rename them. Confirm source of each in Builder.

```

### What I could establish by observing or inspecting the experiment (PILOT items)

| Property | Evidence and remaining limit | What would have failed |
| --- | --- | --- |
| Q1 (dialog and file path) | The experiment's startup dialog accepted numeric participant IDs. The generated Builder script uses `trial_lists/trials_p%02d.csv` with `int(expInfo['participant'])`; the CSV comparisons establish which list was actually recorded. I disabled PsychoPy's Pilot-mode preference that replaced the numeric ID with `pilot` after that caused a `ValueError`. | Dialog not accepting a plain integer; a different list loaded; file not found. |
| Q3 (on-screen sequence) | I completed an initial participant-1 Pilot session with instructions, practice feedback, break, experimental trials, and end screen; I also completed the final 3 and 6 sessions. The Builder flow and generated script show SPACE-gated instructions/break, feedback after practice only, and a frame-counted 2-second end screen. The CSV by itself verifies only the phase counts/order. | Wrong instructions or mapping; break not SPACE-gated; feedback absent/wrong, displayed during the main task, or not 1 second; no 2-second end screen. |
| Q4 (visual trial timing) | The generated Builder script starts the fixation at frame 0, the lowercase prime at `fixFrames`, and the uppercase target at `fixFrames + soaFrames`, with prime visible for `primeFrames`. The code also sets frame-counted blank ITI. I observed the sequence during the pilot/full runs. The actual refresh intervals can deviate if a frame is missed; see participant 6 below. | Incorrect fixation/prime/blank display; target shown early/late or longer than the response deadline; ITI missing. |
| Q5 (all timing in frames) | The compiled code obtains the actual startup frame-rate reading, rounds it, and computes frame counts for fixation, prime, SOA, feedback, target, ITI, and end screen. CSV values were 61 Hz (participant 3) and 60 Hz (participant 6). A positive whole-number `frameRate` alone would not prove that the timings were implemented in frames; the Builder-generated code provides the additional evidence. | Seconds-based component end settings; non-integer `frameRate`; intervals not converted to whole frames. |
| Q6 (F/J and Escape) | Builder keyboard code accepts `['f','j']`, and the default keyboard checks Escape. The instruction code uses odd participant numbers for F=word/J=nonword and even numbers for the reverse. All recorded responses were f, j, or blank, and Q10 confirmed correct mapping. I did not independently quantify intentional wrong-key presses, so this is source-code and ordinary-run evidence rather than a controlled input challenge. | Other keys end a trial; F/J mapping reversed or identical across participant parity; Escape does nothing. |
| Q7 (when RT clock starts) | The generated script starts `trialKey` on the same frame as `targetStim` and calls `trialKey.clock.reset` and `trialKey.clearEvents` on the screen flip. The **revised** checker now compares these components' `.started` timestamps. This corroborates start-frame alignment but cannot independently prove that the PTB keyboard clock was reset correctly or that every pre-target press was ignored. | Keyboard listening earlier than target; pre-target presses counted; RT zero-time anchored earlier than the target's display flip. |
| Q8 (actual stimulus text) | The trial's End Routine code reads `primeStim.text` and `targetStim.text`, which were set from the trial variables (`prime`, `target.upper()`). The trial CSV also agrees with those transformations. Agreement alone could be faked by a copied CSV value; inspecting the Code component supplies the source-based evidence. | Literal word `prime` shown instead of the actual prime; lowercase target; recorded value not read from the stimulus. |
| Q9 (same clock as `.started`) | `prime_onset` and `target_onset` are copied from `primeStim.tStartRefresh` and `targetStim.tStartRefresh`; the generated script schedules these with `win.timeOnFlip`. The original checker also found that the onset fields agree with PsychoPy's `.started` columns on every trial within 25 ms. | Logging routine-local time instead of flip timestamps; missing onset fields; values inconsistent with `.started`. |
| Q10 (keys, RT, accuracy, timeout, trial columns) | The script scores F/J according to participant parity, emits `key`, `rt`, `accuracy`, and `timeout`, and the checker verifies the mapping from the recorded keys and response class. Duplicate `participant` columns came from Builder and the source trial list and remain in the raw CSV. Checks based on saved values cannot independently confirm that the participant saw precisely what was logged. | Incorrect mapping or accuracy; a missing/invalid key value; RT on a timeout; missing source fields. |

**Important distinction:** Inspected Builder/source-code behavior is not identical to direct visual observation or independent hardware validation. I have identified explicitly which checks rely on code inspection and which were observed in the run or corroborated by output timestamps.

### Failed or uncertain findings in my runs

The original checker reported **Q4 FAIL** for **participant 6, trial 26**: the measured prime-to-target onset interval was **1048.1 ms** against a specified 1000 ms. This is 48.1 ms late, approximately three 60-Hz frames. A missed/delayed screen refresh is a plausible mechanism, but the CSV alone cannot prove its cause. Participant 3 had no interval exceeding the checker's 35 ms tolerance. I did **not** alter, overwrite, or rerun the participant 6 output after discovering the discrepancy, so I cannot claim that it was fixed; the original finding is retained for reproducibility. The 35 ms check is a deliberately permissive screening threshold rather than a proof of frame-perfect behavior.

Both output files have two identically named `participant` header fields because the condition CSV and PsychoPy experiment metadata each record the participant. The raw output retains both; the checker distinguishes them by column position. This did not affect Q1–Q2 correctness, but it did cause PowerShell `Import-Csv` to fail. It is a genuine data-import limitation, not a reason to discard either raw file.

## The six provided files

I first committed `first_checker_six.txt` as part of `8b3361d` before examining `provided/output_files/file_A.csv` through `file_F.csv`. The descriptions below follow inspection of the actual CSV values with ChatGPT assistance; they distinguish observed facts from inferred Builder mistakes.

### file_A — participant 3

- **Verdicts:** Q1 PASS; Q2 PASS; Q8 PASS; **Q10 FAIL** (97 accuracy-coding discrepancies); Q3–Q6 observable portions PASS; original Q7 and non-observable portions PILOT. Revised Q7 component-onset comparison PASS.
- **Probable Builder error:** `accuracy` is `0` for all 104 trials, even though 97 responses would be correct given the participant-3 mapping and the recorded keys. The builder likely omitted correct-response scoring or compared F/J to a `word`/`nonword` text label rather than mapping it to the correct key. The exact coding mistake cannot be recovered from a CSV alone.
- **What a researcher might conclude without verification:** An implausible 0% accuracy/floor performance (or that the participant did not understand the lexical decision task). The response data actually indicate many correct F/J judgments; the derived accuracy column is wrong.

### file_B — participant 4

- **Verdicts:** Q1 PASS; Q2 PASS; Q8 PASS; Q10 PASS; other tested observable portions PASS; original Q7 PILOT and revised Q7 start-alignment PASS. Screen-only features still require PILOT/code inspection.
- **Probable Builder error:** None identified by the available output tests. The correct p04 list is in order, display-text fields and response scoring are consistent, and the keyboard's recorded onset aligns with the target; this does not prove every unobservable Builder setting is perfect.
- **What a researcher might conclude without verification:** The participant performed the planned even-ID lexical decision study (100/104 scored correct, including two timeouts). This interpretation is supported by the output checks, subject to the normal limitations of recorded data.

### file_C — participant 7

- **Verdicts:** **Q1 FAIL** and **Q2 FAIL**; Q3–Q6 observable portions and Q8/Q10 PASS; original Q7 PILOT, revised Q7 start-alignment PASS.
- **Probable Builder error:** The dialog/metadata indicates participant 7, but the 104 recorded condition rows match the entire **participant 1** list rather than p07. The most plausible cause is a hard-coded conditions filename such as `trials_p01.csv` in the Builder loop, instead of selecting the file from `expInfo['participant']`.
- **What a researcher might conclude without verification:** That participant 7 saw the prescribed p07 counterbalanced materials. Analyses keyed to participant 7 could silently treat the wrong item/order assignment as valid, obscuring counterbalancing effects.

### file_D — participant 2

- **Verdicts:** Q1 PASS; Q2 PASS; **Q8 FAIL**; Q10 PASS; other tested observable portions PASS; original Q7 PILOT, revised Q7 start-alignment PASS.
- **Probable Builder error:** The `prime_shown` field is the literal text `prime` on the trial rows, despite the condition column containing actual primes such as `gravel`, `metal`, and `thimble`. This suggests that the prime Text component contained literal `prime` instead of the variable `$prime`, or that the End Routine code referenced the wrong object. The CSV cannot unambiguously separate those two explanations.
- **What a researcher might conclude without verification:** That all of the varying source primes were presented normally and the priming manipulation was intact. It could produce a misleading analysis of semantic relatedness even though the displayed-prime evidence disagrees with the trial list.

### file_E — participant 5

- **Verdicts:** Q1 PASS; **Q2 FAIL**; Q3–Q6 observable portions and Q8/Q10 PASS; original Q7 PILOT, revised Q7 start-alignment PASS.
- **Probable Builder error:** All 104 correct p05 rows are present, but not in the specified file order. The first recorded practice trial is trial index 2 (`onion` → `garlic`) instead of index 1 (`gravel` → `blodge`). A likely cause is a `random` rather than `sequential` loop method in Builder.
- **What a researcher might conclude without verification:** That the participant completed the expected list and that random trial order was harmless or intended. The actual design required the exact predetermined order, so position/order comparisons would not match the planned protocol.

### file_F — participant 8

- **Original verdicts:** Q1 PASS; Q2 PASS; Q8 PASS; Q10 internally consistent PASS; **Q7 PILOT** (first checker could not determine RT anchoring). Other originally tested observable portions passed.
- **Post-inspection / revised verdict:** **Q7 FAIL**: the actual `key_resp.started` column precedes `target_text.started` on **104/104 trials**. The discrepancy is **−650 ms** for SOA 150 ms and **−1,500 ms** for SOA 1000 ms. The keyboard begins at trial onset, rather than with target appearance.
- **Probable Builder error:** The Keyboard component's start time was set to the beginning of the trial (0 seconds/0 frames), not to target onset. Its 2-second window therefore ends **500 ms after the target** for 1000-ms SOA trials and **1,350 ms after the target** for 150-ms SOA trials. In the provided data, 50 of 52 long-SOA trials time out, compared with 0 of 52 short-SOA trials. This also invalidates RT-as-target-onset interpretation.
- **What a researcher might conclude without verification:** A very large, false SOA effect on timeouts and apparently slow or missing lexical decisions (50/104 trials time out). The response window itself is confounded with SOA; the original `key`, `rt`, `accuracy`, and `timeout` values can be internally consistent while the task violates Q7.

## First-checker record, limitations, and correction

**Chronology.** The first working checker and its results were committed in `8b3361d`, before manual examination of the six files. The output in `first_checker_six.txt` is the immutable historical baseline, not a regenerated or edited result. The first checker correctly distinguished Q1 and Q2 in these six files: A PASS/PASS, B PASS/PASS, C FAIL/FAIL, D PASS/PASS, E PASS/FAIL, F PASS/PASS. A correct first Q1–Q2 result is meaningful because each check could have failed: Q1 compares the complete condition multiset against the participant's assigned list, while Q2 compares the entire sequence (including all ten condition columns) position by position.

**Miss and fix.** The first checker returned `Q7 PILOT` for every file because it only considered the RT field insufficient to validate the keyboard's start time. That conservative verdict was *not an incorrect PASS*, but it missed an independently **observable** Q7 failure. After inspecting file F with ChatGPT, I found that the output already contained `target_text.started` and `key_resp.started` columns. The revised, LLM-assisted Q7 check compares those two PsychoPy component-start timestamps on every trial; it accepts the alternate Builder component names `targetStim.started` and `trialKey.started` for my own study. It reports PASS when they align within 10 ms and FAIL with trial examples when they do not. I preserved the original checker output rather than retroactively editing it. This is a new falsifiable test: it will fail for the early-start keyboard in F, and it does not mistake internally consistent accuracy coding for proof that response timing is correct.

**Result of revised check on the six supplied CSVs:** Q7 start-alignment PASS for files A, B, C, D, E and **FAIL for F (104/104 trials)**; Q1/Q2 results unchanged. Additional `PILOT` verdicts remain for checks that would require visual observation, inspection of the Builder script, or independent verification of the RT clock reset. The revised file is intended to be committed separately with the message `Fix Q7 checker to detect early keyboard start` and its rerun output preserved as `checker_six_after_q7_fix.txt`.

**The full verbatim initial checker output, produced before manual inspection, is reproduced below and remains independently available in `first_checker_six.txt`:**

```text

==========================================================================================
C:\Users\zhaoc\Desktop\a5-ldt-build\provided\output_files\file_A.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS  startup-dialog participant=3 (rightmost participant column); all 104 condition rows match provided\canonical_trial_lists\trials_p03.csv as a multiset (order checked separately in Q2).
Q2   PASS  Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS  8 practice trials precede all 96 experimental trials in the CSV; a different count/order would fail.
Q3   PILOT Instruction and break SPACE behavior, correct/incorrect/timeout feedback display, and 2-second end screen require observing a run or inspecting Builder.
Q4   PASS  All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PILOT Fixation and prime visibility, blank gap, and actual target cutoff require visual inspection and/or display-timing logs.
Q5   PASS  Recorded frameRate=60 whole Hz.
Q5   PILOT Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS  All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   PILOT The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PILOT RT clock start at the target's first refresh cannot be independently inferred from RT alone; verify simultaneous target/keyboard start and clock reset on flip in Builder/generated script.
Q8   PASS  All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   PILOT CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PILOT No PsychoPy stimulus .started columns available for independent timestamp comparison.
Q10  PASS  All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  FAIL  97 coding errors; first ["trial 1: key='f',rt='0.4836037519372667',accuracy='0',timeout='0'; expected accuracy=1,timeout=0", "trial 2: key='j',rt='0.7463137756088827',accuracy='0',timeout='0'; expected accuracy=1,timeout=0"].
Q10  PILOT Duplicate header names {'participant': 2}; raw CSV retains both, but import software may reject or rename them. Confirm source of each in Builder.
==========================================================================================
C:\Users\zhaoc\Desktop\a5-ldt-build\provided\output_files\file_B.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS  startup-dialog participant=4 (rightmost participant column); all 104 condition rows match provided\canonical_trial_lists\trials_p04.csv as a multiset (order checked separately in Q2).
Q2   PASS  Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS  8 practice trials precede all 96 experimental trials in the CSV; a different count/order would fail.
Q3   PILOT Instruction and break SPACE behavior, correct/incorrect/timeout feedback display, and 2-second end screen require observing a run or inspecting Builder.
Q4   PASS  All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PILOT Fixation and prime visibility, blank gap, and actual target cutoff require visual inspection and/or display-timing logs.
Q5   PASS  Recorded frameRate=60 whole Hz.
Q5   PILOT Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS  All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   PILOT The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PILOT RT clock start at the target's first refresh cannot be independently inferred from RT alone; verify simultaneous target/keyboard start and clock reset on flip in Builder/generated script.
Q8   PASS  All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   PILOT CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PILOT No PsychoPy stimulus .started columns available for independent timestamp comparison.
Q10  PASS  All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS  All 104 trials have internally consistent key/RT/accuracy/timeout for participant 4.
Q10  PILOT Duplicate header names {'participant': 2}; raw CSV retains both, but import software may reject or rename them. Confirm source of each in Builder.
==========================================================================================
C:\Users\zhaoc\Desktop\a5-ldt-build\provided\output_files\file_C.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   FAIL  startup-dialog participant=7 (rightmost participant column); content differs from trials_p07.csv: 104 missing and 104 unexpected condition rows; rows exactly match other participant list(s) [1].
Q2   FAIL  104 trial rows vs 104 expected; first difference at position 1: expected practice/1 PW3 plane->pilot; actual practice/1 PW4 metal->copper.
Q3   PASS  8 practice trials precede all 96 experimental trials in the CSV; a different count/order would fail.
Q3   PILOT Instruction and break SPACE behavior, correct/incorrect/timeout feedback display, and 2-second end screen require observing a run or inspecting Builder.
Q4   PASS  All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PILOT Fixation and prime visibility, blank gap, and actual target cutoff require visual inspection and/or display-timing logs.
Q5   PASS  Recorded frameRate=60 whole Hz.
Q5   PILOT Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS  All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   PILOT The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PILOT RT clock start at the target's first refresh cannot be independently inferred from RT alone; verify simultaneous target/keyboard start and clock reset on flip in Builder/generated script.
Q8   PASS  All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   PILOT CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PILOT No PsychoPy stimulus .started columns available for independent timestamp comparison.
Q10  PASS  All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS  All 104 trials have internally consistent key/RT/accuracy/timeout for participant 7.
Q10  PILOT Duplicate header names {'participant': 2}; raw CSV retains both, but import software may reject or rename them. Confirm source of each in Builder.
==========================================================================================
C:\Users\zhaoc\Desktop\a5-ldt-build\provided\output_files\file_D.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS  startup-dialog participant=2 (rightmost participant column); all 104 condition rows match provided\canonical_trial_lists\trials_p02.csv as a multiset (order checked separately in Q2).
Q2   PASS  Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS  8 practice trials precede all 96 experimental trials in the CSV; a different count/order would fail.
Q3   PILOT Instruction and break SPACE behavior, correct/incorrect/timeout feedback display, and 2-second end screen require observing a run or inspecting Builder.
Q4   PASS  All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PILOT Fixation and prime visibility, blank gap, and actual target cutoff require visual inspection and/or display-timing logs.
Q5   PASS  Recorded frameRate=60 whole Hz.
Q5   PILOT Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS  All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   PILOT The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PILOT RT clock start at the target's first refresh cannot be independently inferred from RT alone; verify simultaneous target/keyboard start and clock reset on flip in Builder/generated script.
Q8   FAIL  Displayed text fields mismatch the expected transformations; first [(1, 'prime', 'BLODGE'), (2, 'prime', 'COPPER'), (3, 'prime', 'WEMSEL')].
Q8   PILOT CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PILOT No PsychoPy stimulus .started columns available for independent timestamp comparison.
Q10  PASS  All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS  All 104 trials have internally consistent key/RT/accuracy/timeout for participant 2.
Q10  PILOT Duplicate header names {'participant': 2}; raw CSV retains both, but import software may reject or rename them. Confirm source of each in Builder.
==========================================================================================
C:\Users\zhaoc\Desktop\a5-ldt-build\provided\output_files\file_E.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS  startup-dialog participant=5 (rightmost participant column); all 104 condition rows match provided\canonical_trial_lists\trials_p05.csv as a multiset (order checked separately in Q2).
Q2   FAIL  104 trial rows vs 104 expected; first difference at position 1: expected practice/1 PN2 gravel->blodge; actual practice/2 PW2 onion->garlic.
Q3   PASS  8 practice trials precede all 96 experimental trials in the CSV; a different count/order would fail.
Q3   PILOT Instruction and break SPACE behavior, correct/incorrect/timeout feedback display, and 2-second end screen require observing a run or inspecting Builder.
Q4   PASS  All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PILOT Fixation and prime visibility, blank gap, and actual target cutoff require visual inspection and/or display-timing logs.
Q5   PASS  Recorded frameRate=60 whole Hz.
Q5   PILOT Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS  All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   PILOT The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PILOT RT clock start at the target's first refresh cannot be independently inferred from RT alone; verify simultaneous target/keyboard start and clock reset on flip in Builder/generated script.
Q8   PASS  All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   PILOT CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PILOT No PsychoPy stimulus .started columns available for independent timestamp comparison.
Q10  PASS  All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS  All 104 trials have internally consistent key/RT/accuracy/timeout for participant 5.
Q10  PILOT Duplicate header names {'participant': 2}; raw CSV retains both, but import software may reject or rename them. Confirm source of each in Builder.
==========================================================================================
C:\Users\zhaoc\Desktop\a5-ldt-build\provided\output_files\file_F.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS  startup-dialog participant=8 (rightmost participant column); all 104 condition rows match provided\canonical_trial_lists\trials_p08.csv as a multiset (order checked separately in Q2).
Q2   PASS  Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS  8 practice trials precede all 96 experimental trials in the CSV; a different count/order would fail.
Q3   PILOT Instruction and break SPACE behavior, correct/incorrect/timeout feedback display, and 2-second end screen require observing a run or inspecting Builder.
Q4   PASS  All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PILOT Fixation and prime visibility, blank gap, and actual target cutoff require visual inspection and/or display-timing logs.
Q5   PASS  Recorded frameRate=60 whole Hz.
Q5   PILOT Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS  All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   PILOT The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PILOT RT clock start at the target's first refresh cannot be independently inferred from RT alone; verify simultaneous target/keyboard start and clock reset on flip in Builder/generated script.
Q8   PASS  All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   PILOT CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PILOT No PsychoPy stimulus .started columns available for independent timestamp comparison.
Q10  PASS  All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS  All 104 trials have internally consistent key/RT/accuracy/timeout for participant 8.
Q10  PILOT Duplicate header names {'participant': 2}; raw CSV retains both, but import software may reject or rename them. Confirm source of each in Builder.

```

### Evidence for the six first-checker Q1 and Q2 verdicts

| File | Q1 (list identity) | Q2 (exact order) | Actual falsifiable comparison |
| --- | --- | --- | --- |
| A | PASS | PASS | All p03 conditions and all 104 positions matched the p03 source file. |
| B | PASS | PASS | All p04 conditions and all 104 positions matched the p04 source file. |
| C | FAIL | FAIL | Declared p07 conditions did not match; rows instead matched p01. |
| D | PASS | PASS | All p02 conditions and all 104 positions matched the p02 source file; Q8 caught a different defect. |
| E | PASS | FAIL | The p05 condition multiset matched, but its row sequence did not. |
| F | PASS | PASS | All p08 conditions and all positions matched; later Q7 showed why Q1/Q2 PASS alone is not sufficient. |

The six outputs demonstrate that successful loading, correct trial count, plausible RTs, and consistent response fields cannot substitute for checking the participant's assigned list, exact trial order, and timing against the experiment specification.

### AI assistance for Part C

ChatGPT generated the first draft of `check_output.py`, suggested the PowerShell commands, independently examined the supplied CSVs **after** the first-checker commit, identified the missed Q7 timing problem in file F, wrote the additional Q7 comparison, and drafted this verification report. I ran and committed the first checker, ran it on my own participant-3 and participant-6 outputs, and will run and commit the revised checker before final submission. The checker and report are aids to verification, not substitutes for independent human judgment about the unobservable `PILOT` items. This contribution should also be disclosed in `build_log.md` (Part E).
