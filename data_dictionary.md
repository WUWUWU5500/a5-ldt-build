# Data dictionary — Assignment 6 instrumented lexical-decision output (Part D)

**Reference file:** `data/7_ldt_2026-11-17_20h24.57.075.csv`. The instrumented CSV contains **85 header fields** (84 named plus a trailing unnamed field). It contains **107 records**: one instructions row, 8 practice trials, one break row, 96 experimental trials, and one end-screen row. Participant 8 uses the same schema.

**Important for reading:** There are **two raw columns both named `participant`**: column 1 comes from the selected trial list, while column 77 comes from the dialog. The timing audit temporarily renames the second one to `participant__copy2`; this is **not** a literal raw CSV header. The 85th column has an empty header and blank values. Use `csv.reader` or rename duplicates explicitly rather than relying on `csv.DictReader`/`pandas` to resolve duplicate names silently.

**Timestamp interpretation:** PsychoPy stimulus and keyboard `*.started`/`*.stopped` events are queued on `win.flip()` and therefore provide **software screen-flip-aligned timestamps**, not photodiode measurements. The routine-level `trial.started`, `iti.stopped`, etc. are **routine/CPU timestamps**, which must not be treated as identical to screen-flip times. `*.stopped` fields for target/keyboard may be absent on trials terminated by a response before the scheduled timeout.

**Units:** Times are seconds unless a column explicitly specifies milliseconds (`soa`); frame intervals in the separate I1 file are seconds. Missing numeric response time is stored as an empty string, and some automatic key-duration fields contain `None`. Loop counters are zero based.

