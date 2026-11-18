# Build log (Part B) and AI-use note

## Trial lists and provenance

I reused my Assignment 2 trial lists for participants 1–8, generated using seed **8683**, instead of the canonical fallback lists. I copied `trials_p01.csv` through `trials_p08.csv` into `trial_lists/`. I confirmed that the participant 3 list contained eight practice rows followed by 96 experimental rows. The experiment uses the corresponding participant-numbered CSV for both loops, preserves the given row order, and divides it into rows 0–7 (practice) and 8–103 (experimental). The trial-list files were committed in **`8f00b94`**.

## Build history and version-control checkpoints

| Commit | What happened |
| --- | --- |
| `8730ede` | Added the Assignment 5 starter repository to Git. |
| `8f00b94` | Added the eight original Assignment 2 trial-list CSV files and recorded their provenance. |
| `9232425` (`predictions:`) | Committed my predictions before the first complete run, along with the initial Builder experiment. I did not revise the original predictions afterward. |
| `778edfa` (`pre-handoff:`) | Committed the hand-built PsychoPy experiment and participant 1 Pilot-mode output **before allowing the language model to edit `ldt.psyexp`**. |
| `38b6a34` | Committed the revised experiment and the completed participant 3 and 6 Run-mode outputs, including the intervening short Pilot tests. |

I first built the experiment manually in PsychoPy Builder 2026.2.4. The flow was **instructions → practice loop (`trial`, `practiceFeedback`, `iti`) → break screen → experimental loop (`trial`, `iti`) → end screen**. I created the instructions and response-key mapping, added the fixation, prime and target text stimuli, configured F/J keyboard responses, made practice feedback, and loaded the participant-specific CSV through sequential loops. During initial testing, I corrected the loop's **Selected rows** expressions; the working expressions use `$list(range(0, 8))` and `$list(range(8, 104))`, without extra literal quotation marks. The original version used second-based timing and did not yet contain all the assignment-specific output columns.

I completed the original, hand-built experiment as **participant 1 in Pilot mode** and committed its `.psyexp` and output files at `778edfa` before requesting direct model edits. After the handoff, I reopened the modified `.psyexp` in Builder, compiled the generated Python script, and tested it. The initial post-handoff Pilot attempt failed because PsychoPy's Pilot preferences automatically substituted the string `pilot` for the numeric participant ID. I disabled **Replace participant ID**, retested with participant 1, and confirmed that the experiment proceeded. I then completed the required full runs for **participants 3 and 6 in Run mode**.

The initial structural inspection of each final CSV found **107 total rows**: three rows without a trial phase, eight practice trial rows, and 96 experimental trial rows. Both files had the required named columns. The CSV header also contained **two columns named `participant`**, apparently from the experiment information and trial-list data. This prevents PowerShell's ordinary `Import-Csv` from reading the files without handling duplicate headers. I retained the raw files unchanged and used Python's `csv.reader` to inspect their headers and trial counts. This is a known limitation to discuss during output verification, not evidence that the experiment failed to run. Exact timing and the row-by-row Q1–Q2 comparison still require verification.

## Language-model handoff and pre/post diff review

- **Pre-handoff commit:** `778edfa`
- **First commit after handoff:** `38b6a34`
- **Model request:** Edit the hand-built `ldt.psyexp` to satisfy the lexical-decision specification, especially frame-based presentation, screen-synchronized responses, and the required per-trial data fields, while retaining the existing Builder structure and participant-specific trial lists.
- **Review method:** The pre-handoff and returned `.psyexp` files were compared for this handoff table. I generated the Python script in PsychoPy 2026.2.4, tested the experiment locally, and inspected the saved output files. I will review this table against my own understanding before submitting.

