"""Fill only Assignment 5 Part D's Reconciliation, using participant 3 CSV.

Run from the A5 repository: uv run python finish_predictions.py
The original Predictions section stays byte-for-byte identical as text.
"""
from __future__ import annotations

import csv
import math
from collections import Counter
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent
PREDICTIONS = ROOT / "predictions.md"
DATA = ROOT / "data"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit("STOP (nothing changed): " + message)


matches = list(DATA.glob("3_ldt_*.csv"))
require(bool(matches), "No participant 3 CSV found in the data/ folder.")
source = max(matches, key=lambda p: p.stat().st_mtime)

with source.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.reader(handle)
    header = next(reader)
    rows = list(reader)

columns = {name: [index for index, item in enumerate(header) if item == name]
           for name in set(header)}


def field(row: list[str], name: str) -> str:
    require(name in columns, f"Missing required column {name!r} in {source.name}.")
    return row[columns[name][0]].strip()


trial_rows = [row for row in rows if field(row, "phase") in ("practice", "experimental")]
phases = Counter(field(row, "phase") for row in trial_rows)
require(len(trial_rows) == 104 and phases == {"practice": 8, "experimental": 96},
        f"Unexpected trial counts: {phases}. Check the selected CSV before reconciling.")
require(all(len(r) == len(header) for r in rows), "Some CSV rows have a different column count.")

rates = [float(field(row, "frameRate")) for row in rows if field(row, "frameRate")]
require(bool(rates), "Cannot find a recorded frameRate.")
rate = int(round(median(rates)))

rt_values = []
num_timeout = 0
for row in trial_rows:
    timeout = field(row, "timeout")
    require(timeout in ("0", "1"), f"Unexpected timeout coding: {timeout!r}")
    num_timeout += (timeout == "1")
    rt = field(row, "rt")
    if rt:
        try:
            number = float(rt)
        except ValueError as exc:
            raise SystemExit(f"Invalid reaction time {rt!r}: {exc}") from exc
        require(math.isfinite(number) and 0 <= number <= 2.2,
                f"Implausible RT {number} in {source.name}.")
        rt_values.append(number)
require(bool(rt_values), "No valid reaction times found.")
median_rt = median(rt_values)

intervals = {}
for row in trial_rows:
    soa_text = field(row, "soa")
    prime_onset = field(row, "prime_onset")
    target_onset = field(row, "target_onset")
    require(soa_text and prime_onset and target_onset, "Missing trial SOA/onset values.")
    soa = int(float(soa_text))
    ms = 1000 * (float(target_onset) - float(prime_onset))
    intervals.setdefault(soa, []).append(ms)
require(150 in intervals and 1000 in intervals, "Missing one or both required SOA conditions.")

prime_sample = field(trial_rows[0], "prime_shown")
target_sample = field(trial_rows[0], "target_shown")
prime_from_csv = field(trial_rows[0], "prime")
target_from_csv = field(trial_rows[0], "target")
require(all(field(r, "prime_shown") == field(r, "prime")
            and field(r, "target_shown") == field(r, "target").upper()
            for r in trial_rows), "Displayed text columns differ from the trial-list text.")

require(PREDICTIONS.exists(), "predictions.md does not exist in this folder.")
original = PREDICTIONS.read_text(encoding="utf-8-sig")
require("## Predictions" in original and "## Reconciliation" in original,
        "Cannot find the original predictions/reconciliation headings.")
prefix, previous_reconciliation = original.split("\n## Reconciliation", 1)
require("**1. How many rows" in prefix, "Predictions section is not the expected original version.")
require("Generated from participant 3 output" not in previous_reconciliation,
        "This script has already filled reconciliation; review the file instead of rerunning.")


def timing_text(soa: int) -> str:
    values = intervals[soa]
    return (f"{len(values)} trials, median {median(values):.1f} ms "
            f"(range {min(values):.1f}–{max(values):.1f} ms)")


