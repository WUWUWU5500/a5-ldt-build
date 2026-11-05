"""PSY 8683 Assignment 5: output verifier.

First-pass checker for Q1-Q10. The primary Assignment 5 automatic checks are
Q1 (participant's list) and Q2 (all rows once, in file order). Other checks
only make a PASS/FAIL claim for properties truly observable in the CSV and
otherwise return PILOT with specific limits.

Usage:
    uv run python check_output.py data/3_ldt_*.csv
    uv run python check_output.py provided/output_files/file_*.csv --lists provided/canonical_trial_lists

Python standard library only. Supports duplicate PsychoPy CSV column names.
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
        return "PILOT", f"Cannot establish dialog participant independently: {origin}. Inspect dialog/run metadata."
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
        return "PILOT", f"Cannot prove participant's intended trial order: {origin}."
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
    """Practice/break/main sequence, and what needs human observation."""
    phase = [output.get(r, "phase") for r in output.trials]
    expected = ["practice"] * 8 + ["experimental"] * 96
    if phase == expected:
        observed = ("PASS", "8 practice trials precede all 96 experimental trials in the CSV; a different count/order would fail.")
    else:
        observed = ("FAIL", f"Observed phase order/count: {dict(Counter(phase))}, expected 8 practice then 96 experimental.")
    return [observed, ("PILOT", "Instruction and break SPACE behavior, correct/incorrect/timeout feedback display, and 2-second end screen require observing a run or inspecting Builder.")]


def num(output: Output, row: list[str], name: str) -> float | None:
    try:
        value = output.get(row, name)
        return float(value) if value != "" else None
    except ValueError:
        return None


def check_q4(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    """Check measured prime-to-target SOA and note unobservable visual effects."""
    if not output.has("prime_onset", "target_onset", "soa"):
        return [("PILOT", "No recorded onset+SOA columns to test; observe timing in a controlled Pilot run.")]
    errors: list[str] = []
    tested = 0
    for i, row in enumerate(output.trials, 1):
        prime, target, soa = (num(output,row,x) for x in ("prime_onset", "target_onset", "soa"))
        if None in (prime, target, soa):
            errors.append(f"trial {i}: absent/non-numeric timestamp or SOA")
            continue
        tested += 1
        if abs((target - prime) * 1000 - soa) > 35:
            errors.append(f"trial {i}: measured {(target-prime)*1000:.1f} ms, specified {soa:g} ms")
    timing = ("FAIL", f"SOA mismatch: {errors[:3]} ({len(errors)} problem(s)).") if errors else ("PASS", f"All {tested} observed prime-to-target intervals within 35 ms of specified SOA.")
    return [timing, ("PILOT", "Fixation and prime visibility, blank gap, and actual target cutoff require visual inspection and/or display-timing logs.")]


def check_q5(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    """Check whether recorded frameRate is rounded; visibility on true frames remains a Pilot check."""
    if not output.has("frameRate"):
        return [("PILOT", "frameRate absent from CSV; examine PsychoPy's startup measurement and Builder frame settings.")]
    raw = {output.get(row,"frameRate") for row in output.trials if output.get(row,"frameRate")}
    if len(raw) != 1:
        return [("FAIL", f"Expected a single measured rounded frameRate, found {sorted(raw)}.")]
    try:
        val = float(next(iter(raw)))
    except ValueError:
        return [("FAIL", f"Non-numeric frameRate: {raw}.")]
    check = ("PASS", f"Recorded frameRate={val:g} whole Hz.") if val > 0 and val.is_integer() else ("FAIL", f"frameRate={val:g} is not a positive whole number.")
    return [check, ("PILOT", "Whether ALL durations were controlled by whole frames, rather than seconds, cannot be proved from the saved rate alone; inspect Builder/generated script.")]


def check_q6(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    """F/J only; response mapping crosschecked with accuracy in Q10."""
    if not output.has("key"):
        return [("PILOT", "The requested 'key' output is absent; verify accepted keys in Builder/Pilot.")]
    invalid = [(i,output.get(r,"key")) for i,r in enumerate(output.trials,1) if output.get(r,"key") not in ("", "f", "j")]
    observed = ("FAIL", f"Other key values recorded, first {invalid[:3]}.") if invalid else ("PASS", "All recorded trial responses are f, j, or empty (could fail if any other key was recorded).")
    return [observed, ("PILOT", "The CSV cannot establish that irrelevant keys are ignored or Escape quits; test in Pilot mode.")]


def check_q7(output: Output, lists_dir: str) -> tuple[str, str]:
    return "PILOT", "RT clock start at the target's first refresh cannot be independently inferred from RT alone; verify simultaneous target/keyboard start and clock reset on flip in Builder/generated script."


def check_q8(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    if not output.has("prime_shown", "target_shown"):
        return [("FAIL", "prime_shown or target_shown missing from output CSV.")]
    bad = [(i,output.get(r,"prime_shown"),output.get(r,"target_shown")) for i,r in enumerate(output.trials,1) if output.get(r,"prime_shown") != output.get(r,"prime") or output.get(r,"target_shown") != output.get(r,"target").upper()]
    observed = ("FAIL", f"Displayed text fields mismatch the expected transformations; first {bad[:3]}.") if bad else ("PASS", "All prime_shown values equal lowercase source primes; all target_shown equal uppercase targets.")
    return [observed, ("PILOT", "CSV agreement alone cannot prove that text came from the actual visual object rather than a copied condition; inspect Code component.")]


def check_q9(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    if not output.has("prime_onset", "target_onset"):
        return [("FAIL", "prime_onset or target_onset absent from CSV.")]
    if not output.has("primeStim.started", "targetStim.started"):
        return [("PILOT", "No PsychoPy stimulus .started columns available for independent timestamp comparison.")]
    bad = []
    for i,row in enumerate(output.trials,1):
        a,b,c,d = (num(output,row,x) for x in ("prime_onset","primeStim.started","target_onset","targetStim.started"))
        if None in (a,b,c,d) or abs(a-b)>0.025 or abs(c-d)>0.025:
            bad.append(i)
    if bad:
        return [("FAIL", f"Onset timestamps differ from stimulus .started on {len(bad)} trial(s), first {bad[:5]}.")]
    return [("PASS", "prime_onset and target_onset match corresponding PsychoPy stimulus .started values within 25 ms on all trial rows.")]


def check_q10(output: Output, lists_dir: str) -> list[tuple[str, str]]:
    required = list(TRIAL_COLUMNS) + ["key","rt","accuracy","timeout"]
    missing = [c for c in required if not output.has(c)]
    structural = ("FAIL", f"Missing required columns: {missing}.") if missing else ("PASS", "All ten trial-list columns and key/rt/accuracy/timeout appear in the output header.")
    if missing:
        return [structural]
    p, origin = output.dialog_id()
    if p is None:
        return [structural, ("PILOT", f"Could not check participant-dependent scoring: {origin}.")]
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
    return [structural, scoring, ("PILOT", f"Duplicate header names {duplicates}; raw CSV retains both, but import software may reject or rename them. Confirm source of each in Builder.")]


CHECKS = [check_q1, check_q2, check_q3, check_q4, check_q5,
          check_q6, check_q7, check_q8, check_q9, check_q10]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="+", help="CSV files")
    ap.add_argument("--lists", default="trial_lists", help="Folder of participant trial lists")
    args = ap.parse_args()
    for filepath in args.files:
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
                    print(f"{check.__name__[6:].upper():4s} {verdict:5s} {evidence}")
            except Exception as exc:
                print(f"{check.__name__[6:].upper():4s} FAIL  Checker could not complete: {type(exc).__name__}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