| Change found in the pre/post experiment comparison | Decision | Reason and review |
| --- | --- | --- |
| Added measured-refresh-rate initialization in `instructionCode`: require a valid measurement, round to integer `frameRate`, and derive frame counts. | **Kept** | Implements the specification's refresh-rate-based timing. A prior Pilot log measured about 59.65 Hz (approximately 60 Hz when rounded); the actual rate is measured at startup. |
| Changed fixation from a 0.5-second Builder duration to `fixFrames`, starting at frame 0. | **Kept** | Targets 500 ms using screen refreshes rather than elapsed-time cutoffs. |
| Changed the prime to start at `fixFrames` and last `primeFrames` (150 ms). | **Kept** | Aligns the prime directly after fixation and gives it a frame-count duration. |
| Added `trialTimingCode` to convert each CSV `soa` value into `soaFrames` and reject an SOA shorter than the prime. | **Kept** | Keeps the participant's trial-specific SOA while validating an impossible timing combination. |
| Changed the target start to `fixFrames + soaFrames` and duration to `targetFrames` (2,000 ms). | **Kept** | Measures the SOA from the prime onset, including the required blank interval after a short prime when SOA is 1,000 ms. |
| Changed `trialKey` to start on the target's frame, stop after `targetFrames`, and accept only `f` or `j`. | **Kept** | Synchronizes response collection and RT with target onset; the first valid key ends the trial, while other keys are ignored. |
| Changed practice feedback (1,000 ms), ITI (500 ms), and end screen (2,000 ms) to frame-count durations. | **Kept** | Applies the same whole-frame approach to all fixed-length intervals. |
| Added `trialRecordCode` to record `prime_shown` and `target_shown` from the actual stimulus objects. | **Kept** | Records what PsychoPy assigned to the displayed text components, rather than only copying CSV values. |
| Added `prime_onset` and `target_onset` from each stimulus's `tStartRefresh` field. | **Kept** | Stores screen-refresh-aligned timestamps comparable with PsychoPy's `.started` fields. |
| Added the explicit `key`, `rt`, `accuracy`, and `timeout` output fields, using numeric-participant parity and the trial's `correct_response`. | **Kept** | Provides the required response variables, with empty key/RT and accuracy 0 for a timeout. |
| Preserved the original instructions, practice feedback logic, sequential loops, trial-list file expression, and overall Builder flow. | **Kept unchanged** | These were created before handoff and already supported the basic task. I did not accept a redesign or shuffled trial order. |
| PsychoPy Pilot preference replaced the participant number with `pilot`, causing an integer-conversion error. | **Changed local Pilot setting** | I turned off **Replace participant ID**. This was an environment preference correction following testing, not a change to the trial list. |
| Two output columns were both named `participant`. | **Not corrected in collected raw data** | Both completed Run-mode outputs have this issue. I preserved them for transparent audit and used a reader that accepts duplicate headers; a checker must account for it rather than silently assume all headers are unique. |

I did not revert any of the main model-added timing or response-recording code. The code's intended behavior is supported by inspection and successful completion of the experiment, but successful execution does **not** by itself prove every onset, RT, or trial-list row is correct. Those remain separate verification questions.

## Experiment settings used in the revised version

| Setting | Value or behavior |
| --- | --- |
| Software | PsychoPy Builder 2026.2.4, local desktop experiment |
| Participant selection | Numeric ID entered in start dialog; loads `trial_lists/trials_pNN.csv` |
| Conditions | 8 practice rows (0–7), then 96 experimental rows (8–103); sequential order, one repetition |
| Instructions and break | SPACE advances each screen |
| Key mapping | Odd ID: F = word, J = nonword; even ID: J = word, F = nonword |
| Allowed responses | F and J; Escape quits experiment |
| Fixation | `+` for 500 ms, computed as `fixFrames` |
| Prime | CSV `prime`, lowercase in supplied lists; displayed for 150 ms (`primeFrames`) |
| SOA | Prime-onset to target-onset delay is `soa` from CSV (150 or 1,000 ms), rounded to frames |
| Target | CSV `target` converted to uppercase; displayed until valid response or a 2,000 ms limit |
| Reaction time | PsychoPy keyboard RT measured from keyboard start on the target screen refresh |
| Practice feedback | Correct, Incorrect, or Too slow; 1,000 ms after each practice trial only |
| Intertrial interval | Blank screen, 500 ms after each trial (following feedback in practice) |
| End screen | Thank-you text for 2,000 ms |
| Refresh rate | PsychoPy-measured `frameRate`, rounded to the nearest whole Hz; frame counts calculated from it. At 60 Hz: fixation 30 frames, prime 9, target maximum 120, feedback 60, ITI 30, end 120; SOA 9 or 60 frames. |
| Per-trial derived data | `prime_shown`, `target_shown`, `prime_onset`, `target_onset`, `key`, `rt`, `accuracy`, `timeout` |
| Accuracy/timeout | Accuracy = 1 only for the correct F/J response; timeout = 1 when no valid F/J response occurs within the target window |
| Data files | Timestamped participant files under `data/`; completed final runs for participant IDs 3 and 6 in Run mode |

## AI-use note

## AI-use note

 I created the initial PsychoPy experiment myself in Builder and completed the participant 1 Pilot run before handing the file to ChatGPT. After the pre-handoff commit (`778edfa`), ChatGPT modified the experiment to use frame-based timing and record stimulus onsets, responses, accuracy, and timeouts. I reopened and tested the modified experiment, corrected the Pilot-mode participant-ID setting, and completed the participant 3 and 6 runs myself.

ChatGPT also generated the Python checker and verification report. I ran the checker and preserved its original results before examining the six provided files. The first checker missed the early keyboard onset in file F, so ChatGPT helped revise Q7, and I tested and committed the correction. I retained the duplicate `participant` columns and the observed timing discrepancy in the reports rather than altering the raw data. 
## Assignment 6 addendum — instrumentation, verification, and AI use (Part F)

