"""Quick I1/I2 instrumentation check. Run from the A5/A6 repository root.

Examples:
  uv run python verify_a6_frame_log.py data/1_ldt_2026-11-17_20h00.00.000.csv
  uv run python verify_a6_frame_log.py data/7_ldt_*.csv

A complete PsychoPy run is necessary: Escape can bypass the End Experiment
hook that writes the frame interval log.
"""
from __future__ import annotations
import csv
from pathlib import Path
import sys
from collections import Counter


def check(csvfile: Path):
    if not csvfile.is_file():
        raise FileNotFoundError(csvfile)
    log = csvfile.with_name(csvfile.stem + '_frameIntervals.log')
    if not log.is_file():
        raise FileNotFoundError(f"Missing I1 interval log: {log}. Finish the run normally rather than pressing Escape.")
    with csvfile.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
        lines = list(reader)
    for field in ('phase', 'dropped_frames', 'frameRate'):
        if field not in headers:
            raise ValueError(f"Missing CSV column: {field}")
    at = {k: headers.index(k) for k in ('phase', 'dropped_frames', 'frameRate')}
    trials = [row for row in lines if row[at['phase']] in ('practice', 'experimental')]
    drops = [int(float(row[at['dropped_frames']])) for row in trials]
    hz_values = {int(round(float(row[at['frameRate']]))) for row in trials}
    if len(hz_values) != 1:
        raise ValueError(f"Expected one rounded frame rate, got: {hz_values}")
    hz = hz_values.pop()
    threshold = 1.5 / hz
    text = log.read_text(encoding='utf-8-sig').strip()
    intervals = [float(x.strip()) for x in text.replace('\n', ',').split(',') if x.strip()]
    logfile_drops = sum(interval > threshold for interval in intervals)
    csv_drops = sum(drops)
    total = sum(intervals)
    print(f'CSV: {csvfile.name}')
    print(f'LOG: {log.name}')
    print(f'Trials: {len(trials)} (practice={sum(row[at["phase"]] == "practice" for row in trials)}, experimental={sum(row[at["phase"]] == "experimental" for row in trials)})')
    print(f'Rounded frame rate: {hz} Hz; dropped threshold: {threshold*1000:.3f} ms')
    print(f'Intervals recorded: {len(intervals)}; summed duration: {total:.3f} s')
    print(f'CSV dropped_frames total: {csv_drops}')
    print(f'Log intervals above threshold: {logfile_drops}')
    passed = logfile_drops == csv_drops and len(intervals) > 0 and len(trials) > 0
    print('I1/I2 dropped-count reconciliation:', 'PASS' if passed else 'FAIL')
    if not passed:
        return False
    # Approximate size: in each trial, recorded flip intervals span the
    # fixation-to-last-visible-target period, not feedback, ITI, etc.
    if all(x in headers for x in ('fixation.started', 'trial.stopped')):
        fi = headers.index('fixation.started')
        en = headers.index('trial.stopped')
        dur = sum(float(row[en]) - float(row[fi]) for row in trials if row[fi] and row[en])
        delta = abs(dur - total)
        print(f'Approx. trial-screen duration: {dur:.3f} s; difference from I1 sum: {delta:.3f} s')
        print('Duration plausibility (within 3 frames per trial):', 'PASS' if delta < (3 * len(trials) / hz) else 'REVIEW')
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: uv run python verify_a6_frame_log.py data/<completed-run>.csv', file=sys.stderr)
        raise SystemExit(2)
    paths = []
    for spec in sys.argv[1:]:
        if '*' in spec or '?' in spec:
            import glob
            paths.extend(Path(p) for p in glob.glob(spec))
        else:
            paths.append(Path(spec))
    try:
        okay = all(check(p) for p in paths)
    except Exception as e:
        print(f'FAIL: {type(e).__name__}: {e}', file=sys.stderr)
        raise SystemExit(1)
    if not okay:
        raise SystemExit(1)
