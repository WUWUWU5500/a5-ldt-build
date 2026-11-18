"""PSY 8683 Assignment 6: automated verification of lexical-decision outputs.

Preserves A5 Q1/Q2 checks, extends falsifiable Q3-Q10 checks, and adds I1/I2
frame-interval and dropped-frame checks for newly instrumented runs.

PASS/FAIL: settled by the available data. UNDETERMINED: the data cannot settle
it and the output says what additional evidence would. PILOT is reserved for
checks actually established from direct observation / reading the build; the
CSV-only checker does not label something PILOT automatically.

Commands (run in the repository root):
  uv run --python 3.11 python check_output.py data/3_ldt_*.csv data/6_ldt_*.csv
  uv run --python 3.11 python check_output.py data/7_ldt_*.csv data/8_ldt_*.csv
  uv run --python 3.11 python check_output.py provided/output_files/*.csv --lists provided/canonical_trial_lists

Standard library only. Supports duplicate PsychoPy CSV column names.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

TRIAL_COLUMNS = (
    "participant", "phase", "trial_index", "item_id", "target", "prime",
    "relatedness", "soa", "correct_response", "seed",
)
CONTENT_COLUMNS = tuple(c for c in TRIAL_COLUMNS if c != "participant")


@dataclass
class Output:
    path: Path
    header: list[str]
    rows: list[list[str]]

    def positions(self, name: str) -> list[int]:
        return [i for i, col in enumerate(self.header) if col == name]

    def get(self, row: list[str], name: str, copy: int = 0) -> str:
        positions = self.positions(name)
        if not positions:
            return ""
        i = positions[copy] if copy >= 0 and copy < len(positions) else positions[-1]
        return row[i].strip() if i < len(row) else ""

    def has(self, *names: str) -> bool:
        return all(self.positions(n) for n in names)

    @property
    def trials(self) -> list[list[str]]:
        return [r for r in self.rows if self.get(r, "phase") in ("practice", "experimental")]

    @property
    def extras(self) -> list[list[str]]:
        return [r for r in self.rows if self.get(r, "phase") not in ("practice", "experimental")]

    def dialog_id(self) -> tuple[int | None, str]:
        # PsychoPy's TrialHandler appends a trial-list participant column near
        # the start, while ExperimentHandler appends the startup-dialog value
        # toward the right of the CSV (often creating a duplicate name).
        cols = self.positions("participant")
        if len(cols) < 2:
            return None, "startup-dialog participant cannot be distinguished from trial-list participant"
        values = {self.get(row, "participant", copy=len(cols)-1) for row in self.rows}
        values.discard("")
        if len(values) != 1:
            return None, f"startup participant values are not unique: {sorted(values)}"
        value = next(iter(values))
        try:
            p = int(value)
            return p, f"startup-dialog participant={p} (rightmost participant column)"
        except ValueError:
            return None, f"startup-dialog participant is not numeric: {value!r}"


def read_output(path: str | Path) -> Output:
    path = Path(path)
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = csv.reader(f)
        try:
            header = next(rows)
        except StopIteration:
            raise ValueError(f"Empty CSV: {path}")
        data = list(rows)
    widths = Counter(len(r) for r in data)
    if len(widths) > 1 or (widths and len(header) not in widths):
        raise ValueError(f"Malformed CSV {path}: header has {len(header)} columns, row widths {dict(widths)}")
    return Output(path=path, header=header, rows=data)


def get_list_path(lists_dir: str | Path, p: int) -> Path:
    return Path(lists_dir) / f"trials_p{p:02d}.csv"


def load_list(lists_dir: str | Path, p: int) -> list[dict[str, str]]:
    path = get_list_path(lists_dir, p)
    with path.open(encoding="utf-8-sig", newline="") as f:
        records = list(csv.DictReader(f))
    return [{k: (v or "").strip() for k, v in row.items() if k is not None} for row in records]


def canon(value: Any) -> str:
    # Avoid false differences when a numeric integer is displayed as '150.0'.
    s = str(value).strip()
    if s and s.lstrip("-+").replace(".", "", 1).isdigit() and "." in s:
        try:
            n = float(s)
            if n.is_integer():
                return str(int(n))
        except ValueError:
            pass
    return s


def signature_dict(row: dict[str, str], cols: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(canon(row.get(k, "")) for k in cols)


def signature_output(output: Output, row: list[str], cols: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(canon(output.get(row, k)) for k in cols)


def identifying(row: dict[str, str] | None) -> str:
    if row is None:
        return "[missing]"
    return f"{row.get('phase','')}/{row.get('trial_index','')} {row.get('item_id','')} {row.get('prime','')}->{row.get('target','')}"


def as_dict(output: Output, row: list[str]) -> dict[str, str]:
    return {col: output.get(row, col) for col in TRIAL_COLUMNS}


def check_q1(output: Output, lists_dir: str) -> tuple[str, str]:
    """Was the correct participant-specific list used?"""
    p, origin = output.dialog_id()
    if p is None:
        return "UNDETERMINED", f"Cannot establish dialog participant independently: {origin}. Inspect dialog/run metadata."
    path = get_list_path(lists_dir, p)
    if not path.exists():
        return "FAIL", f"{origin}; expected file absent: {path}"
    if not output.has(*CONTENT_COLUMNS):
        missing = [c for c in CONTENT_COLUMNS if not output.has(c)]
        return "FAIL", f"{origin}; output lacks trial-list fields: {missing}"
    expected = load_list(lists_dir, p)
    observed = Counter(signature_output(output, r, CONTENT_COLUMNS) for r in output.trials)
    intended = Counter(signature_dict(row, CONTENT_COLUMNS) for row in expected)
    if observed == intended:
        return "PASS", f"{origin}; all {len(expected)} condition rows match {path} as a multiset (order checked separately in Q2)."
    missing = sum((intended - observed).values())
    extra = sum((observed - intended).values())
    alt = []
    for other in sorted(Path(lists_dir).glob("trials_p*.csv")):
        try:
            q = int(other.stem.split("p")[-1])
            if q != p and Counter(signature_dict(r, CONTENT_COLUMNS) for r in load_list(lists_dir, q)) == observed:
                alt.append(q)
        except (ValueError, KeyError, OSError):
            continue
    note = f"; rows exactly match other participant list(s) {alt}" if alt else ""
    return "FAIL", f"{origin}; content differs from {path.name}: {missing} missing and {extra} unexpected condition rows{note}."


def check_q2(output: Output, lists_dir: str) -> tuple[str, str]:
    """Did every trial-list row run exactly once, in list order?"""
    p, origin = output.dialog_id()
    if p is None:
        return "UNDETERMINED", f"Cannot prove participant's intended trial order: {origin}."
    path = get_list_path(lists_dir, p)
    if not path.exists():
        return "FAIL", f"Cannot compare trial order: missing {path}."
    missing_cols = [c for c in TRIAL_COLUMNS if not output.has(c)]
    if missing_cols:
        return "FAIL", f"Missing trial-list columns {missing_cols}."
    expected = load_list(lists_dir, p)
    observed = [signature_output(output, row, TRIAL_COLUMNS) for row in output.trials]
    wanted = [signature_dict(row, TRIAL_COLUMNS) for row in expected]
    if observed == wanted:
        phases = Counter(output.get(row, "phase") for row in output.trials)
        return "PASS", f"Exactly {len(wanted)} rows in exact list order ({phases['practice']} practice, {phases['experimental']} experimental); {len(output.extras)} nontrial rows excluded."
    for i in range(max(len(wanted), len(observed))):
        a = observed[i] if i < len(observed) else None
        e = wanted[i] if i < len(wanted) else None
        if a != e:
            a_text = identifying(as_dict(output, output.trials[i])) if i < len(observed) else "[missing]"
            e_text = identifying(expected[i]) if i < len(wanted) else "[none expected]"
            return "FAIL", f"{len(observed)} trial rows vs {len(wanted)} expected; first difference at position {i+1}: expected {e_text}; actual {a_text}."
    return "FAIL", "Trial sequence differs."


def check_q3(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    """Q3: recorded practice->main sequence, not undocumented visual behavior."""
    phase = [output.get(r, "phase") for r in output.trials]
    wanted = ["practice"] * 8 + ["experimental"] * 96
    if phase == wanted:
        sequence = ("PASS", "104 trial rows: 8 practice first, then 96 experimental, in recorded order.")
    else:
        sequence = ("FAIL", f"Expected 8 practice then 96 main; observed phases {dict(Counter(phase))}; first 12={phase[:12]!r}.")
    display = ("UNDETERMINED", "Trial CSV cannot prove instruction text, SPACE gating, feedback visibility, break behavior, or final 2-s display. Inspect Builder and watch a complete run; hardware is needed for physical durations.")
    return [sequence, display]


def num(output: Output, row: list[str], name: str) -> float | None:
    try:
        value = output.get(row, name)
        return float(value) if value != "" else None
    except ValueError:
        return None


def _rounded_hz(output: Output) -> int | None:
    """A single positive integer refresh rate shared by trial rows."""
    vals = {num(output, row, "frameRate") for row in output.trials}
    if len(vals) != 1 or None in vals:
        return None
    value = next(iter(vals))
    if value <= 0 or not value.is_integer():
        return None
    return int(value)


def _drop_context(output: Output, row: list[str], inside_trial: bool) -> str:
    """A per-trial drop flags a *possible*, not demonstrated, local cause."""
    if not inside_trial:
        return "outside I1/I2 trial recording; no local frame-drop inference"
    drops = num(output, row, "dropped_frames")
    if drops is None:
        return "I2 not recorded; mechanism unknown"
    if drops < 0 or not drops.is_integer():
        return "invalid I2 value; mechanism unknown"
    if drops > 0:
        return f"I2={int(drops)} on trial (possible delayed flip, not localized to this event)"
    return "I2=0 on trial (no logged >1.5-frame interval)"


def _estimated_cadence(output: Output, nominal_hz: int) -> float:
    """Estimate actual flip period robustly from repeated screen timestamps.

    PsychoPy sometimes rounds its screen-rate *estimate* to 61 while the
    physical refresh is 60 Hz. Using 1/61 for judging 61 scheduled frames
    would wrongly call a correct ~1016.7 ms interval a 62-frame failure.
    Anchor the cadence on multiple event types so one systematically wrong
    stimulus duration cannot simply define its own expected frame period.
    """
    import statistics
    ratios = []
    for names, expected_ms in (
        (("fixation", "fixation_text", "fixText"), 500),
        (("primeStim", "prime_text", "primeText", "prime_stim"), 150),
    ):
        base = next((n for n in names if output.has(f"{n}.started", f"{n}.stopped")), None)
        if base:
            expected = round(expected_ms * nominal_hz / 1000)
            for row in output.trials:
                start = num(output, row, f"{base}.started")
                stop = num(output, row, f"{base}.stopped")
                if start is not None and stop is not None and stop > start:
                    ratios.append((stop-start)/expected)
    if output.has("prime_onset", "target_onset", "soa"):
        for row in output.trials:
            p = num(output, row, "prime_onset")
            t = num(output, row, "target_onset")
            soa = num(output, row, "soa")
            if p is not None and t is not None and soa is not None and t > p:
                frames = round(soa * nominal_hz / 1000)
                if frames > 0:
                    ratios.append((t-p)/frames)
    # Many independent timestamp samples are required before estimating
    # a cadence different from nominal; otherwise fall back conservatively.
    return statistics.median(ratios) if len(ratios) >= 10 else 1 / nominal_hz


def _frame_duration_check(
    output: Output,
    label: str,
    rows: list[list[str]],
    start_col: str,
    stop_col: str,
    expected_ms: int | None,
    inside_trial: bool,
) -> tuple[str, str]:
    """Compare measured timestamp intervals with scheduled integer frames.

    A 1-frame excess is not silently forgiven by a broad 35-ms window.
    For each anomaly we distinguish whether a drop was recorded *somewhere*
    in that trial, but do not infer which interval it affected.
    """
    if not output.has(start_col, stop_col):
        return "UNDETERMINED", f"{label}: cannot find {start_col}/{stop_col}; check Builder component names."
    hz = _rounded_hz(output)
    if hz is None:
        return "UNDETERMINED", f"{label}: no unique positive whole-number frameRate for frame-count comparison."
    if not rows:
        return "UNDETERMINED", f"{label}: no relevant rows."

    cadence = _estimated_cadence(output, hz)
    errors = []
    for i, row in enumerate(rows, 1):
        start, stop = num(output, row, start_col), num(output, row, stop_col)
        if start is None or stop is None or stop <= start:
            errors.append(f"row {i}: missing/nonpositive software timestamps")
            continue
        specified = expected_ms if expected_ms is not None else num(output, row, "soa")
        if specified is None:
            errors.append(f"row {i}: missing expected duration")
            continue
        expected_frames = round(float(specified) * hz / 1000)
        measured_ms = (stop - start) * 1000
        measured_frames = round((stop - start) / cadence)
        # Allow modest PsychoPy timestamp jitter (< 3/4 frame) rather than
        # classifying borderline 9-ms refresh estimates as a whole missed
        # physical frame. One full 16.7-ms period still fails.
        expected_seconds = expected_frames * cadence
        if abs((stop - start) - expected_seconds) > 0.75 * cadence:
            # A missed frame is an observed delivery deviation even if caused by
            # the machine rather than an erroneous Builder frame specification.
            context = _drop_context(output, row, inside_trial)
            errors.append(
                f"row {i}: measured {measured_frames} vs expected {expected_frames} "
                f"frame-equivalents ({measured_ms:.1f} ms, {context})"
            )

    if errors:
        return (
            "FAIL",
            f"{label}: {len(errors)}/{len(rows)} software frame-equivalent deviations; "
            f"first {errors[:4]}. A drop flag explains risk but does not prove the affected event."
        )
    return (
        "PASS",
        f"{label}: all {len(rows)} events match scheduled integer frame equivalents "
        f"using measured cadence ~{cadence*1000:.3f} ms, scheduled rate {hz} Hz "
        f"(software timestamp inference, not photodiode timing)."
    )


def _first_pair(output: Output, candidates: tuple[str, ...]) -> str | None:
    return next((n for n in candidates if output.has(f"{n}.started", f"{n}.stopped")), None)


def check_q4(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    """Frame-equivalent checks preserve drop-associated vs systematic failures."""
    results = [_frame_duration_check(
        output, "prime->target SOA", output.trials, "prime_onset", "target_onset",
        expected_ms=None, inside_trial=True,
    )]
    for label, duration, names in (
        ("fixation", 500, ("fixation", "fixation_text", "fixText")),
        ("prime", 150, ("primeStim", "prime_text", "primeText", "prime_stim")),
    ):
        name = _first_pair(output, names)
        results.append(_frame_duration_check(
            output, label, output.trials,
            f"{name}.started" if name else "<unknown>.started",
            f"{name}.stopped" if name else "<unknown>.stopped",
            expected_ms=duration, inside_trial=True,
        ))
    results.append((
        "UNDETERMINED",
        "Software timestamps cannot establish physical light onset, actual blank-gap "
        "visibility, or target cutoff; inspect Builder and/or use hardware timing."
    ))
    return results


def check_q5(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    """Test whole-Hz metadata and ALL output-observable fixed durations."""
    hz = _rounded_hz(output)
    raw = {output.get(row, "frameRate") for row in output.trials if output.get(row, "frameRate")}
    if hz is None:
        return [("FAIL" if raw else "UNDETERMINED",
                 f"No single positive rounded integer frameRate: {sorted(raw)}")]
    results = [("PASS", f"Recorded refresh rate is a positive rounded integer: {hz} Hz.")]

    for label, expected_ms, options, rows, in_trial in (
        ("inter-trial interval", 500, ("blankText", "blank", "itiText", "iti_text"), output.trials, False),
        ("practice feedback", 1000, ("feedbackText", "feedback_text", "feedbackTextStim"),
         [row for row in output.trials if output.get(row, "phase") == "practice"], False),
        ("end screen", 2000, ("endText", "end_text", "endTextStim"), output.extras, False),
    ):
        name = _first_pair(output, options)
        if name:
            matching_rows = [r for r in rows if output.get(r, f"{name}.started") or output.get(r, f"{name}.stopped")]
            results.append(_frame_duration_check(
                output, label, matching_rows, f"{name}.started", f"{name}.stopped",
                expected_ms=expected_ms, inside_trial=in_trial,
            ))
        else:
            results.append(("UNDETERMINED", f"{label}: no recognized component start/stop pair."))

    # Maximum target duration applies only to timeout rows. Earlier responses
    # terminate the routine and should not be treated as duration violations.
    name = _first_pair(output, ("targetStim", "target_text", "targetText", "target_stim"))
    timeout_rows = [r for r in output.trials if output.get(r, "timeout") in ("1", "1.0")]
    if timeout_rows:
        if name:
            results.append(_frame_duration_check(
                output, "target timeout window", timeout_rows,
                f"{name}.started", f"{name}.stopped", 2000, True,
            ))
        else:
            results.append(("UNDETERMINED", "target timeout window: no recognizable offset columns."))
    results.append(("UNDETERMINED",
        "CSV frame equivalents cannot prove that Builder specified every duration "
        "in frames or that the display emitted photons at those times."
    ))
    return results


def check_q6(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    """F/J only; response mapping crosschecked with accuracy in Q10."""
    if not output.has("key"):
        return [("UNDETERMINED", "The requested 'key' output is absent; verify accepted keys in Builder/Pilot.")]
    invalid = [(i,output.get(r,"key")) for i,r in enumerate(output.trials,1) if output.get(r,"key") not in ("", "f", "j")]
    observed = ("FAIL", f"Other key values recorded, first {invalid[:3]}.") if invalid else ("PASS", "All recorded trial responses are f, j, or empty (could fail if any other key was recorded).")
    return [observed, ("UNDETERMINED", "The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.")]


def check_q7(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    """Compare logged keyboard and target-onset refreshes where both exist.

    A5's initial blanket PILOT verdict missed a deliberately early keyboard
    onset in one example. Independently logged *.started columns permit a
    falsifiable CSV check instead of assuming all response windows are valid.
    """
    candidates = [
        ("targetStim.started", "trialKey.started"),
        ("target_text.started", "key_resp.started"),
        ("targetText.started", "key_resp.started"),
        ("target_text.started", "response.started"),
        ("targetStim.started", "key_resp.started"),
    ]
    pair = next(((target, kb) for target, kb in candidates
                 if output.has(target, kb)), None)
    if pair is None:
        return [("UNDETERMINED", "No recognizable target/keyboard component-start column pair. Inspect the CSV header/Builder component names and observe response gating in a Pilot.")]

    target_col, keyboard_col = pair
    bad = []
    for i, row in enumerate(output.trials, 1):
        target = num(output, row, target_col)
        keyboard = num(output, row, keyboard_col)
        if target is None or keyboard is None:
            bad.append(f"trial {i}: target or keyboard start timestamp missing")
        elif abs(keyboard - target) > 0.002:
            bad.append(f"trial {i}: keyboard starts {(keyboard-target)*1000:+.1f} ms relative to target")

    if bad:
        observed = ("FAIL", f"Keyboard onset differs from target onset on {len(bad)}/{len(output.trials)} trials; first {bad[:4]}.")
    else:
        observed = ("PASS", f"Keyboard and target start on the same logged refresh on all {len(output.trials)} trials ({keyboard_col} versus {target_col}; <=2 ms tolerance).")

    return [
        observed,
        ("UNDETERMINED", "Matching component-start timestamps alone cannot prove the keyboard RT clock was reset on that screen flip or that no earlier keystrokes leaked in; inspect generated code and test with intentionally early and late keys."),
    ]


def check_q8(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    if not output.has("prime_shown", "target_shown"):
        return [("FAIL", "prime_shown or target_shown missing from output CSV.")]
    bad = [(i,output.get(r,"prime_shown"),output.get(r,"target_shown")) for i,r in enumerate(output.trials,1) if output.get(r,"prime_shown") != output.get(r,"prime") or output.get(r,"target_shown") != output.get(r,"target").upper()]
    observed = ("FAIL", f"Displayed text fields mismatch the expected transformations; first {bad[:3]}.") if bad else ("PASS", "All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.")
    return [observed, ("UNDETERMINED", "CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.")]


def check_q9(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    """Q9: check explicit onset data against independent component-flip logs."""
    if not output.has("prime_onset", "target_onset"):
        return [("FAIL", "Required prime_onset or target_onset column absent from CSV.")]
    pairs = [
        ("primeStim.started", "targetStim.started"),
        ("prime_text.started", "target_text.started"),
        ("primeText.started", "targetText.started"),
        ("prime_stim.started", "target_stim.started"),
    ]
    pair = next((x for x in pairs if output.has(*x)), None)
    if pair is None:
        return [("UNDETERMINED", "Could not identify independently generated prime/target *.started timestamps. Need component-name mapping from Builder or an instrumented run, not an assumed PASS.")]
    start_p, start_t = pair
    problems = []
    for i, row in enumerate(output.trials, 1):
        p, p_ref = num(output, row, "prime_onset"), num(output, row, start_p)
        t, t_ref = num(output, row, "target_onset"), num(output, row, start_t)
        if None in (p, p_ref, t, t_ref) or abs(p-p_ref)>0.002 or abs(t-t_ref)>0.002:
            problems.append(i)
    if problems:
        return [("FAIL", f"Onset fields differ from {start_p}/{start_t} on {len(problems)} trial(s); first={problems[:5]}.")]
    return [
        ("PASS", f"Both custom onset fields match the {start_p}/{start_t} logged flip timestamps across {len(output.trials)} trials (2 ms tolerance)."),
        ("UNDETERMINED", "Software flip timestamps do not establish photon emission timing; a photodiode would be needed for physical onset."),
    ]


def check_q10(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    required = list(TRIAL_COLUMNS) + ["key","rt","accuracy","timeout"]
    missing = [c for c in required if not output.has(c)]
    structural = ("FAIL", f"Missing required columns: {missing}.") if missing else ("PASS", "All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.")
    if missing:
        return [structural]
    p, origin = output.dialog_id()
    if p is None:
        return [structural, ("UNDETERMINED", f"Could not check participant-dependent scoring: {origin}.")]
    errors=[]
    for i,row in enumerate(output.trials,1):
        key = output.get(row,"key")
        rt = output.get(row,"rt")
        acc = output.get(row,"accuracy")
        timeout = output.get(row,"timeout")
        correct = output.get(row,"correct_response")
        word_key = "f" if p % 2 else "j"
        expected = word_key if correct == "word" else ("j" if word_key=="f" else "f")
        wanted_acc = str(int(key==expected))
        wanted_timeout = str(int(key==""))
        if (acc,timeout)!=(wanted_acc,wanted_timeout) or (key=="" and rt!=""):
            errors.append(f"trial {i}: key={key!r},rt={rt!r},accuracy={acc!r},timeout={timeout!r}; expected accuracy={wanted_acc},timeout={wanted_timeout}")
        if rt:
            try:
                if not (0 <= float(rt) <= 2.1):
                    errors.append(f"trial {i}: RT {rt} outside 0..2.1 s")
            except ValueError:
                errors.append(f"trial {i}: nonnumeric RT {rt!r}")
    scoring = ("FAIL", f"{len(errors)} coding errors; first {errors[:2]}.") if errors else ("PASS", f"All {len(output.trials)} trials have internally consistent key/RT/accuracy/timeout for participant {p}.")
    duplicates = {k:n for k,n in Counter(output.header).items() if k and n > 1}
    if duplicates:
        header_result = ("UNDETERMINED", f"Duplicate header names {duplicates}; raw CSV preserves both, but import software may rename them. Confirm provenance in Builder.")
    else:
        header_result = ("PASS", "No duplicate nonempty CSV header names.")
    return [structural, scoring, header_result]



def instrumented_status(output: Output) -> bool:
    """An old A5 or provided output need not have I1/I2 instrumentation."""
    return output.has("dropped_frames") or output.path.with_name(output.path.stem + "_frameIntervals.log").exists()


def read_frame_log(path: Path) -> list[float]:
    """PsychoPy saveFrameIntervals() emits comma-separated floats in seconds."""
    import math
    text = path.read_text(encoding="utf-8-sig")
    values = []
    for raw in text.replace("\n", ",").split(","):
        if not raw.strip():
            continue
        value = float(raw.strip())
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"Nonpositive/nonfinite interval: {value!r}")
        values.append(value)
    return values


def frame_audit(output: Output) -> list[tuple[str, str, str]]:
    """Return I1/I2 verdicts, avoiding false failures for pre-I1 files."""
    log = output.path.with_name(output.path.stem + "_frameIntervals.log")
    if not instrumented_status(output):
        note = "This output predates I1/I2 or is provided without an instrumented build; need a new complete run with I1/I2 to audit frame delivery."
        return [("I1", "UNDETERMINED", note), ("I2", "UNDETERMINED", note)]

    if not log.is_file():
        return [("I1", "FAIL", f"Instrumented CSV has dropped_frames but no matching {log.name} file; a complete run must save it."),
                ("I2", "UNDETERMINED", "Cannot reconcile dropped_frames with independent log when I1 log is missing.")]
    try:
        intervals = read_frame_log(log)
    except (ValueError, OSError, UnicodeError) as exc:
        return [("I1", "FAIL", f"Could not parse {log.name}: {exc}"),
                ("I2", "UNDETERMINED", "No parseable I1 data to reconcile I2.")]
    if not intervals:
        return [("I1", "FAIL", "I1 log exists but records no flip intervals."),
                ("I2", "UNDETERMINED", "No intervals to compare with I2.")]

    hz_vals = {num(output, row, "frameRate") for row in output.trials}
    if len(hz_vals) != 1 or None in hz_vals or next(iter(hz_vals)) <= 0:
        return [("I1", "FAIL", f"Cannot establish a single valid recorded frameRate: {hz_vals}"),
                ("I2", "UNDETERMINED", "Drop threshold depends on known frameRate.")]
    hz = next(iter(hz_vals))
    threshold = 1.5 / round(hz)
    n_log = sum(value > threshold for value in intervals)
    sum_seconds = sum(intervals)
    n_trials = len(output.trials)
    total_screen_seconds = None
    if output.has("fixation.started", "trial.stopped"):
        durations = []
        for row in output.trials:
            a, b = num(output,row,"fixation.started"), num(output,row,"trial.stopped")
            if a is not None and b is not None and b >= a:
                durations.append(b-a)
        if len(durations) == n_trials:
            total_screen_seconds = sum(durations)

    if total_screen_seconds is None:
        plausible = "No complete fixation.started / trial.stopped pair; inspect whether intervals span only trial screens."
        i1_state = "UNDETERMINED"
    else:
        diff = abs(sum_seconds-total_screen_seconds)
        max_error = 3 * n_trials / round(hz)
        i1_state = "PASS" if diff <= max_error else "FAIL"
        plausible = f"trial-screen span={total_screen_seconds:.3f}s; difference={diff:.3f}s; tolerance={max_error:.3f}s"
    i1_msg = f"{len(intervals)} intervals, sum={sum_seconds:.3f}s, max={max(intervals)*1000:.2f}ms; {plausible}. Builder code intends to exclude feedback/ITI/instructions/break/end."

    if not output.has("dropped_frames"):
        return [("I1", i1_state, i1_msg), ("I2", "FAIL", "I1 log exists, but required per-trial dropped_frames column is missing.")]
    bad = []
    drops = []
    for i, row in enumerate(output.trials, 1):
        value = num(output,row,"dropped_frames")
        if value is None or not value.is_integer() or value < 0:
            bad.append((i, output.get(row,"dropped_frames")))
        else:
            drops.append(int(value))
    if bad:
        i2_state, i2_msg = "FAIL", f"Non-integer/negative/missing per-trial dropped_frames values: first {bad[:4]}"
    else:
        n_csv = sum(drops)
        i2_state = "PASS" if n_csv == n_log else "FAIL"
        i2_msg = f"per-trial CSV drops={n_csv}; logged intervals >{threshold*1000:.3f}ms={n_log}; {n_trials} trial rows."
    return [("I1", i1_state, i1_msg), ("I2", i2_state, i2_msg)]


def builder_evidence(output: Output, script: str | Path) -> list[tuple[str, str, str]]:
    """Optional direct Builder-code evidence; not inferred from a CSV.

    PILOT is only used when the supplied compiled experiment actually
    demonstrates the programmed behavior. Without this option, the checker
    cannot assert access to a build and leaves those portions UNDETERMINED.
    """
    source = Path(script)
    try:
        code = source.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return [("BUILD", "UNDETERMINED", f"Cannot inspect Builder script {source}: {exc}")]
    if not output.has("primeStim.started", "targetStim.started", "trialKey.started"):
        return [("BUILD", "UNDETERMINED", "This output does not use the provided own-build component family; do not apply unrelated Builder evidence.")]
    tests = (
        ("Q3", ("practiceLoop", "practiceFeedback", "breakScreen", "mainLoop", "endScreen"),
         "Generated Builder script establishes the programmed instructions/practice/feedback/break/main/end sequence; visible behavior was piloted separately."),
        ("Q5", ("fixFrames", "primeFrames", "soaFrames", "itiFrames", "feedbackFrames", "endFrames", "frameN >="),
         "Builder script schedules fixed events by integer frame numbers; physical presentation still requires separate evidence."),
        ("Q6", ("keyList=['f', 'j']", 'keyList=["escape"]'),
         "Builder code limits trial keys to F/J and checks Escape independently; the CSV cannot test every irrelevant key."),
        ("Q7", ("win.callOnFlip(trialKey.clock.reset)", "win.callOnFlip(trialKey.clearEvents"),
         "Builder code resets and clears the response device on the target flip."),
        ("Q8", ("str(primeStim.text)", "str(targetStim.text)"),
         "Shown stimulus strings are read from the live PsychoPy TextStim objects in the compiled Builder code."),
        ("Q9", ("primeStim.tStartRefresh", "targetStim.tStartRefresh"),
         "Custom onset values come from visual-object refresh timestamps, not arbitrary condition-string times."),
    )
    outcomes = []
    for q, markers, summary in tests:
        if all(marker in code for marker in markers):
            outcomes.append((q, "PILOT", summary))
        else:
            outcomes.append((q, "UNDETERMINED", "The supplied Builder script did not establish all required source-code features; inspect manually."))
    return outcomes


CHECKS = [check_q1, check_q2, check_q3, check_q4, check_q5,
          check_q6, check_q7, check_q8, check_q9, check_q10]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="+", help="CSV files")
    ap.add_argument("--lists", default="trial_lists", help="Folder of participant trial lists")
    ap.add_argument("--builder", default=None, help="Optional own-build compiled ldt.py for independent code inspection and PILOT verdicts")
    args = ap.parse_args()
    # PowerShell often passes wildcards literally to Python. Expand here so
    # the same command works on Windows and shells that expand *.csv for us.
    import glob
    files = []
    for spec in args.files:
        if any(ch in spec for ch in "*?["):
            matches = sorted(glob.glob(spec))
            if not matches:
                print(f"NO MATCH for {spec!r}")
            files.extend(matches)
        else:
            files.append(spec)
    if not files:
        print("No CSV files to check.")
        return 2
    for filepath in files:
        print("=" * 90)
        print(filepath)
        try:
            output = read_output(filepath)
        except (OSError, UnicodeError, ValueError, csv.Error) as exc:
            print(f"READ FAIL {exc}")
            continue
        print(f"ROWS: {len(output.rows)} total, {len(output.trials)} trials, {len(output.extras)} nontrial")
        for check in CHECKS:
            try:
                results = check(output, args.lists)
                if isinstance(results, tuple):
                    results = [results]
                for verdict, evidence in results:
                    print(f"{check.__name__[6:].upper():4s} {verdict:12s} {evidence}")
            except Exception as exc:
                print(f"{check.__name__[6:].upper():4s} FAIL         Checker could not complete: {type(exc).__name__}: {exc}")
        for label, verdict, evidence in frame_audit(output):
            print(f"{label:4s} {verdict:12s} {evidence}")
        if args.builder:
            for label, verdict, evidence in builder_evidence(output, args.builder):
                print(f"{label:4s} {verdict:12s} BUILDER EVIDENCE: {evidence}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