**Environment and provenance.** I worked in the original `a5-ldt-build` Git repository, leaving the original A5 participant 3 and 6 results unchanged. `a5-submission` remained my A5 checkpoint. PsychoPy Builder version was 2026.2.4 on Windows 11. The A6 predictions were committed before additional A6 verification under `207a680` (`predictions-a6:`), and the first working six-file Q3–Q10 checker output was committed under `40a568c` (`first-run:`). I did not edit the prediction file afterward.

**I1/I2 changes.** I added two Builder Code components to `ldt.psyexp`. `a6SessionFrameCode` sets `win.refreshThreshold = 1.5 * frameDur`, clears earlier startup intervals/counts, and writes `data/<participant>_ldt_<timestamp>_frameIntervals.log` at experiment end using `win.saveFrameIntervals`. `a6FrameCode` turns on `win.recordFrameIntervals` at the start of each `trial` routine, stores starting `win.nDroppedFrames`, then disables recording and writes `dropped_frames = win.nDroppedFrames - a6_drop_start` at the end of that trial. Practice feedback, ITI, instructions, break and end-screen routines are separate from `trial`, so they are not included in I1. I first put the End Experiment code in a reused trial component and observed two generated `saveFrameIntervals` calls; I moved it to an experiment-level component and recompiled until exactly one call remained. Experiment changes were committed using `instrument:` prefixes, including `f895ef4` and `90ea704`. The final verified file uses `a6SessionFrameCode` and `a6FrameCode`.

**Local run and tests.** After compiling Builder, I ran a complete participant 1 Pilot with the numeric-ID replacement preference disabled. I1 generated a nonempty log and the independent I1/I2 verifier reported **PASS**: 104 trials, 7,924 intervals, one >25-ms interval and one CSV drop. In normal Run mode I collected participant 7 with unnecessary applications closed and participant 8 with a muted video playing in Google Chrome. Both produced 104 trial rows plus three nontrial rows; both passed I1/I2 reconciliation and duration plausibility. P7: 8,193 intervals, 0 drops, longest 19.814 ms. P8: 8,088 intervals, 1 drop, longest 25.809 ms. The respective CSV/log drop totals matched **0=0** and **1=1**. Participant 8's CSV and frame log were committed as `ba2492c` (`data:`); participant 7's CSV and frame log were also committed in the A6 workflow (verify its hash with `git log` if needed). No participant 3/6 reruns were performed.

**Automated checker and timing audit.** I extended `check_output.py` to cover Q3–Q10, I1 and I2 and distinguish `PASS`, `FAIL`, `PILOT` and `UNDETERMINED`. It accepts duplicate `participant` headers and alternative component-name families in the supplied files. It caught participant 6 trial 26's 1,048.1-ms SOA exception and the six-file issues A/Q10, C/Q1/Q2, D/Q8, E/Q2 and F/Q7. It did not claim that CSV agreements proved actual physical display timing. I used a separate script `a6_timing_audit.py` to infer frame equivalents from saved `.started`/`.stopped` values and document all fixed-duration results; it found one 33-frame-equivalent ITI in each new run, outside I1/I2 coverage. Full findings and the original first-run output are in `a6_report.md`, and the instrumented CSV's columns and per-trial I1 log are documented in `data_dictionary.md`.

**AI-use disclosure.** I used ChatGPT as a coding and writing assistant for A6 to propose/edit the PsychoPy XML instrumentation, draft and extend the Python verifier, create the timing audit, interpret outputs, and draft report and dictionary text. My contributions were operating PsychoPy Builder locally, compiling and repeatedly verifying the generated Python code, completing Pilot and Run-mode sessions, checking the independent I1/I2 totals, preserving the required Git milestones, and reviewing the generated artifacts before submission. Initial AI-generated instrumentation created a duplicate End Experiment save because the `trial` routine was reused; this was discovered through inspecting generated `ldt.py`, corrected by moving the save to a single experiment-level Code component, and confirmed by recompilation. The generated audit report and text should be reviewed against the user's original project and Canvas instructions before submission; external hardware verification was not performed.


**Post-first-run checker refinement and AI assistance.** After preserving the initial six-file checker output in the required `first-run:` commit, I used ChatGPT to develop a targeted additional Q4/Q5 analysis that compares inferred frame-equivalent durations with scheduled integer-frame counts and reports a distinct explanation for deviations occurring on trials with logged dropped frames. I retained the original `a6_first_run_six.txt` and unchanged committed predictions, tested the revised checks against the provided files and archived A5 participant 3/6 files, and documented the newly recognized outlying participant-3 ITI separately from the previously reported participant-6 SOA failure. The analysis uses software flip timestamps and does not infer photon-level timing or assign a specific flipped frame to a dropped-frame event.
