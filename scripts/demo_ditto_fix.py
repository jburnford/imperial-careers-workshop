"""Replay one bounded correction on the workshop's saved audit examples.

Run: python3 scripts/demo_ditto_fix.py
This writes a workshop demonstration, not a change to the published graph.
"""
import copy
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DITTO = {"do", "ditto"}


def is_ditto(place):
    return isinstance(place, str) and place.strip().lower().rstrip(".") in DITTO


def correct(record):
    out = copy.deepcopy(record)
    changes, unresolved = [], []
    previous = None
    for i, event in enumerate(out["events"]):
        place = event.get("place")
        if is_ditto(place):
            if previous:
                event["place"] = previous
                event["place_inherited"] = True
                changes.append({"event": i + 1, "field": "place", "before": place,
                                "after": previous, "reason": "Printed ditto; previous event has a place."})
            else:
                unresolved.append({"event": i + 1, "reason": "No previous resolved place; keep for review."})
        # A missing or unresolved predecessor stops inheritance.
        previous = event.get("place")
        if not isinstance(previous, str) or not previous.strip() or is_ditto(previous):
            previous = None
    return out, changes, unresolved


def main():
    examples = json.loads((BASE / "outputs/structure/audit-examples.json").read_text())
    results = []
    for example in examples:
        before = example["struct"]
        after, changes, unresolved = correct(before)
        # Only the intended fields may change. Preserve every other field.
        restored = copy.deepcopy(after)
        for change in changes:
            i = change["event"] - 1
            restored["events"][i] = copy.deepcopy(before["events"][i])
            for key in set(before["events"][i]) | set(after["events"][i]):
                if key not in {"place", "place_inherited"}:
                    assert before["events"][i].get(key) == after["events"][i].get(key)
        assert restored == before
        assert correct(after) == (after, [], unresolved), "A second run must make no further changes"
        results.append({"person_id": example["person_id"], "source": example["source"],
                        "before": before, "after": after, "changes": changes, "unresolved": unresolved})

    # Deliberately constructed boundary cases, separate from the historical sample.
    boundary = {"events": [{"place": "do."}, {"place": "Ceylon"},
                           {"place": None}, {"place": "ditto"}]}
    unchanged, changes, unresolved = correct(boundary)
    assert unchanged == boundary and not changes and len(unresolved) == 2
    balmer = next(r for r in results if "col1936-p832b11" in r["person_id"])
    assert balmer["after"]["events"][3]["place"] == "Kenya-Uganda-Tanganyika"
    assert sum(len(r["changes"]) for r in results) == 1
    report = {
        "scope": "Workshop replay on three saved pre-normalisation audit records; not a corpus rerun or accuracy estimate.",
        "records_checked": len(results),
        "events_checked": sum(len(r["before"]["events"]) for r in results),
        "events_changed": sum(len(r["changes"]) for r in results),
        "checks": {"other_fields_preserved": True, "second_run_unchanged": True,
                   "missing_predecessor_left_unresolved": True},
        "records": results,
    }
    target = BASE / "outputs/structure/ditto-fix-replay.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Checked {report['records_checked']} records / {report['events_checked']} events; "
          f"changed {report['events_changed']} place. Preservation, repeat-run and boundary checks passed.")


if __name__ == "__main__":
    main()