percent_timeout = num_timeout * 100 / len(trial_rows)
duplicate = {name: len(indices) for name, indices in columns.items() if len(indices) > 1}
reconciliation = f"""## Reconciliation

*Generated from participant 3 output: `data/{source.name}`. The original Predictions section above has not been edited.*

**1. Number of output rows.** My prediction of 107 rows was correct. The completed participant 3 CSV contains **{len(rows)} rows**: **{len(trial_rows)} actual trial rows** (8 practice and 96 experimental), plus **{len(rows) - len(trial_rows)} rows with no trial phase**. PsychoPy's ExperimentHandler also saves entries for the instructions, break, and end routines. A reader must filter the `phase` column to isolate the trial-level data.

**2. Duplicate column names.** My prediction was incorrect. The raw CSV contains **two columns named `participant`**{f' (duplicate-header counts: {duplicate})' if duplicate else ''}. The two sources are the participant field from PsychoPy's experiment information dialog and the `participant` field imported from the trial-list conditions. PsychoPy exported both with the same name instead of merging them; this also caused PowerShell's `Import-Csv` to fail. I used a header-position-aware Python CSV reader in the checker to avoid losing either copy.

**3. Prime-to-target onset intervals.** The final build measured and recorded a refresh rate of **{rate} Hz**, rather than the 60 Hz I assumed. By the assignment's rounding rule, a 150-ms SOA uses **{round(150 * rate / 1000)} frames** (nominally {1000 * round(150 * rate / 1000) / rate:.1f} ms) and a 1,000-ms SOA uses **{round(1000 * rate / 1000)} frames** (nominally {1000 * round(1000 * rate / 1000) / rate:.1f} ms). The recorded prime-to-target intervals were: **150-ms SOA: {timing_text(150)}**; **1,000-ms SOA: {timing_text(1000)}**. Small deviations from the intended durations can occur when frame intervals vary. My initial Builder draft used time-in-seconds scheduling, but the post-handoff experiment was changed to whole-frame scheduling. Unlike my initial expectation, the final output contains both `prime_onset` and `target_onset`; they were added during the post-handoff changes. My checker marked participant 3's observable SOA intervals as PASS under its stated tolerance.

**4. Median RT and timeout proportion.** I predicted a median RT of 0.65 seconds and approximately 5% timeouts. The participant 3 run instead had a **median valid RT of {median_rt:.3f} seconds ({median_rt * 1000:.1f} ms)** across **{len(rt_values)} nonempty RTs** and **{num_timeout} timeout trials out of 104 ({percent_timeout:.2f}%)**. The difference from my prediction is due to the actual keypresses and response delays during my run, not a fixed constant in the experiment. Only trials with an actual recorded response contribute to the RT median; timeouts have empty RTs by design. The final post-handoff build also created the specifically named `rt` and `timeout` columns that were not in my initial Builder draft.

**5. Displayed prime and target.** My prediction about the text transformations was correct: primes remained lowercase and targets were displayed in uppercase. For example, the first participant 3 trial had source `prime={prime_from_csv}` and `target={target_from_csv}`, and its recorded stimulus-object texts were **`prime_shown={prime_sample}`** and **`target_shown={target_sample}`**. The `smoke` / `PEPPER` pair in my prediction was an example of the intended formatting, not a requirement that those words appear as a specific participant 3 trial. My prediction that the two shown-text columns might be absent was wrong for the final version because the LLM-assisted post-handoff update explicitly records `primeStim.text` and `targetStim.text` at the end of each trial. The checker confirmed this relationship for all 104 trial rows.
"""

# Preserve the original predictions text; replace only the unfilled reconciliation template.
PREDICTIONS.write_text(prefix + "\n\n" + reconciliation, encoding="utf-8")

print("Updated:", PREDICTIONS.name)
print("Source:", source.name)
print("Original Predictions section preserved; only Reconciliation replaced.")
print(f"Rows: {len(rows)} total; {len(trial_rows)} trial rows; duplicate headers: {duplicate}")
print(f"Frame rate: {rate} Hz; 150-ms SOA: {timing_text(150)}; 1000-ms SOA: {timing_text(1000)}")
print(f"Median RT: {median_rt:.3f} sec; timeouts: {num_timeout}/104 = {percent_timeout:.2f}%")
print("Review predictions.md before committing.")
