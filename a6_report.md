# Assignment 6 — Verification report and timing audit (Part C)

**Experiment:** PsychoPy Builder lexical decision task, `ldt.psyexp` (PsychoPy 2026.2.4).  **Analysis date:** November 17, 2026.  **Evidence:** `a6_own_verification.txt`, committed first run `a6_first_run_six.txt` (`40a568c`), `a6_timing_results.txt`, generated Builder `ldt.py`, and I1/I2 logs for participant IDs 7 and 8. The tag `a5-submission` remains the pre-A6 experiment snapshot.

**Decision convention:** `PASS` and `FAIL` refer to falsifiable software/output checks only. `UNDETERMINED` means the available output alone does not settle the claimed behavior; `PILOT` should be used when that behavior is independently settled by the Builder script or observation rather than by a CSV. A `PASS` is not proof of photon-level accuracy. The full checker transcripts are reproduced in Appendix A and B.

## 1. Assignment 5 build against Q3–Q10

My A5 participant 3 and participant 6 files each contain **107 rows** (one instructions row, eight practice trials, one break row, 96 experimental trials, one final row), and **104 actual trials**. They were collected in Run mode before I1/I2 were added; these original data were not altered or rerun.

| Property | Participant 3 | Participant 6 | Interpretation after inspecting the own-build script / pilot |
|---|---|---|---|
| Q3 routine sequence | PASS + output-only UNDETERMINED | PASS + output-only UNDETERMINED | Builder flow and complete Pilot/Run observation support instructions → 8 practice trials with feedback/ITI → SPACE break → 96 main trials with ITI → 2-s ending. A CSV alone only proves recorded order. |
| Q4 fixation / prime / SOA | PASS on measured software intervals; visibility UNDETERMINED | **FAIL** on trial 26 SOA; fixation/prime pass | Trial 26 recorded **1048.1 ms** where **1000 ms** was specified, an overshoot of **48.1 ms (~2.9 frames at 60 Hz)**. It may reflect a delayed flip, but run 6 had no interval-level I1 record, so the cause is not established. Other recorded intervals passed. |
| Q5 rounded refresh and frame-count implementation | 61 Hz integer PASS | 60 Hz integer PASS | Generated Builder script computes `fixFrames`, `primeFrames`, `soaFrames`, `feedbackFrames`, `itiFrames`, `endFrames`, and `targetFrames` from a rounded measured rate and schedules starts/stops by `frameN`; this resolves the implementation question for the own build, not physical delivery. |
| Q6 permitted keys | PASS; CSV-only behavior UNDETERMINED | PASS; CSV-only behavior UNDETERMINED | `trialKey.getKeys(keyList=['f','j'], ignoreKeys=['escape'])` accepts F/J during the target; the default keyboard independently checks Escape. Odd/even participant instruction mapping is in `instructionCode`. No external hardware verification is implied. |
| Q7 response-window onset | PASS; RT reset CSV-only UNDETERMINED | PASS; RT reset CSV-only UNDETERMINED | Generated code schedules `trialKey` and `targetStim` at the same `frameN`, uses `win.callOnFlip(trialKey.clock.reset)` and `win.callOnFlip(trialKey.clearEvents, ...)`, and ignores keys during the onset flip. This establishes the programmed clock reset/clear mechanism. |
| Q8 shown text | PASS; object provenance CSV-only UNDETERMINED | PASS; object provenance CSV-only UNDETERMINED | `trialRecordCode` explicitly reads `str(primeStim.text)` and `str(targetStim.text)`, not only source CSV strings. |
| Q9 custom onsets | PASS; photon timing UNDETERMINED | PASS; photon timing UNDETERMINED | `prime_onset`/`target_onset` read the matching visual objects' `tStartRefresh` and agree with their `.started` columns. Physical onset requires a photodiode. |
| Q10 recorded responses, scoring | PASS; duplicate header noted | PASS; duplicate header noted | `trialRecordCode` uses odd/even participant key mapping, the first accepted F/J key, keyboard RT, and explicit blank RT/timeout behavior. Raw CSV contains two columns named `participant`, a data-import problem rather than an observed wrong score. |

**Resolution of failed checks:** Participant 6's Q4 exception is a failure of the measured single-trial timing outcome, **not a proven Builder logic bug**. The A6 changes instrumented frame delivery but did not retroactively repair the A5 sample, and there is no separate `fix:` commit claiming to fix that trial. In the subsequent runs 7 and 8, all 104 measured SOAs per run were within tolerance. Keep the A5 failure visible in the record.

**Pilot and inspection evidence:** I completed a numeric-ID participant 1 A6 Pilot run after disabling PsychoPy's setting that replaces numeric IDs with the string `pilot`. The complete Pilot showed instructions, practice feedback, break and final screen, and generated a matching frame-interval log. I then completed participants 7 and 8 in Run mode. The specific operational checks for Q6/Q7/Q8 are additionally supported by the generated Python code described above; I do not claim to have independently tested every possible invalid-key sequence.

**A5-to-A6 code change:** The task flow, trial lists, F/J mapping and stimulus scheduling were retained. I1 and I2 added frame-interval recording and per-trial `dropped_frames`. The generated Python script was compiled locally and `win.saveFrameIntervals(...)` was verified to occur once. The successful A6 Pilot had 104 trial rows, 7,924 I1 intervals, 1 CSV/log drop in each source, and plausibly matching recorded trial-screen duration.

## 2. Timing audit

### 2.1 Machine and collection conditions

| Configuration | Participant 7 — quiet | Participant 8 — Chrome video |
|---|---|---|
| Computer and OS | Windows 11; **exact machine model to confirm locally** | Same computer and OS |
| Display and OS-selected refresh rate | **OS display model/setting not independently recorded**; experiment measured/rounded **60 Hz** | Same display; experiment measured/rounded **60 Hz** |
| PsychoPy window | Fullscreen `True` in normal Run mode (from generated script); Pilot is windowed by preference | Same normal Run-mode setting |
| PsychoPy | 2026.2.4 | 2026.2.4 |
| Main load | Unnecessary applications closed | A muted video playing in Google Chrome in background |
| Scheduled full trials | 8 practice + 96 experimental | 8 practice + 96 experimental |
| CSV file | `data/7_ldt_2026-11-17_20h24.57.075.csv` | `data/8_ldt_2026-11-17_20h31.06.094.csv` |
| I1 log | Matching `_frameIntervals.log` | Matching `_frameIntervals.log` |

