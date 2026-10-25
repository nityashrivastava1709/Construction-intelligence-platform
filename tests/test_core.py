"""Run with:  pip install pytest && pytest -q"""

from PIL import Image

from core.gemini_service import run_analysis
from core.schemas import normalise_crack, normalise_safety
from core.utils import format_inr, parse_json
from core.valuation import compute_valuation, milestone_states

TIER2 = "Tier 2 (Indore, Jaipur, Pune…)"
RCC = "RCC Framed Residential"


def test_format_inr():
    assert format_inr(2_50_00_000) == "₹ 2.50 Cr"
    assert format_inr(7_50_000) == "₹ 7.50 Lakhs"
    assert format_inr(9_500) == "₹ 9,500"


def test_parse_json_handles_fences_and_noise():
    assert parse_json('```json\n{"a": 1}\n```') == {"a": 1}
    assert parse_json('Here you go: {"a": 2} thanks') == {"a": 2}


def test_valuation_bounds():
    zero = compute_valuation(RCC, 1000, TIER2, 0)
    full = compute_valuation(RCC, 1000, TIER2, 100)
    assert zero.capex == 0 and full.remaining == 0
    assert full.asset_value == full.full_value
    assert zero.asset_value < full.asset_value


def test_milestones():
    states = [s for *_, s in milestone_states(45)]
    assert states == ["done", "done", "active", "pending", "pending", "pending"]


def test_normalisers_clamp_and_fill():
    s = normalise_safety({"safety_score": 250, "hazards": [{"severity": "weird"}]})
    assert s["safety_score"] == 100 and s["hazards"][0]["severity"] == "Medium"
    assert set(s["ppe_detection"]) == {"helmet", "high_vis_vest", "steel_toe_boots", "safety_harness"}
    c = normalise_crack({"defect_type": "???", "urgency": "later"})
    assert c["defect_type"] == "Hairline" and c["urgency"] == "Repair within 30 days"


def test_demo_mode_without_key():
    img = Image.new("RGB", (10, 10))
    for kind in ("safety", "crack"):
        out = run_analysis(kind, "", "gemini-2.5-flash", img, seed=7)
        assert out.is_demo and out.error is None and out.result
