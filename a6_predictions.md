# Predictions (Part A)

These predictions are based on the Assignment 5 results already recorded in my repository and my understanding of the Builder experiment. I have not run any new Assignment 6 checks. The reconciliation will go in `a6_report.md`; I will leave these predictions unchanged after committing them.

## The six provided files

**Legend:** `PASS` / `FAIL` refers to what I expect the CSV to establish. `UNDETERMINED` means that the file alone does not settle the stated part, even if its recorded values look plausible.

| Property | A | B | C | D | E | F |
| --- | --- | --- | --- | --- | --- | --- |
| **Q3** Sequence | PASS trial-phase order; UNDETERMINED instructions, feedback shown, break/end behavior | PASS order; UNDETERMINED screen behavior | PASS order; UNDETERMINED screen behavior | PASS order; UNDETERMINED screen behavior | PASS practice-before-experimental; UNDETERMINED screen behavior | PASS order; UNDETERMINED screen behavior |
| **Q4** Stimuli and SOA | PASS recorded SOA; UNDETERMINED actual display/target cutoff | PASS SOA; UNDETERMINED display | PASS SOA; UNDETERMINED display | PASS SOA; UNDETERMINED display | PASS SOA; UNDETERMINED display | PASS SOA; UNDETERMINED display |
| **Q5** Frame timing | PASS rounded 60 Hz and recorded frame-grid intervals; UNDETERMINED whether Builder specified *all* durations in frames | PASS rate/grid; UNDETERMINED implementation | PASS rate/grid; UNDETERMINED implementation | PASS rate/grid; UNDETERMINED implementation | PASS rate/grid; UNDETERMINED implementation | PASS rate/grid; UNDETERMINED implementation |
| **Q6** Keys | PASS recorded keys limited to f/j/blank; UNDETERMINED ignoring other keys, Escape, and displayed mapping | PASS valid keys; UNDETERMINED key handling | PASS; UNDETERMINED key handling | PASS; UNDETERMINED key handling | PASS; UNDETERMINED key handling | PASS; UNDETERMINED key handling |
| **Q7** Response window | PASS logged keyboard/target starts; UNDETERMINED whether clock truly reset on flip | PASS starts; UNDETERMINED clock/early-key handling | PASS starts; UNDETERMINED clock/early-key handling | PASS starts; UNDETERMINED clock/early-key handling | PASS starts; UNDETERMINED clock/early-key handling | **FAIL** keyboard starts before target; UNDETERMINED clock/early-key handling |
| **Q8** Shown text | PASS text values; UNDETERMINED whether read from visual objects | PASS values; UNDETERMINED source | PASS values; UNDETERMINED source | **FAIL** shown prime values; UNDETERMINED source | PASS values; UNDETERMINED source | PASS values; UNDETERMINED source |
| **Q9** Onsets | PASS if recorded onset fields agree with matching stimulus `.started` fields; UNDETERMINED actual light onset | PASS internal fields; UNDETERMINED physical onset | PASS internal fields; UNDETERMINED physical onset | PASS internal fields; UNDETERMINED physical onset | PASS internal fields; UNDETERMINED physical onset | PASS internal fields; UNDETERMINED physical onset |
| **Q10** Coding | **FAIL** accuracy coding; PASS fields present | PASS response coding/fields | PASS response coding/fields | PASS response coding/fields | PASS response coding/fields | PASS response coding/fields |

**1. Properties expected to remain UNDETERMINED.** A CSV cannot prove which instructions, feedback, break, or final screen actually appeared (Q3), what the participant physically saw on the display (Q4), whether Builder used frame counts rather than time conditions (Q5), whether irrelevant keys were ignored or Escape worked (Q6), whether the keyboard clock reset exactly on the target flip or rejected early presses (Q7), whether shown-text fields were read from the actual TextStim objects (Q8), or the physical light onset of the stimuli (Q9). Inspecting the original Builder script, direct piloting, and/or hardware timing measurements would settle different parts of these questions.

**2. Failures among files that passed Q1–Q2 in A5.** I predict **three** such files will fail at least one observable Q3–Q10 check: **A** (Q10), **D** (Q8), and **F** (Q7). B should pass all measurable checks. E failed Q2 already; C failed Q1 and Q2 already.

## Your own build

**3. Refresh rate and required frame counts.** I predict the machine will measure approximately **60 Hz**, as in my earlier participant 6 run (though participant 3 recorded 61 Hz). At exactly 60 Hz, Q5 requires fixation **30 frames** (500 ms); prime **9 frames** (150 ms); SOA 150 **9 frames**; SOA 1000 **60 frames**; ITI **30 frames** (500 ms); practice feedback **60 frames** (1000 ms); and final screen **120 frames** (2000 ms). These are SOAs from **prime onset**, not from the trial beginning. If the measured rounded rate is 61 Hz instead, the corresponding rounded counts are 30, 9, 9, 61, 30, 61, and 122 frames.

**4. Expected Q3–Q10 failures in my tagged A5 build.** I expect the recorded trial structure, keys, text fields, onset fields, and response coding to pass most checks. I expect **at least one Q4 timing exception** in participant 6, because the A5 checker already reported trial 26 at approximately 1048 ms instead of 1000 ms. I am least sure about physical frame delivery and whether the target timeout is accurate on a dropped-frame trial. The duplicated `participant` header is also an output usability issue, even though the original trial-list values were preserved.

**5. Dropped frames in instrumented runs.** I predict **2 total dropped frames** in the quiet participant 7 run and **12 total dropped frames** with a muted browser video playing for participant 8. I expect the video to create more contention, especially around the prime-to-target interval or during target presentation. These are specific estimates to compare with the I1 log and the `dropped_frames` totals, not guaranteed outcomes.

**6. If a frame drops during the prime.** With my build's frame-number-based stimulus timing, the prime will stay visible **longer in elapsed milliseconds**, although its scheduled number of frames remains the same. The prime-onset-to-target-onset SOA will also become longer in elapsed time if that delayed flip lies within the SOA interval.

**7. Limits of software timing evidence.** Software timestamps can verify (i) the logged interval from fixation onset to prime onset, (ii) the logged prime-to-target SOA, and (iii) whether the keyboard component starts on the same recorded flip as the target. They can **bound but not prove** the actual visible prime duration, because refresh timestamps may not equal photon timing. Without external hardware such as a photodiode, they **cannot measure the physical light-onset time at the display**.