The exact computer model, display model and Windows **Settings → System → Display → Advanced display** refresh-rate setting were not captured in the supplied verification records and must be entered from the test machine rather than guessed. The saved software `frameRate` field is not the same as an independently documented Windows setting.

### 2.2 Expected frame counts and achieved software timestamp distributions

**Method:** I computed `round((stop_timestamp − start_timestamp) × frameRate)` for each event that had matching `.started` and `.stopped` fields. This reconstructs **frame-equivalent counts from software timestamps**; it does not directly count physical screen refreshes. The nominal `frameRate` was 60 Hz in both runs. The short SOA appeared in 52 trials and the long SOA in 52 trials per run.

| Event | Q5 required at 60 Hz | Run 7 (quiet) | Run 8 (video) |
|---|---:|---|---|
| Fixation | 30 | 30 frames ×104 (492.27–501.40 ms) | 30 ×104 (494.41–501.64 ms) |
| Prime | 9 | 9 ×104 (149.04–151.85 ms) | 9 ×104 (146.91–151.86 ms) |
| Prime→target, SOA=150 ms | 9 | 9 ×52 (149.10–151.85 ms) | 9 ×52 (146.91–151.45 ms) |
| Prime→target, SOA=1000 ms | 60 | 60 ×52 (998.53–1000.96 ms) | 60 ×52 (997.42–1000.99 ms) |
| ITI | 30 | **30 ×103; 33 ×1** (498.17–557.75 ms) | **30 ×103; 33 ×1** (495.87–556.57 ms) |
| Practice feedback | 60 | 60 ×8 (998.07–1000.87 ms) | 60 ×8 (998.92–1003.94 ms) |
| Final screen | 120 | 120 ×1 (1997.63 ms) | 120 ×1 (1997.79 ms) |
| **I2 dropped frames in trial screens** | threshold interval >25.000 ms | **0** | **1** |
| Longest logged I1 interval | — | **19.814 ms** | **25.809 ms** |
| Recorded I1 intervals | — | 8,193 | 8,088 |
| Sum of recorded I1 intervals | — | 136.478 s | 134.734 s |
| Approximate trial-screen span from CSV timestamps | — | 136.509 s | 134.769 s |
| Difference between span and I1 sum | — | 0.031 s | 0.036 s |

**Deviations from requested frame-equivalent count:** There were **exactly two** departures in this measured set: participant 7's **experimental trial 19 ITI** estimated as 33 frames, and participant 8's **experimental trial 21 ITI** estimated as 33 frames. On both trials, I2 recorded `dropped_frames=0`. That does not prove the intervening display was correct: **ITI is outside I1/I2 recording**, so I2 intentionally cannot detect delays during ITI flips. The 56–58 ms excess could reflect scheduling or rendering delays, but the existing recording cannot identify its cause. There were no other count deviations among the audited fixed events.

**I1/I2 numerical reconciliation:** PsychoPy threshold `1.5 × (1/60 s) = 25.000 ms`. In participant 7, `sum(dropped_frames)=0` and **0** I1 intervals exceed threshold; in participant 8, `sum(dropped_frames)=1` and **1** I1 interval exceeds threshold. Thus **both runs PASS**, consistent with the independent verifier. The I1 total duration is only 31–36 ms below the corresponding software trial-screen spans, consistent with the startup/stop boundary intervals and the requirement to exclude feedback and ITIs. This does not prove the interval recorder captured literal photons or every nontrial event.

**Interpretation of load:** The predicted qualitative direction (more drops with a muted video) matched the observations, but the absolute counts were far smaller than forecast: **0 (rather than 2)** and **1 (rather than 12)**. Two runs, one per condition, do not establish a causal effect of browser video; other display/OS timing variation is possible.

### 2.3 Three timing-evidence bins for Q4, Q5, Q7, Q9 and Q10

**Bin 1 — Verified from software timestamps, conditional on accurate flip timestamping.** Q4: fixation and prime start/stop deltas and both prime-to-target SOAs match their scheduled frame equivalents on all 104 participant 7/8 trials. Q7: `trialKey.started` and `targetStim.started` have the same software flip timestamp, and `win.callOnFlip(trialKey.clock.reset)` is present in the code. Q9: custom `prime_onset` and `target_onset` reproduce the matching `.started` values; Q10: the saved first valid key, nonnegative response latency, accuracy, and timeout are internally consistent with the target-locked programming. Q5's per-trial drop totals reconcile with I1 intervals for the monitored period.

**Bin 2 — Bounded but not directly verified from the saved data.** Q4's **physical** fixation, prime, blank-gap, and target durations are approximated by rounded frame counts and the flip interval measurements, but software cannot establish exact visibility at the screen. Q5's scheduled frame-count scheme is verified by reading the Builder-generated code, while physical display performance outside I1 (feedback, ITI, break, end screen) is only bounded by software onset/offset stamps. Q7's latest response acceptance is programmed as `targetFrames`, and Q10's 2-s timeout is based on that number of frames; when a trial ends on an early key, the target's *maximum-duration* behavior is not tested, and any delayed flip can shift elapsed time. There is no second-by-second hardware upper bound without separate measurement.

| Screen setting | Fixation / ITI (500 ms) | Prime (150 ms) | SOA 150 ms | SOA 1000 ms | Feedback (1000 ms) | End screen (2000 ms) | Target maximum (2000 ms) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 60 Hz | 30 | 9 | 9 | 60 | 60 | 120 | 120 |
| 75 Hz | 38 | 11 | 11 | 75 | 75 | 150 | 150 |
| 120 Hz | 60 | 18 | 18 | 120 | 120 | 240 | 240 |
| 144 Hz | 72 | 22 | 22 | 144 | 144 | 288 | 288 |