| # | Raw CSV column | Source | Meaning / timing reference | Units or values | Populated rows |
|---:|---|---|---|---|---|
| 1 | `participant` | trial-list CSV | Participant ID embedded in the selected trial list | integer ID | all 107 output rows (replicated experiment metadata) |
| 2 | `phase` | trial-list CSV | Practice or experimental phase | practice / experimental | 104 trials (8 practice + 96 experimental) |
| 3 | `trial_index` | trial-list CSV | List-defined trial index | integer | 104 trials (8 practice + 96 experimental) |
| 4 | `item_id` | trial-list CSV | Item identifier | string | 104 trials (8 practice + 96 experimental) |
| 5 | `target` | trial-list CSV | Target string as specified in list | string | 104 trials (8 practice + 96 experimental) |
| 6 | `prime` | trial-list CSV | Prime string as specified in list | string | 104 trials (8 practice + 96 experimental) |
| 7 | `relatedness` | trial-list CSV | Prime-target relatedness condition | categorical string | 104 trials (8 practice + 96 experimental) |
| 8 | `soa` | trial-list CSV | Prime-onset-to-target-onset SOA requested by the list | milliseconds; 150 or 1000 | 104 trials (8 practice + 96 experimental) |
| 9 | `correct_response` | trial-list CSV | Correct lexical decision category | word / nonword | 104 trials (8 practice + 96 experimental) |
| 10 | `seed` | trial-list CSV | List generation seed | integer; 8683 | 104 trials (8 practice + 96 experimental) |
| 11 | `thisN` | PsychoPy automatic | Current trial running index within active loop | 0-based integer | 104 trials (8 practice + 96 experimental) |
| 12 | `thisTrialN` | PsychoPy automatic | Trial index within current repetition | 0-based integer | 104 trials (8 practice + 96 experimental) |
| 13 | `thisRepN` | PsychoPy automatic | Repetition index | 0-based integer | 104 trials (8 practice + 96 experimental) |
| 14 | `trialKey.keys` | PsychoPy automatic (`trialKey`) | Key captured by trial keyboard | f / j / None | 104 trials (8 practice + 96 experimental) |
| 15 | `trialKey.rt` | PsychoPy automatic (`trialKey`) | Response time measured by keyboard after target onset | seconds | 104 trials (8 practice + 96 experimental) |
| 16 | `trialKey.duration` | PsychoPy automatic (`trialKey`) | Recorded keypress hold duration when available | seconds or None | 104 trials (8 practice + 96 experimental) |
| 17 | `practiceLoop.thisRepN` | PsychoPy automatic (`practiceLoop`) | Practice repetition index | 0-based integer | 8 practice trials |
| 18 | `practiceLoop.thisTrialN` | PsychoPy automatic (`practiceLoop`) | Practice trial index in repetition | 0-based integer | 8 practice trials |
| 19 | `practiceLoop.thisN` | PsychoPy automatic (`practiceLoop`) | Practice running trial index | 0-based integer | 8 practice trials |
| 20 | `practiceLoop.thisIndex` | PsychoPy automatic (`practiceLoop`) | Index of practice item within selected list | 0-based integer | 8 practice trials |
| 21 | `mainLoop.thisRepN` | PsychoPy automatic (`mainLoop`) | Main repetition index | 0-based integer | 96 experimental trials |
| 22 | `mainLoop.thisTrialN` | PsychoPy automatic (`mainLoop`) | Main trial index in repetition | 0-based integer | 96 experimental trials |
| 23 | `mainLoop.thisN` | PsychoPy automatic (`mainLoop`) | Main running trial index | 0-based integer | 96 experimental trials |
| 24 | `mainLoop.thisIndex` | PsychoPy automatic (`mainLoop`) | Index of experimental item within selected list | 0-based integer | 96 experimental trials |
| 25 | `thisRow.t` | PsychoPy automatic | Scheduled/display-row timestamp associated with trial start | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 26 | `notes` | PsychoPy automatic | PsychoPy notes field; unused in current runs | text, usually blank | usually blank |
| 27 | `piloting` | PsychoPy automatic | Whether the experiment was run in Pilot mode | True / False | first nontrial row |
| 28 | `instructions.started` | PsychoPy automatic | Instructions routine start (routine/CPU timestamp, not necessarily flip) | seconds on global clock | first nontrial row |
| 29 | `instructionsText.started` | PsychoPy automatic (`instructionsText`) | instructionsText: onset scheduled on `win.flip()` | seconds on global clock | first nontrial row |
| 30 | `instructionsKey.started` | PsychoPy automatic (`instructionsKey`) | instructionsKey: listening onset scheduled on `win.flip()` | seconds on global clock | first nontrial row |
| 31 | `instructions.stopped` | PsychoPy automatic | Instructions routine end (routine/CPU timestamp, not necessarily flip) | seconds on global clock | first nontrial row |
| 32 | `instructionsKey.keys` | PsychoPy automatic (`instructionsKey`) | key (SPACE expected) | f / j / space / None | first nontrial row |
| 33 | `instructionsKey.rt` | PsychoPy automatic (`instructionsKey`) | RT relative to instructions key start | seconds or None | first nontrial row |
| 34 | `instructionsKey.duration` | PsychoPy automatic (`instructionsKey`) | keypress duration | seconds or None | first nontrial row |
| 35 | `trial.started` | PsychoPy automatic | Trial routine start (routine/CPU timestamp, not necessarily flip) | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 36 | `fixation.started` | PsychoPy automatic (`fixation`) | fixation: onset scheduled on `win.flip()` | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 37 | `fixation.stopped` | PsychoPy automatic (`fixation`) | fixation: offset scheduled on `win.flip()` | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 38 | `primeStim.started` | PsychoPy automatic (`primeStim`) | primeStim: onset scheduled on `win.flip()` | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 39 | `primeStim.stopped` | PsychoPy automatic (`primeStim`) | primeStim: offset scheduled on `win.flip()` | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 40 | `targetStim.started` | PsychoPy automatic (`targetStim`) | targetStim: onset scheduled on `win.flip()` | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 41 | `trialKey.started` | PsychoPy automatic (`trialKey`) | trialKey: listening onset scheduled on `win.flip()` | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 42 | `trial.stopped` | PsychoPy automatic | Trial routine end (routine/CPU timestamp, not necessarily flip) | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 43 | `dropped_frames` | Code component (`a6FrameCode`) | Number of recorded trial-frame intervals longer than 1.5 rounded-refresh periods | nonnegative integer; count | 104 trials (8 practice + 96 experimental) |
| 44 | `practiceLoop.trialKey.keys` | PsychoPy automatic (`practiceLoop`) | Practice-loop keyboard key copied from trialKey | f / j / None | 8 practice trials |
| 45 | `practiceLoop.trialKey.rt` | PsychoPy automatic (`practiceLoop`) | Practice-loop keyboard response latency | seconds | 8 practice trials |
| 46 | `practiceLoop.trialKey.duration` | PsychoPy automatic (`practiceLoop`) | Practice-loop keyboard keypress duration | seconds or None | 8 practice trials |
| 47 | `prime_shown` | Code component (`trialRecordCode`) | Prime text read from live `primeStim.text` object | string, normally lowercase | 104 trials (8 practice + 96 experimental) |
| 48 | `target_shown` | Code component (`trialRecordCode`) | Target text read from live `targetStim.text` object | uppercase string | 104 trials (8 practice + 96 experimental) |
| 49 | `prime_onset` | Code component (`trialRecordCode`) | Prime visual object `tStartRefresh` | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 50 | `target_onset` | Code component (`trialRecordCode`) | Target visual object `tStartRefresh` | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 51 | `key` | Code component (`trialRecordCode`) | First valid key after target onset, if any | f / j / blank | 104 trials (8 practice + 96 experimental) |
| 52 | `rt` | Code component (`trialRecordCode`) | Latency to first valid key from target onset; blank on timeout | seconds or blank | 104 trials (8 practice + 96 experimental) |
| 53 | `accuracy` | Code component (`trialRecordCode`) | Participant-parity-dependent accuracy of first valid key | 0 / 1 | 104 trials (8 practice + 96 experimental) |
| 54 | `timeout` | Code component (`trialRecordCode`) | Whether target response window ended without valid F/J response | 0 / 1 | 104 trials (8 practice + 96 experimental) |
| 55 | `practiceFeedback.started` | PsychoPy automatic | Practice-feedback routine beginning (CPU/handler time) | seconds on global clock | 8 practice trials |
| 56 | `feedbackText.started` | PsychoPy automatic (`feedbackText`) | Practice feedback visual text onset on `win.flip()` | seconds on global clock | 8 practice trials |
| 57 | `feedbackText.stopped` | PsychoPy automatic (`feedbackText`) | Practice feedback visual text offset on `win.flip()` | seconds on global clock | 8 practice trials |
| 58 | `practiceFeedback.stopped` | PsychoPy automatic | Practice-feedback routine end (CPU/handler time) | seconds on global clock | 8 practice trials |
| 59 | `iti.started` | PsychoPy automatic | ITI routine start (routine/CPU timestamp, not necessarily flip) | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 60 | `blankText.started` | PsychoPy automatic (`blankText`) | blankText: onset scheduled on `win.flip()` | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 61 | `blankText.stopped` | PsychoPy automatic (`blankText`) | blankText: offset scheduled on `win.flip()` | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 62 | `iti.stopped` | PsychoPy automatic | ITI routine end (routine/CPU timestamp, not necessarily flip) | seconds on global clock | 104 trials (8 practice + 96 experimental) |
| 63 | `breakScreen.started` | PsychoPy automatic | Break routine start (routine/CPU timestamp, not necessarily flip) | seconds on global clock | one break nontrial row |
| 64 | `breakText.started` | PsychoPy automatic (`breakText`) | breakText: onset scheduled on `win.flip()` | seconds on global clock | one break nontrial row |
| 65 | `breakKey.started` | PsychoPy automatic (`breakKey`) | breakKey: listening onset scheduled on `win.flip()` | seconds on global clock | one break nontrial row |
| 66 | `breakScreen.stopped` | PsychoPy automatic | Break routine end (routine/CPU timestamp, not necessarily flip) | seconds on global clock | one break nontrial row |
| 67 | `breakKey.keys` | PsychoPy automatic (`breakKey`) | key (SPACE expected) | f / j / space / None | one break nontrial row |
| 68 | `breakKey.rt` | PsychoPy automatic (`breakKey`) | RT relative to break key start | seconds or None | one break nontrial row |
| 69 | `breakKey.duration` | PsychoPy automatic (`breakKey`) | keypress duration | seconds or None | one break nontrial row |
| 70 | `mainLoop.trialKey.keys` | PsychoPy automatic (`mainLoop.trialKey`) | key response copied into experimental loop | f / j / space / None | 96 experimental trials |
| 71 | `mainLoop.trialKey.rt` | PsychoPy automatic (`mainLoop.trialKey`) | RT copied into experimental loop | seconds or None | 96 experimental trials |
| 72 | `mainLoop.trialKey.duration` | PsychoPy automatic (`mainLoop.trialKey`) | keypress duration copied into experimental loop | seconds or None | 96 experimental trials |
| 73 | `endScreen.started` | PsychoPy automatic | End-screen routine start (routine/CPU timestamp, not necessarily flip) | seconds on global clock | final nontrial row |
| 74 | `endText.started` | PsychoPy automatic (`endText`) | endText: onset scheduled on `win.flip()` | seconds on global clock | final nontrial row |
| 75 | `endText.stopped` | PsychoPy automatic (`endText`) | endText: offset scheduled on `win.flip()` | seconds on global clock | final nontrial row |
| 76 | `endScreen.stopped` | PsychoPy automatic | End-screen routine end (routine/CPU timestamp, not necessarily flip) | seconds on global clock | final nontrial row |
| 77 | `participant` (second occurrence; `participant__copy2` in audit only) | startup dialog | Second raw `participant` column: ID entered in startup dialog (name normalized to `participant__copy2` by audit script) | integer ID | all 107 output rows (replicated experiment metadata) |
| 78 | `session` | startup dialog | Session entered in startup dialog | string, e.g. 001 | all 107 output rows (replicated experiment metadata) |
| 79 | `date` | PsychoPy automatic | PsychoPy session date/time stamp | timestamp text | all 107 output rows (replicated experiment metadata) |
| 80 | `expName` | PsychoPy automatic | Experiment name | ldt | all 107 output rows (replicated experiment metadata) |
| 81 | `expVersion` | PsychoPy automatic | Experiment version string (empty in current run) | string / blank | all 107 output rows (replicated experiment metadata) |
| 82 | `psychopyVersion` | PsychoPy automatic | PsychoPy version | version string; 2026.2.4 | all 107 output rows (replicated experiment metadata) |
| 83 | `frameRate` | PsychoPy automatic + `instructionCode` | Rounded measured display refresh rate saved to extraInfo | Hz, integer | all 107 output rows (replicated experiment metadata) |
| 84 | `expStart` | PsychoPy automatic | Experiment start wall-clock time | timestamp with UTC offset | all 107 output rows (replicated experiment metadata) |
| 85 | *(empty header)* | PsychoPy automatic | Trailing unnamed CSV column emitted by PsychoPy; no measurement stored | blank | all 107 rows; blank |

