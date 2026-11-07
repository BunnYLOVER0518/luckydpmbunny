#!/usr/bin/env python3
"""Build the standalone page from the authoritative DPM rows.

Run `python3 scripts/build-dpm.py` after editing data/dpm-raw.json.
Run `python3 scripts/build-dpm.py --check` in CI or before committing.
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/dpm-raw.json"
OUTPUT = ROOT / "index.html"
PREFIX = "const RAW="


def extract(page):
    if page.count(PREFIX) != 1:
        raise ValueError("index.html must contain exactly one RAW assignment")
    start = page.index(PREFIX) + len(PREFIX)
    rows, length = json.JSONDecoder().raw_decode(page[start:])
    if page[start + length] != ",":
        raise ValueError("unexpected RAW assignment boundary")
    return rows, start, start + length


def validate(rows):
    if not isinstance(rows, list) or len(rows) != 274:
        raise ValueError("expected 274 DPM cases")
    heroes = {r["hero"] for r in rows}
    expected_heroes = {
        "각성 헤일리", "군체 타르", "귀신 닌자", "기사 랜슬롯", "닥터 펄스",
        "마도학자 지지", "마왕 드래곤", "만년 초나", "보스 골라조", "블롭단",
        "사신 다이안", "선인 쿤", "아이엠 미야옹", "에이스 배트맨",
        "여왕 콜디", "요정왕 에밀리", "용사 레이", "원시 밤바",
        "천룡 우치", "캡틴 로카", "탑 베인",
    }
    if heroes != expected_heroes:
        raise ValueError("hero roster changed; review and update the baseline")
    keys = [(r["hero"], r["level"], r["variant"], r["boss"]) for r in rows]
    if len(set(keys)) != len(rows):
        raise ValueError("duplicate DPM case")
    samples = {
        ("원시 밤바", 6, "기본", 1): 3.757365590142158,
        ("닥터 펄스", 12, "기본", 1): 5.281764597692531,
        ("요정왕 에밀리", 6, "기본", 1): 38.924561623412544,
        ("마도학자 지지", 25, "기본", 2): 188.9572023324705,
    }
    by_key = dict(zip(keys, rows))
    for key, expected in samples.items():
        if by_key[key]["values"]["0"] != expected:
            raise ValueError(f"baseline DPM changed: {key}")
    for row in rows:
        if set(row["values"]) != {"0", "6", "12"}:
            raise ValueError(f"missing support DPM values: {row['hero']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if index.html differs from source")
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    validate(source)
    page = OUTPUT.read_text(encoding="utf-8")
    actual, start, end = extract(page)
    compact = json.dumps(source, ensure_ascii=False, separators=(",", ":"))
    built = page[:start] + compact + page[end:]
    if args.check:
        if actual != source or built != page:
            raise SystemExit("index.html RAW differs from data/dpm-raw.json; run python3 scripts/build-dpm.py")
        print(f"OK: {len(source)} cases, {len({r['hero'] for r in source})} heroes, baseline DPM values")
    else:
        OUTPUT.write_text(built, encoding="utf-8")
        print("Updated index.html RAW from data/dpm-raw.json")


if __name__ == "__main__":
    main()