These counts come from `round(duration_ms × rounded_frameRate / 1000)` in `instructionCode` and per-trial `soaFrames` in `trialTimingCode`, then `frameN` comparisons in the Builder-generated script. **At 75 Hz**, the 500-ms count becomes 38 frames (=506.7 ms nominal) and the 150-ms count becomes 11 frames (=146.7 ms nominal); millisecond durations do not always divide evenly into whole frames. No runs were conducted at 75, 120 or 144 Hz, so those are *program predictions*, not measured outcomes.

**Bin 3 — Not reachable without external hardware.** A photodiode placed on the display (plus synchronized acquisition/trigger) would be needed to verify Q4's actual light onset/offset and blank interval, Q5's physically delivered refreshes and timing drift, and Q9's visual onset relative to the software timestamps. Independent keyboard event measurement (or an instrumented response device with synchronized timing) would be needed to verify Q7/Q10 input latency and precise physical response window boundaries. The software log can detect delayed flip calls but cannot by itself prove when the LCD/OLED pixels visibly changed.

## 3. Six provided files (simulated 60-Hz display)

The six supplied CSVs were generated by a simulated participant on a perfect simulated 60-Hz display; they lack the Builder code and I1/I2 logs. The first working Q3–Q10 checker and its output were committed as **`40a568c` (`first-run:`)** before the subsequent manual review. The complete, unedited first-run transcript is included in **Appendix B**.

| File | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---|---|---|---|---|---|---|---|---|---|---|
| A | PASS | PASS | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* | **FAIL** scoring; required columns PASS |
| B | PASS | PASS | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* |
| C | **FAIL** | **FAIL** | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* |
| D | PASS | PASS | PASS* | PASS* | PASS* | PASS* | PASS* | **FAIL** shown prime | PASS* | PASS* |
| E | PASS | **FAIL** | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* | PASS* |
| F | PASS | PASS | PASS* | PASS* | PASS* | PASS* | **FAIL** keyboard onset | PASS* | PASS* | PASS* |

`PASS*` means the **CSV-verifiable subchecks passed**, but the property also has a separate **UNDETERMINED** component. This is deliberately not an overall claim that the complete property was verified from a CSV. All provided files have I1/I2 = UNDETERMINED because their independent logs/build were not supplied.

### General limits for every provided file

The same unresolved questions apply to A–F even where measurable fields pass: **Q3** physical instructions, correct/incorrect/timeout feedback, SPACE gating, break/end behavior; **Q4** whether the stimulus was genuinely visible, blank gap rendered, and target cutoff accurate; **Q5** whether every duration was coded in frame counts instead of coincidentally producing 60-Hz-like stamps; **Q6** handling of irrelevant keys and Escape; **Q7** actual RT clock reset on the target flip and rejection of pre-target presses; **Q8** whether the recorded shown strings came from the actual TextStim objects; **Q9** physical light-onset timing, which requires a photodiode; and **Q10** duplicate `participant` header provenance/source inspection where present. Appropriate settling evidence would be the original Builder/generated Python project, a complete and deliberately varied functional Pilot run, and independent stimulus/response hardware measurements for photon- and input-level claims. The supplied CSV alone is insufficient for those portions. The checker nevertheless *could fail* on the falsifiable subconditions: Q3 phase/order, Q4 recorded onset/fixation/prime durations, Q5 rounded frameRate, Q6 stored key domain, Q7 keyboard versus target `.started`, Q8 shown text against intended text, Q9 internal onset duplication, Q10 scoring/header/RT/timeout.

### file_A

- **Verdicts Q3–Q10:** All CSV-verifiable subchecks PASS **except** Q10 accuracy coding: 97 trial rows inconsistent with expected participant-specific F/J mapping (out of 104). The remaining behavioral/physical aspects are `UNDETERMINED` as listed above. The file has 104 trial rows.
- **Most plausible Builder/configuration mistake:** An incorrect key-to-correctness comparison or participant parity condition, e.g. flipped accuracy mapping; raw key/RT values can still be plausible. This is an inference from output, **not a verified observation of the unavailable Builder file**.
- **What an uncritical researcher might conclude:** Responses and apparent error rates might be interpreted as true poor performance, although the scoring is internally wrong.
- **UNDETERMINED and settling evidence:** Inspect original Builder/component parameters and generated Python code for Q3–Q8 behavior and Q10 provenance; perform a controlled Pilot with invalid/early/late keys; use a photodiode for actual Q4/Q9 display onset and Q5 physical frame delivery. No independent I1/I2 log exists for this provided file.

### file_B

- **Verdicts Q3–Q10:** All CSV-verifiable subchecks PASS **except** No observed CSV-verifiable Q3–Q10 failure. The remaining behavioral/physical aspects are `UNDETERMINED` as listed above. The file has 104 trial rows.
- **Most plausible Builder/configuration mistake:** No specific Builder defect is supported by this CSV; avoid assuming perfect implementation. This is an inference from output, **not a verified observation of the unavailable Builder file**.
- **What an uncritical researcher might conclude:** The file looks internally coherent, but this is not proof that instructions, ignored keys, frame-coded durations, or physical displays were correct.
- **UNDETERMINED and settling evidence:** Inspect original Builder/component parameters and generated Python code for Q3–Q8 behavior and Q10 provenance; perform a controlled Pilot with invalid/early/late keys; use a photodiode for actual Q4/Q9 display onset and Q5 physical frame delivery. No independent I1/I2 log exists for this provided file.

### file_C

- **Verdicts Q3–Q10:** All CSV-verifiable subchecks PASS **except** Q1 and Q2 fail (dialog participant 7, recorded conditions match another participant list); observable Q3–Q10 checks pass. The remaining behavioral/physical aspects are `UNDETERMINED` as listed above. The file has 104 trial rows.
- **Most plausible Builder/configuration mistake:** Likely selected the wrong participant-numbered condition list or entered/opened a mismatching list while retaining dialog ID 7. This is an inference from output, **not a verified observation of the unavailable Builder file**.
- **What an uncritical researcher might conclude:** The analyst might treat the condition rows as legitimate participant 7 data and miss participant-to-stimulus misassignment.
- **UNDETERMINED and settling evidence:** Inspect original Builder/component parameters and generated Python code for Q3–Q8 behavior and Q10 provenance; perform a controlled Pilot with invalid/early/late keys; use a photodiode for actual Q4/Q9 display onset and Q5 physical frame delivery. No independent I1/I2 log exists for this provided file.

