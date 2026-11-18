"""Assignment 6 fixed-duration audit for two completed PsychoPy runs.

Run from a5-ldt-build (requires Python standard library only):
    uv run --python 3.11 python .\a6_timing_audit.py | Set-Content -Encoding utf8 .\a6_timing_results.txt

Reads the original CSV files without changing them; accepts duplicate headers.
Frame estimates are round((onset_stop - onset_start) * rounded_refresh_Hz).
These are estimates based on software timestamps, not physical light measurements.
"""
from __future__ import annotations
import csv
import glob
from pathlib import Path
from collections import Counter

EVENTS = [
    ('fixation', 'fixation.started', 'fixation.stopped', 500),
    ('prime', 'primeStim.started', 'primeStim.stopped', 150),
    ('SOA 150', 'primeStim.started', 'targetStim.started', 150),
    ('SOA 1000', 'primeStim.started', 'targetStim.started', 1000),
    ('ITI', 'blankText.started', 'blankText.stopped', 500),
    ('practice feedback', 'feedbackText.started', 'feedbackText.stopped', 1000),
    ('end screen', 'endText.started', 'endText.stopped', 2000),
]

def rowf(row, name):
    try:
        value = row.get(name, '').strip()
        return float(value) if value else None
    except (ValueError, AttributeError):
        return None

def read_rows(path):
    with path.open(newline='', encoding='utf-8-sig') as f:
        raw = csv.reader(f)
        header = next(raw)
        records = list(raw)
    if len(header) != len(records[0]):
        raise ValueError(f'CSV width mismatch: {path}')
    # Duplicate names (notably participant) get suffix to avoid silent overwrite.
    names = []
    seen = Counter()
    for name in header:
        seen[name] += 1
        names.append(name if seen[name] == 1 else f'{name}__copy{seen[name]}')
    return [dict(zip(names, record)) for record in records]

def interval_log(path):
    log = path.with_name(f'{path.stem}_frameIntervals.log')
    if not log.exists():
        return None
    values = [float(s.strip()) for s in log.read_text(encoding='utf-8-sig').replace('\n', ',').split(',') if s.strip()]
    return values

def check(run):
    paths = sorted(Path('data').glob(f'{run}_ldt_*.csv'))
    if len(paths) != 1:
        raise RuntimeError(f'Need exactly one completed participant {run} CSV; found {[str(p) for p in paths]}')
    path = paths[0]
    rows = read_rows(path)
    if run == 7:
        print('\n=== INSTRUMENTED CSV COLUMN ORDER (P7) ===')
        for j, col in enumerate(rows[0].keys(), 1):
            print(f'{j:02d}. {col}')
    trials = [r for r in rows if r.get('phase') in ('practice', 'experimental')]
    hz_set = {rowf(r, 'frameRate') for r in trials}
    if len(hz_set) != 1 or None in hz_set:
        raise ValueError(f'Unexpected frame rate values: {hz_set}')
    hz = int(round(hz_set.pop()))
    expected = {'fixation': round(.5*hz), 'prime': round(.150*hz), 'SOA 150': round(.150*hz),
                'SOA 1000': hz, 'ITI': round(.5*hz), 'practice feedback': hz, 'end screen': 2*hz}
    print(f'\n=== PARTICIPANT {run}: {path.name} ===')
    print(f'Rows: {len(rows)}; trials {len(trials)}; refresh {hz} Hz')
    print('| Event | Expected frames | Observed (frames: n) | Range, ms | Deviations, trial: actual (trial drops) |')
    print('|---|---:|---|---|---|')
    for event, start, stop, ms in EVENTS:
        occurrences = []
        for i,r in enumerate(rows):
            if event == 'SOA 150' and rowf(r, 'soa') != 150:
                continue
            if event == 'SOA 1000' and rowf(r, 'soa') != 1000:
                continue
            a,b = rowf(r, start),rowf(r, stop)
            if a is None or b is None: continue
            delta = 1000 * (b-a)
            frames = int(round((b-a)*hz))
            if r.get('phase') in ('practice', 'experimental'):
                tri = f'{r.get("phase", "")}/{r.get("trial_index", "")}'
            else:
                tri = f'nontrial row {i+1}'
            occurrences.append((frames, delta, tri, int(rowf(r, 'dropped_frames') or 0)))
        if occurrences:
            counts = Counter(x[0] for x in occurrences)
            fmt = ', '.join(f'{k}: {v}' for k,v in sorted(counts.items()))
            lo,hi = min(x[1] for x in occurrences), max(x[1] for x in occurrences)
            deviations = [f'{tri}: {frames} (I2={drops})' for frames,_,tri,drops in occurrences if frames != expected[event]]
            dev_text = '; '.join(deviations[:8]) + ('; ...' if len(deviations)>8 else '') if deviations else 'none'
            print(f'| {event} | {expected[event]} | {fmt} | {lo:.2f}–{hi:.2f} | {dev_text} |')
        else:
            print(f'| {event} | {expected[event]} | NO TIMESTAMPS | — | Not verifiable from saved file |')
    log = interval_log(path)
    if log is not None:
        csvdrops=sum(int(rowf(r, 'dropped_frames') or 0) for r in trials)
        logdrops=sum(v > 1.5/hz for v in log)
        print(f'I1 intervals: {len(log)}; sum {sum(log):.3f} sec; longest {max(log)*1000:.3f} ms')
        print(f'I2 CSV total: {csvdrops}; interval-log count > {1.5/hz*1000:.3f} ms: {logdrops}; agreement: {"PASS" if csvdrops==logdrops else "FAIL"}')
    else:
        print('I1 LOG NOT FOUND — timing summaries above still calculated from CSV')

if __name__ == '__main__':
    print('Software-timestamp audit; frames inferred from refresh duration, not measured directly by photodiode.')
    for hz in (60,75,120,144):
        print(f'Target counts at {hz} Hz: fixation={round(hz*.5)}, prime={round(hz*.15)}, SOA150={round(hz*.15)}, SOA1000={hz}, ITI={round(hz*.5)}, feedback={hz}, end={2*hz}')
    for n in (7, 8):
        check(n)
