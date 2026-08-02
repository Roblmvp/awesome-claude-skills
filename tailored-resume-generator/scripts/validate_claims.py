#!/usr/bin/env python3
"""Deterministically separate evidence-backed resume claims from gaps."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ELIGIBLE = {
    "verified_candidate_fact",
    "candidate_confirmed_fact",
    "approximate_candidate_confirmed_fact",
    "transferable_experience",
}
KNOWN = ELIGIBLE | {
    "job_requirement",
    "inferred_possibility",
    "unknown",
    "prohibited_unsupported_claim",
}


def classify(records: list[dict]) -> dict[str, list[dict]]:
    """Return eligible claims and gaps, rejecting malformed evidence records."""
    claims, gaps = [], []
    for record in records:
        status = record.get("status")
        if status not in KNOWN:
            raise ValueError(f"unknown claim status: {status!r}")
        item = dict(record)
        if status in ELIGIBLE:
            if not item.get("evidence_id"):
                raise ValueError("eligible claim requires evidence_id")
            if status == "approximate_candidate_confirmed_fact" and item.get("approximate") is not True:
                raise ValueError("approximate fact requires approximate=true")
            if status == "transferable_experience":
                item["label"] = "transferable experience"
            claims.append(item)
        else:
            gaps.append(item)
    return {"eligible_claims": claims, "gaps": gaps}


def assemble_employer_text(records: list[dict]) -> str:
    """Assemble only evidence-eligible text for an employer-facing draft."""
    result = classify(records)
    return "\n".join(item["text"] for item in result["eligible_claims"])


def main() -> int:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    records = json.loads(source.read_text() if source else sys.stdin.read())
    print(json.dumps(classify(records), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