### file_D

- **Verdicts Q3–Q10:** All CSV-verifiable subchecks PASS **except** Q8 fails: `prime_shown` records literal `prime` rather than expected prime strings. The remaining behavioral/physical aspects are `UNDETERMINED` as listed above. The file has 104 trial rows.
- **Most plausible Builder/configuration mistake:** Likely stored the literal string `prime` instead of reading `primeStim.text`, or recorded a wrong constant for the shown-prime field. This is an inference from output, **not a verified observation of the unavailable Builder file**.
- **What an uncritical researcher might conclude:** An analyst might conclude every prime was the word “prime,” or trust other trial-list prime values and overlook the broken shown-text provenance.
- **UNDETERMINED and settling evidence:** Inspect original Builder/component parameters and generated Python code for Q3–Q8 behavior and Q10 provenance; perform a controlled Pilot with invalid/early/late keys; use a photodiode for actual Q4/Q9 display onset and Q5 physical frame delivery. No independent I1/I2 log exists for this provided file.

### file_E

- **Verdicts Q3–Q10:** All CSV-verifiable subchecks PASS **except** Q2 fails on the canonical item order (same rows, different order); observable Q3–Q10 checks pass. The remaining behavioral/physical aspects are `UNDETERMINED` as listed above. The file has 104 trial rows.
- **Most plausible Builder/configuration mistake:** Likely used a random/shuffled loop instead of sequential list order, or otherwise reordered trials while preserving the list multiset. This is an inference from output, **not a verified observation of the unavailable Builder file**.
- **What an uncritical researcher might conclude:** The researcher could assume trial position and condition sequence matched the preregistered list and attribute order-dependent effects incorrectly.
- **UNDETERMINED and settling evidence:** Inspect original Builder/component parameters and generated Python code for Q3–Q8 behavior and Q10 provenance; perform a controlled Pilot with invalid/early/late keys; use a photodiode for actual Q4/Q9 display onset and Q5 physical frame delivery. No independent I1/I2 log exists for this provided file.

### file_F

- **Verdicts Q3–Q10:** All CSV-verifiable subchecks PASS **except** Q7 fails: keyboard component begins 650 ms or 1500 ms before target (104/104 trials). The remaining behavioral/physical aspects are `UNDETERMINED` as listed above. The file has 104 trial rows.
- **Most plausible Builder/configuration mistake:** Likely configured the keyboard to start at trial onset instead of at `fixFrames + soaFrames`; target itself begins later. This is an inference from output, **not a verified observation of the unavailable Builder file**.
- **What an uncritical researcher might conclude:** The researcher might interpret reaction times as target-locked although responses or RT clocks may have started during fixation/prime/blank time.
- **UNDETERMINED and settling evidence:** Inspect original Builder/component parameters and generated Python code for Q3–Q8 behavior and Q10 provenance; perform a controlled Pilot with invalid/early/late keys; use a photodiode for actual Q4/Q9 display onset and Q5 physical frame delivery. No independent I1/I2 log exists for this provided file.

### First working checker, repairs, and A5's blind spots

The first working A6 checker, preserved in commit **`40a568c`**, detected exactly the observable failures summarized above. **I did not discover and silently correct a wrong Q3–Q10 verdict after that milestone**, so there was no further `first-run:` checker revision to document at this stage. Its distinct tests are falsifiable, not generic PASS labels: phase order in Q3, measured SOAs/visible-duration timestamps in Q4, positive integer refresh in Q5, F/J/blank domain in Q6, keyboard-versus-target start timing in Q7, text string transformation in Q8, redundant timestamp agreement in Q9, and participant-specific key/accuracy/timeout consistency in Q10. On file B all of these output subchecks could have failed on a different CSV, but none did here. The same applies to the unaffected subchecks of files A, C, D, E and F.

**Which A5 check came closest but missed new failures?** A5 **Q1** verifies participant-specific condition content, and **Q2** verifies each condition row appears once in canonical order. Therefore Q1/Q2 passed files **A, D and F** even though each has a different **post-list execution/data-logging flaw**: A miscalculates accuracy (Q10), D misrecords shown prime text (Q8), F starts the keyboard too early (Q7). Q2 is superficially closest to D's item-string provenance/order and Q1 to A's participant parity, but neither observes the visual text object's logged field, correctness equation or keyboard onset time; both rely on trial-list fields rather than response/stimulus evidence. C and E were already caught by A5's Q1/Q2 comparisons.

**Specific failure mechanisms:** A includes 97 inconsistently coded trial accuracies; D records a constant `prime_shown='prime'` instead of each actual prime; F's keyboard is timestamped **650 ms early in 150-ms SOA trials** and **1500 ms early in 1000-ms SOA trials**, consistent with listening from trial start rather than target onset. C's participant 7 dialog ID is inconsistent with a different participant list; E preserves the trial multiset but changes canonical order. No need to re-label them as Q3 failures merely because Q1/Q2 failed—the checker distinguishes phase ordering from list content order.

## 4. Reconciliation with committed Part A predictions

**Prediction 1 — Provided-file Q3–Q10 table and observable-vs-unobservable split.** The predicted Q10 fail in A, Q8 fail in D, Q7 fail in F and output-level passes in the other inspected portions were confirmed. In C and E, the list identity/order errors are Q1/Q2 rather than Q3–Q10 failures; their **eight practice then 96 experimental** phase structure still passes Q3. The checks cannot establish the actual presented instructions, physical durations, whether all durations were defined by frames, ignored-key behavior, actual object provenance, or light-onset timing without additional sources. There were no contrary cells within the operationalized CSV tests; a numerical PASS does **not** cancel an UNDETERMINED behavioral component.

**Prediction 2 — Count of new failures among files that passed A5 Q1/Q2.** Predicted **three files A, D, F**; observed **three files A, D, F**. The mechanism is that Q1/Q2 inspect the identity and order of the trial-list rows, not whether response scoring, shown-text recording, or keyboard onset is correctly implemented. The prediction was correct.

