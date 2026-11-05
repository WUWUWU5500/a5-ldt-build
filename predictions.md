# Predictions and reconciliation (Part D)

Fill in **Predictions** before your first complete run, and commit this file
with a message that starts `predictions:`. Do not edit the Predictions
section after that commit; the history is how it is read. Then run the
experiment and fill in **Reconciliation**.

You are graded on the reconciliation, not on being right.

## Predictions

Answer for your own build, as participant 3.

## Predictions

**1. How many rows will the output file have?**

I predict 107 rows: 104 trial rows (8 practice and 96 experimental), plus  3 nontrial rows associated with the instructions, break, and end screens. 

**2. Will any column name appear more than once?**

I predict that no column names will be duplicated exactly. The practice and experimental loops use the same trial-list columns, but I expect PsychoPy to use shared column names for both. 
**3. What will the prime-to-target onset intervals be?**

Assuming my computer runs at 60 Hz:

- SOA 150: approximately 150 ms, or 9 frames.
- SOA 1000: approximately 1000 ms, or 60 frames.

My current Builder version schedules these events in seconds rather than explicitly counting frames. Therefore, I expect small timing differences to be possible. I also predict that the current output may not contain the required `prime_onset` and `target_onset` columns.

**4. What will the median RT and timeout proportion be?**

I predict a median reaction time of approximately 0.65 seconds (650 ms), with about 5% of trials resulting in timeouts. My current Builder version records keyboard reaction times through `trialKey.rt`, rather than the required `rt` column.

**5. What will `prime_shown` and `target_shown` contain?**

For a trial with prime `smoke` and target `pepper`, I predict that the experiment will display:

- Prime: `smoke`
- Target: `PEPPER`

However, the current Builder version does not yet explicitly save `prime_shown` and `target_shown`. I therefore predict these columns may be absent.


## Reconciliation

*Generated from participant 3 output: `data/3_ldt_2026-11-04_21h40.50.643.csv`. The original Predictions section above has not been edited.*

**1. Number of output rows.** My prediction was correct. The output contained 107 rows: 104 trials (8 practice and 96 experimental) and 3 nontrial rows for instructions, break, and end screens.

**2. Duplicate column names.** My prediction was incorrect. The participant column appeared twice because PsychoPy saved it from both the participant dialog and the trial list.

**3. Prime-to-target onset intervals.** The final build measured and recorded a refresh rate of **61 Hz**, rather than the 60 Hz I assumed. By the assignment's rounding rule, a 150-ms SOA uses **9 frames** (nominally 147.5 ms) and a 1,000-ms SOA uses **61 frames** (nominally 1000.0 ms). The recorded prime-to-target intervals were: **150-ms SOA: 52 trials, median 150.1 ms (range 148.4–152.0 ms)**; **1,000-ms SOA: 52 trials, median 1016.1 ms (range 1014.1–1018.2 ms)**. Small deviations from the intended durations can occur when frame intervals vary. My initial Builder draft used time-in-seconds scheduling, but the post-handoff experiment was changed to whole-frame scheduling. Unlike my initial expectation, the final output contains both `prime_onset` and `target_onset`; they were added during the post-handoff changes. My checker marked participant 3's observable SOA intervals as PASS under its stated tolerance.

**4. Median RT and timeout proportion.** I predicted a median RT of 0.65 seconds and 5% timeouts. The actual median RT was 0.085 seconds, with 0% timeouts. The unusually fast RTs may reflect anticipatory responses during my self-test. The final version recorded both rt and timeout.

**5. Displayed prime and target.** My prediction was correct: primes appeared in lowercase and targets in uppercase. For example, plane and PILOT. Unlike my initial prediction, the final version saved both prime_shown and target_shown after the LLM-assisted modifications.
