"""Normalisers that make any model/demo output safe for the UI to render."""

from __future__ import annotations

from .constants import DEFECTS, PPE_LABELS, SEVERITY_ORDER, URGENCY_COLOR


def normalise_safety(d: dict) -> dict:
    d = d if isinstance(d, dict) else {}
    try:
        score = int(max(0, min(100, float(d.get("safety_score", 0)))))
    except (TypeError, ValueError):
        score = 0
    d["safety_score"] = score
    d.setdefault("overall_status", "Needs Improvement")
    d.setdefault("summary", "")
    d.setdefault("workers_detected", 0)

    ppe = d.get("ppe_detection") if isinstance(d.get("ppe_detection"), dict) else {}
    for key in PPE_LABELS:
        item = ppe.get(key) if isinstance(ppe.get(key), dict) else {}
        item.setdefault("status", "not_visible")
        item.setdefault("workers_observed", 0)
        item.setdefault("notes", "")
        ppe[key] = item
    d["ppe_detection"] = ppe

    hazards = [h for h in d.get("hazards", []) if isinstance(h, dict)]
    for h in hazards:
        if h.get("severity") not in SEVERITY_ORDER:
            h["severity"] = "Medium"
    hazards.sort(key=lambda h: SEVERITY_ORDER.index(h["severity"]), reverse=True)
    d["hazards"] = hazards
    return d


def normalise_crack(d: dict) -> dict:
    d = d if isinstance(d, dict) else {}
    if d.get("defect_type") not in DEFECTS:
        d["defect_type"] = "Hairline"
    for key, default in (("confidence", 0.5), ("estimated_crack_width_mm", 0.0)):
        try:
            d[key] = float(d.get(key, default))
        except (TypeError, ValueError):
            d[key] = default
    d["severity"] = d.get("severity") if d.get("severity") in SEVERITY_ORDER else "Medium"
    d["urgency"] = d.get("urgency") if d.get("urgency") in URGENCY_COLOR else "Repair within 30 days"
    d["root_causes"] = [str(x) for x in d.get("root_causes", [])]
    d["recommended_repairs"] = [r for r in d.get("recommended_repairs", []) if isinstance(r, dict)]
    for key in ("crack_pattern", "monitoring_plan", "standard_reference", "disclaimer"):
        d.setdefault(key, "—")
    return d


NORMALISERS = {"safety": normalise_safety, "crack": normalise_crack}