**Prediction 3 — Local refresh rate and frame counts.** Predicted ~60 Hz; both A6 runs recorded a rounded **60 Hz**. Fixation/ITI 30, prime 9, SOA150 9, SOA1000 60, feedback 60 and end 120 match the code and achieved timestamps except the two longer ITIs noted above. The prior A5 participant 3 run recorded 61 Hz; PsychoPy estimates refresh independently at startup and rounding can vary slightly between sessions.

**Prediction 4 — Tagged A5 Q3–Q10 exception and uncertainties.** Predicted a Q4 outlier on participant 6 near 1048 ms, and it was found on trial 26; participant 3's measured SOAs passed. The A5 CSV cannot retrospectively reveal whether a particular frame was missed, because I1 was not running then. The duplicate raw `participant` header was also confirmed. Instrumented P7/P8 show proper onset alignment but cannot prove photon-level target visibility or every edge case in keyboard/timeout behavior.

**Prediction 5 — I2 drops quiet vs video.** Predicted P7 **2** and P8 **12**; observed P7 **0** and P8 **1**. The operational mechanism is **far fewer measured intervals exceeded 1.5 frames than expected**; running a muted browser video did not generate the assumed level of GPU/CPU contention in this single run. The video run still had one >25-ms interval, compared with none in quiet condition, but that is not evidence of a statistically established or causal load effect. The two 33-frame-equivalent ITIs are outside the I1/I2 sampling window and must not be counted as I2 drops.

**Prediction 6 — One delayed flip within the prime.** The frame-number-based code retains the scheduled count but any delayed `win.flip()` between prime onset and offset could extend **elapsed millisecond duration** and possibly the prime-to-target SOA. This mechanism is supported by the scheduling code, but in P7/P8 no prime-count deviations were observed and the one P8 drop could not be localized to the prime from the aggregate I1 log alone. It remains a conditional prediction, not an observed prime-specific incident.

**Prediction 7 — Three limits of evidence.** The three predicted software checks—fixation-to-prime interval, prime-to-target SOA, and keyboard-start/target-start coincidence—were assessed using software timestamps. The ability to bound visual duration is conditional on measured flip behavior and does not establish physical pixels. A photodiode and synchronized input-device timing are still required for true screen-light and external response latency claims.

**Prediction-table cell corrections:** The only material qualification is that the word `PASS` in the predicted table often meant a **falsifiable CSV subproperty**, rather than full Q3–Q10 compliance. In the final A6 checker, each of those has a separate `UNDETERMINED` row. These are distinct evidence scopes, not contradictions or retrospective edits to predictions.

## Appendix A — Checker output on own participants 3, 6, 7 and 8 (verbatim)

