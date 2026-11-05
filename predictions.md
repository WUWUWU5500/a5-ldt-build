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

1.

2.

3.

4.

5.

## Reconciliation

For each prediction: what you got, and if it differs, why. "I was wrong" is
not a reason. Name the mechanism: what PsychoPy, your build, or your machine
did that you did not expect.

1.

2.

3.

4.

5.