## Separate instrumentation log — I1

**File name pattern:** `data/<participant>_ldt_<timestamp>_frameIntervals.log`. Generated by the **`a6SessionFrameCode` End Experiment** hook via `win.saveFrameIntervals(...)`. Each comma-separated number is the elapsed interval **in seconds** between successive recorded `win.flip()` calls. The recording is enabled in **`a6FrameCode` Begin Routine** for trial routines and disabled in **End Routine**; therefore it excludes the instructions, feedback, ITI, break and end-screen routines. PsychoPy omits the first interval after recording starts so the preceding display is not erroneously counted. These are software flip intervals, not physical display-light measurements.

**I2 reconciliation:** `dropped_frames` (CSV column 43) is the per-trial difference in `win.nDroppedFrames`, with `win.refreshThreshold = 1.5 * frameDur`. Across all trial rows, the sum must equal the number of I1 log intervals strictly greater than `1.5 / frameRate` seconds. For participant 7 both counts were **0**; for participant 8 both were **1**. The uninstrumented participant 3 and 6 files do not have this column/log and are correctly `UNDETERMINED` for I1/I2.

## Source and row notes

- **Trial list:** `trial_lists/trials_pNN.csv`; 10 content columns replicated into the output. The list-side participant column appears on all rows as exported metadata.
- **Startup dialog:** participant number and session; automatic `date`, `expName`, etc. are added as experiment metadata.
- **Code component:** `instructionCode` calculates the rounded frame rate; `trialRecordCode` creates the derived response and text/onset fields; `a6FrameCode` creates per-trial `dropped_frames`; `a6SessionFrameCode` writes the separate I1 log.
- **PsychoPy automatic:** routine and stimulus timestamps, keyboard raw values, trial indexes, loop indexes, status fields, and metadata; many are blank on rows unrelated to their routine.