```text
==========================================================================================
.\data\3_ldt_2026-11-04_21h40.50.643.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS         startup-dialog participant=3 (rightmost participant column); all 104 condition rows match trial_lists\trials_p03.csv as a multiset (order checked separately in Q2).
Q2   PASS         Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS         104 trial rows: 8 practice first, then 96 experimental, in recorded order.
Q3   UNDETERMINED Trial CSV cannot prove instruction text, SPACE gating, feedback visibility, break behavior, or final 2-s display. Inspect Builder and watch a complete run; hardware is needed for physical durations.
Q4   PASS         All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PASS         fixation: all 104 recorded start/stop intervals within 35 ms of 500 ms.
Q4   PASS         prime: all 104 recorded start/stop intervals within 35 ms of 150 ms.
Q4   UNDETERMINED On-screen appearance, actual blank gap and physical target cut-off need direct observation and/or photodiode; software flip timing alone is insufficient.
Q5   PASS         Recorded frameRate=61 whole Hz.
Q5   UNDETERMINED Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS         All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   UNDETERMINED The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PASS         Keyboard and target start on the same logged refresh on all 104 trials (trialKey.started versus targetStim.started; <=2 ms tolerance).
Q7   UNDETERMINED Matching component-start timestamps alone cannot prove the keyboard RT clock was reset on that screen flip or that no earlier keystrokes leaked in; inspect generated code and test with intentionally early and late keys.
Q8   PASS         All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   UNDETERMINED CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PASS         Both custom onset fields match the primeStim.started/targetStim.started logged flip timestamps across 104 trials (2 ms tolerance).
Q9   UNDETERMINED Software flip timestamps do not establish photon emission timing; a photodiode would be needed for physical onset.
Q10  PASS         All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS         All 104 trials have internally consistent key/RT/accuracy/timeout for participant 3.
Q10  UNDETERMINED Duplicate header names {'participant': 2}; raw CSV preserves both, but import software may rename them. Confirm provenance in Builder.
I1   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
I2   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
==========================================================================================
.\data\6_ldt_2026-11-04_21h44.32.454.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS         startup-dialog participant=6 (rightmost participant column); all 104 condition rows match trial_lists\trials_p06.csv as a multiset (order checked separately in Q2).
Q2   PASS         Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS         104 trial rows: 8 practice first, then 96 experimental, in recorded order.
Q3   UNDETERMINED Trial CSV cannot prove instruction text, SPACE gating, feedback visibility, break behavior, or final 2-s display. Inspect Builder and watch a complete run; hardware is needed for physical durations.
Q4   FAIL         SOA mismatch: ['trial 26: measured 1048.1 ms, specified 1000 ms'] (1 problem(s)).
Q4   PASS         fixation: all 104 recorded start/stop intervals within 35 ms of 500 ms.
Q4   PASS         prime: all 104 recorded start/stop intervals within 35 ms of 150 ms.
Q4   UNDETERMINED On-screen appearance, actual blank gap and physical target cut-off need direct observation and/or photodiode; software flip timing alone is insufficient.
Q5   PASS         Recorded frameRate=60 whole Hz.
Q5   UNDETERMINED Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS         All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   UNDETERMINED The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PASS         Keyboard and target start on the same logged refresh on all 104 trials (trialKey.started versus targetStim.started; <=2 ms tolerance).
Q7   UNDETERMINED Matching component-start timestamps alone cannot prove the keyboard RT clock was reset on that screen flip or that no earlier keystrokes leaked in; inspect generated code and test with intentionally early and late keys.
Q8   PASS         All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   UNDETERMINED CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PASS         Both custom onset fields match the primeStim.started/targetStim.started logged flip timestamps across 104 trials (2 ms tolerance).
Q9   UNDETERMINED Software flip timestamps do not establish photon emission timing; a photodiode would be needed for physical onset.
Q10  PASS         All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS         All 104 trials have internally consistent key/RT/accuracy/timeout for participant 6.
Q10  UNDETERMINED Duplicate header names {'participant': 2}; raw CSV preserves both, but import software may rename them. Confirm provenance in Builder.
I1   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
I2   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
==========================================================================================
.\data\7_ldt_2026-11-17_20h24.57.075.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS         startup-dialog participant=7 (rightmost participant column); all 104 condition rows match trial_lists\trials_p07.csv as a multiset (order checked separately in Q2).
Q2   PASS         Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS         104 trial rows: 8 practice first, then 96 experimental, in recorded order.
Q3   UNDETERMINED Trial CSV cannot prove instruction text, SPACE gating, feedback visibility, break behavior, or final 2-s display. Inspect Builder and watch a complete run; hardware is needed for physical durations.
Q4   PASS         All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PASS         fixation: all 104 recorded start/stop intervals within 35 ms of 500 ms.
Q4   PASS         prime: all 104 recorded start/stop intervals within 35 ms of 150 ms.
Q4   UNDETERMINED On-screen appearance, actual blank gap and physical target cut-off need direct observation and/or photodiode; software flip timing alone is insufficient.
Q5   PASS         Recorded frameRate=60 whole Hz.
Q5   UNDETERMINED Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS         All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   UNDETERMINED The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PASS         Keyboard and target start on the same logged refresh on all 104 trials (trialKey.started versus targetStim.started; <=2 ms tolerance).
Q7   UNDETERMINED Matching component-start timestamps alone cannot prove the keyboard RT clock was reset on that screen flip or that no earlier keystrokes leaked in; inspect generated code and test with intentionally early and late keys.
Q8   PASS         All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   UNDETERMINED CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PASS         Both custom onset fields match the primeStim.started/targetStim.started logged flip timestamps across 104 trials (2 ms tolerance).
Q9   UNDETERMINED Software flip timestamps do not establish photon emission timing; a photodiode would be needed for physical onset.
Q10  PASS         All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS         All 104 trials have internally consistent key/RT/accuracy/timeout for participant 7.
Q10  UNDETERMINED Duplicate header names {'participant': 2}; raw CSV preserves both, but import software may rename them. Confirm provenance in Builder.
I1   PASS         8193 intervals, sum=136.478s, max=19.81ms; trial-screen span=136.509s; difference=0.031s; tolerance=5.200s. Builder code intends to exclude feedback/ITI/instructions/break/end.
I2   PASS         per-trial CSV drops=0; logged intervals >25.000ms=0; 104 trial rows.
==========================================================================================
.\data\8_ldt_2026-11-17_20h31.06.094.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS         startup-dialog participant=8 (rightmost participant column); all 104 condition rows match trial_lists\trials_p08.csv as a multiset (order checked separately in Q2).
Q2   PASS         Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS         104 trial rows: 8 practice first, then 96 experimental, in recorded order.
Q3   UNDETERMINED Trial CSV cannot prove instruction text, SPACE gating, feedback visibility, break behavior, or final 2-s display. Inspect Builder and watch a complete run; hardware is needed for physical durations.
Q4   PASS         All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PASS         fixation: all 104 recorded start/stop intervals within 35 ms of 500 ms.
Q4   PASS         prime: all 104 recorded start/stop intervals within 35 ms of 150 ms.
Q4   UNDETERMINED On-screen appearance, actual blank gap and physical target cut-off need direct observation and/or photodiode; software flip timing alone is insufficient.
Q5   PASS         Recorded frameRate=60 whole Hz.
Q5   UNDETERMINED Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS         All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   UNDETERMINED The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PASS         Keyboard and target start on the same logged refresh on all 104 trials (trialKey.started versus targetStim.started; <=2 ms tolerance).
Q7   UNDETERMINED Matching component-start timestamps alone cannot prove the keyboard RT clock was reset on that screen flip or that no earlier keystrokes leaked in; inspect generated code and test with intentionally early and late keys.
Q8   PASS         All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   UNDETERMINED CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PASS         Both custom onset fields match the primeStim.started/targetStim.started logged flip timestamps across 104 trials (2 ms tolerance).
Q9   UNDETERMINED Software flip timestamps do not establish photon emission timing; a photodiode would be needed for physical onset.
Q10  PASS         All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS         All 104 trials have internally consistent key/RT/accuracy/timeout for participant 8.
Q10  UNDETERMINED Duplicate header names {'participant': 2}; raw CSV preserves both, but import software may rename them. Confirm provenance in Builder.
I1   PASS         8088 intervals, sum=134.734s, max=25.81ms; trial-screen span=134.769s; difference=0.036s; tolerance=5.200s. Builder code intends to exclude feedback/ITI/instructions/break/end.
I2   PASS         per-trial CSV drops=1; logged intervals >25.000ms=1; 104 trial rows.
```

## Appendix B — First working Q3–Q10 checker on six provided files (verbatim; Git commit `40a568c`)

```text
==========================================================================================
provided/output_files/file_A.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS         startup-dialog participant=3 (rightmost participant column); all 104 condition rows match provided/canonical_trial_lists/trials_p03.csv as a multiset (order checked separately in Q2).
Q2   PASS         Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS         104 trial rows: 8 practice first, then 96 experimental, in recorded order.
Q3   UNDETERMINED Trial CSV cannot prove instruction text, SPACE gating, feedback visibility, break behavior, or final 2-s display. Inspect Builder and watch a complete run; hardware is needed for physical durations.
Q4   PASS         All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PASS         fixation: all 104 recorded start/stop intervals within 35 ms of 500 ms.
Q4   PASS         prime: all 104 recorded start/stop intervals within 35 ms of 150 ms.
Q4   UNDETERMINED On-screen appearance, actual blank gap and physical target cut-off need direct observation and/or photodiode; software flip timing alone is insufficient.
Q5   PASS         Recorded frameRate=60 whole Hz.
Q5   UNDETERMINED Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS         All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   UNDETERMINED The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PASS         Keyboard and target start on the same logged refresh on all 104 trials (key_resp.started versus target_text.started; <=2 ms tolerance).
Q7   UNDETERMINED Matching component-start timestamps alone cannot prove the keyboard RT clock was reset on that screen flip or that no earlier keystrokes leaked in; inspect generated code and test with intentionally early and late keys.
Q8   PASS         All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   UNDETERMINED CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PASS         Both custom onset fields match the prime_text.started/target_text.started logged flip timestamps across 104 trials (2 ms tolerance).
Q9   UNDETERMINED Software flip timestamps do not establish photon emission timing; a photodiode would be needed for physical onset.
Q10  PASS         All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  FAIL         97 coding errors; first ["trial 1: key='f',rt='0.4836037519372667',accuracy='0',timeout='0'; expected accuracy=1,timeout=0", "trial 2: key='j',rt='0.7463137756088827',accuracy='0',timeout='0'; expected accuracy=1,timeout=0"].
Q10  UNDETERMINED Duplicate header names {'participant': 2}; raw CSV preserves both, but import software may rename them. Confirm provenance in Builder.
I1   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
I2   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
==========================================================================================
provided/output_files/file_B.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS         startup-dialog participant=4 (rightmost participant column); all 104 condition rows match provided/canonical_trial_lists/trials_p04.csv as a multiset (order checked separately in Q2).
Q2   PASS         Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS         104 trial rows: 8 practice first, then 96 experimental, in recorded order.
Q3   UNDETERMINED Trial CSV cannot prove instruction text, SPACE gating, feedback visibility, break behavior, or final 2-s display. Inspect Builder and watch a complete run; hardware is needed for physical durations.
Q4   PASS         All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PASS         fixation: all 104 recorded start/stop intervals within 35 ms of 500 ms.
Q4   PASS         prime: all 104 recorded start/stop intervals within 35 ms of 150 ms.
Q4   UNDETERMINED On-screen appearance, actual blank gap and physical target cut-off need direct observation and/or photodiode; software flip timing alone is insufficient.
Q5   PASS         Recorded frameRate=60 whole Hz.
Q5   UNDETERMINED Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS         All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   UNDETERMINED The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PASS         Keyboard and target start on the same logged refresh on all 104 trials (key_resp.started versus target_text.started; <=2 ms tolerance).
Q7   UNDETERMINED Matching component-start timestamps alone cannot prove the keyboard RT clock was reset on that screen flip or that no earlier keystrokes leaked in; inspect generated code and test with intentionally early and late keys.
Q8   PASS         All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   UNDETERMINED CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PASS         Both custom onset fields match the prime_text.started/target_text.started logged flip timestamps across 104 trials (2 ms tolerance).
Q9   UNDETERMINED Software flip timestamps do not establish photon emission timing; a photodiode would be needed for physical onset.
Q10  PASS         All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS         All 104 trials have internally consistent key/RT/accuracy/timeout for participant 4.
Q10  UNDETERMINED Duplicate header names {'participant': 2}; raw CSV preserves both, but import software may rename them. Confirm provenance in Builder.
I1   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
I2   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
==========================================================================================
provided/output_files/file_C.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   FAIL         startup-dialog participant=7 (rightmost participant column); content differs from trials_p07.csv: 104 missing and 104 unexpected condition rows; rows exactly match other participant list(s) [1].
Q2   FAIL         104 trial rows vs 104 expected; first difference at position 1: expected practice/1 PW3 plane->pilot; actual practice/1 PW4 metal->copper.
Q3   PASS         104 trial rows: 8 practice first, then 96 experimental, in recorded order.
Q3   UNDETERMINED Trial CSV cannot prove instruction text, SPACE gating, feedback visibility, break behavior, or final 2-s display. Inspect Builder and watch a complete run; hardware is needed for physical durations.
Q4   PASS         All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PASS         fixation: all 104 recorded start/stop intervals within 35 ms of 500 ms.
Q4   PASS         prime: all 104 recorded start/stop intervals within 35 ms of 150 ms.
Q4   UNDETERMINED On-screen appearance, actual blank gap and physical target cut-off need direct observation and/or photodiode; software flip timing alone is insufficient.
Q5   PASS         Recorded frameRate=60 whole Hz.
Q5   UNDETERMINED Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS         All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   UNDETERMINED The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PASS         Keyboard and target start on the same logged refresh on all 104 trials (key_resp.started versus target_text.started; <=2 ms tolerance).
Q7   UNDETERMINED Matching component-start timestamps alone cannot prove the keyboard RT clock was reset on that screen flip or that no earlier keystrokes leaked in; inspect generated code and test with intentionally early and late keys.
Q8   PASS         All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   UNDETERMINED CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PASS         Both custom onset fields match the prime_text.started/target_text.started logged flip timestamps across 104 trials (2 ms tolerance).
Q9   UNDETERMINED Software flip timestamps do not establish photon emission timing; a photodiode would be needed for physical onset.
Q10  PASS         All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS         All 104 trials have internally consistent key/RT/accuracy/timeout for participant 7.
Q10  UNDETERMINED Duplicate header names {'participant': 2}; raw CSV preserves both, but import software may rename them. Confirm provenance in Builder.
I1   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
I2   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
==========================================================================================
provided/output_files/file_D.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS         startup-dialog participant=2 (rightmost participant column); all 104 condition rows match provided/canonical_trial_lists/trials_p02.csv as a multiset (order checked separately in Q2).
Q2   PASS         Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS         104 trial rows: 8 practice first, then 96 experimental, in recorded order.
Q3   UNDETERMINED Trial CSV cannot prove instruction text, SPACE gating, feedback visibility, break behavior, or final 2-s display. Inspect Builder and watch a complete run; hardware is needed for physical durations.
Q4   PASS         All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PASS         fixation: all 104 recorded start/stop intervals within 35 ms of 500 ms.
Q4   PASS         prime: all 104 recorded start/stop intervals within 35 ms of 150 ms.
Q4   UNDETERMINED On-screen appearance, actual blank gap and physical target cut-off need direct observation and/or photodiode; software flip timing alone is insufficient.
Q5   PASS         Recorded frameRate=60 whole Hz.
Q5   UNDETERMINED Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS         All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   UNDETERMINED The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PASS         Keyboard and target start on the same logged refresh on all 104 trials (key_resp.started versus target_text.started; <=2 ms tolerance).
Q7   UNDETERMINED Matching component-start timestamps alone cannot prove the keyboard RT clock was reset on that screen flip or that no earlier keystrokes leaked in; inspect generated code and test with intentionally early and late keys.
Q8   FAIL         Displayed text fields mismatch the expected transformations; first [(1, 'prime', 'BLODGE'), (2, 'prime', 'COPPER'), (3, 'prime', 'WEMSEL')].
Q8   UNDETERMINED CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PASS         Both custom onset fields match the prime_text.started/target_text.started logged flip timestamps across 104 trials (2 ms tolerance).
Q9   UNDETERMINED Software flip timestamps do not establish photon emission timing; a photodiode would be needed for physical onset.
Q10  PASS         All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS         All 104 trials have internally consistent key/RT/accuracy/timeout for participant 2.
Q10  UNDETERMINED Duplicate header names {'participant': 2}; raw CSV preserves both, but import software may rename them. Confirm provenance in Builder.
I1   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
I2   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
==========================================================================================
provided/output_files/file_E.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS         startup-dialog participant=5 (rightmost participant column); all 104 condition rows match provided/canonical_trial_lists/trials_p05.csv as a multiset (order checked separately in Q2).
Q2   FAIL         104 trial rows vs 104 expected; first difference at position 1: expected practice/1 PN2 gravel->blodge; actual practice/2 PW2 onion->garlic.
Q3   PASS         104 trial rows: 8 practice first, then 96 experimental, in recorded order.
Q3   UNDETERMINED Trial CSV cannot prove instruction text, SPACE gating, feedback visibility, break behavior, or final 2-s display. Inspect Builder and watch a complete run; hardware is needed for physical durations.
Q4   PASS         All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PASS         fixation: all 104 recorded start/stop intervals within 35 ms of 500 ms.
Q4   PASS         prime: all 104 recorded start/stop intervals within 35 ms of 150 ms.
Q4   UNDETERMINED On-screen appearance, actual blank gap and physical target cut-off need direct observation and/or photodiode; software flip timing alone is insufficient.
Q5   PASS         Recorded frameRate=60 whole Hz.
Q5   UNDETERMINED Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS         All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   UNDETERMINED The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   PASS         Keyboard and target start on the same logged refresh on all 104 trials (key_resp.started versus target_text.started; <=2 ms tolerance).
Q7   UNDETERMINED Matching component-start timestamps alone cannot prove the keyboard RT clock was reset on that screen flip or that no earlier keystrokes leaked in; inspect generated code and test with intentionally early and late keys.
Q8   PASS         All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   UNDETERMINED CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PASS         Both custom onset fields match the prime_text.started/target_text.started logged flip timestamps across 104 trials (2 ms tolerance).
Q9   UNDETERMINED Software flip timestamps do not establish photon emission timing; a photodiode would be needed for physical onset.
Q10  PASS         All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS         All 104 trials have internally consistent key/RT/accuracy/timeout for participant 5.
Q10  UNDETERMINED Duplicate header names {'participant': 2}; raw CSV preserves both, but import software may rename them. Confirm provenance in Builder.
I1   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
I2   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
==========================================================================================
provided/output_files/file_F.csv
ROWS: 107 total, 104 trials, 3 nontrial
Q1   PASS         startup-dialog participant=8 (rightmost participant column); all 104 condition rows match provided/canonical_trial_lists/trials_p08.csv as a multiset (order checked separately in Q2).
Q2   PASS         Exactly 104 rows in exact list order (8 practice, 96 experimental); 3 nontrial rows excluded.
Q3   PASS         104 trial rows: 8 practice first, then 96 experimental, in recorded order.
Q3   UNDETERMINED Trial CSV cannot prove instruction text, SPACE gating, feedback visibility, break behavior, or final 2-s display. Inspect Builder and watch a complete run; hardware is needed for physical durations.
Q4   PASS         All 104 observed prime-to-target intervals within 35 ms of specified SOA.
Q4   PASS         fixation: all 104 recorded start/stop intervals within 35 ms of 500 ms.
Q4   PASS         prime: all 104 recorded start/stop intervals within 35 ms of 150 ms.
Q4   UNDETERMINED On-screen appearance, actual blank gap and physical target cut-off need direct observation and/or photodiode; software flip timing alone is insufficient.
Q5   PASS         Recorded frameRate=60 whole Hz.
Q5   UNDETERMINED Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.
Q6   PASS         All recorded trial responses are f, j, or empty (could fail if any other key was recorded).
Q6   UNDETERMINED The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.
Q7   FAIL         Keyboard onset differs from target onset on 104/104 trials; first ['trial 1: keyboard starts -650.0 ms relative to target', 'trial 2: keyboard starts -650.0 ms relative to target', 'trial 3: keyboard starts -1500.0 ms relative to target', 'trial 4: keyboard starts -650.0 ms relative to target'].
Q7   UNDETERMINED Matching component-start timestamps alone cannot prove the keyboard RT clock was reset on that screen flip or that no earlier keystrokes leaked in; inspect generated code and test with intentionally early and late keys.
Q8   PASS         All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.
Q8   UNDETERMINED CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.
Q9   PASS         Both custom onset fields match the prime_text.started/target_text.started logged flip timestamps across 104 trials (2 ms tolerance).
Q9   UNDETERMINED Software flip timestamps do not establish photon emission timing; a photodiode would be needed for physical onset.
Q10  PASS         All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.
Q10  PASS         All 104 trials have internally consistent key/RT/accuracy/timeout for participant 8.
Q10  UNDETERMINED Duplicate header names {'participant': 2}; raw CSV preserves both, but import software may rename them. Confirm provenance in Builder.
I1   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
I2   UNDETERMINED This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery.
```
