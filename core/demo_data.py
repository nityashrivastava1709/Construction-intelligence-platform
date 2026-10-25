"""Deterministic sample outputs used when no API key is supplied (or the API fails)."""

from __future__ import annotations


def demo_safety(seed: int) -> dict:
    variants = [
        dict(score=58, status="Non-Compliant", vest="non_compliant", harness="non_compliant"),
        dict(score=74, status="Needs Improvement", vest="compliant", harness="non_compliant"),
        dict(score=36, status="Critical Risk", vest="non_compliant", harness="non_compliant"),
    ]
    v = variants[seed % len(variants)]
    return {
        "safety_score": v["score"],
        "overall_status": v["status"],
        "summary": "Demonstration output. Several workers show partial PPE and fall-protection "
        "gaps near the working edge; housekeeping and access control need attention.",
        "workers_detected": 4 + seed % 3,
        "ppe_detection": {
            "helmet": {"status": "compliant", "workers_observed": 4, "notes": "Helmets worn; one chin strap loose."},
            "high_vis_vest": {"status": v["vest"], "workers_observed": 3, "notes": "At least one worker without a vest."},
            "steel_toe_boots": {"status": "not_visible", "workers_observed": 0, "notes": "Footwear not clearly visible."},
            "safety_harness": {"status": v["harness"], "workers_observed": 2, "notes": "Work at height without anchored harness."},
        },
        "hazards": [
            {"hazard": "Unprotected working edge", "severity": "Critical", "location": "Upper slab edge",
             "remedy": "Install guardrails (1.0 m top rail, mid rail, toe board) and enforce 100% harness tie-off.",
             "standard_reference": "OSHA 1926.501(b)"},
            {"hazard": "Scaffold without full planking / bracing", "severity": "High", "location": "Left elevation",
             "remedy": "Complete decking, add cross-bracing and obtain a scaffold tag inspection before use.",
             "standard_reference": "OSHA 1926.451; IS 4014"},
            {"hazard": "Exposed reinforcement starter bars", "severity": "Medium", "location": "Column stubs",
             "remedy": "Fit rebar caps / mushroom protectors on all protruding bars.",
             "standard_reference": "OSHA 1926.701(b)"},
            {"hazard": "Material stacked in walkway", "severity": "Low", "location": "Ground level",
             "remedy": "Designate laydown areas and keep 1.2 m clear access paths.",
             "standard_reference": "OSHA 1926.25"},
        ],
    }


def demo_crack(seed: int) -> dict:
    options = [
        ("Structural Shear", 1.8, "Critical", "Immediate action", "Diagonal (45°)"),
        ("Settlement", 1.1, "High", "Repair within 7 days", "Stair-step / vertical"),
        ("Hairline", 0.15, "Low", "Monitor", "Random map pattern"),
        ("Thermal Expansion", 0.4, "Medium", "Repair within 30 days", "Horizontal at slab-wall joint"),
        ("Spalling", 0.8, "High", "Repair within 7 days", "Delamination with exposed steel"),
    ]
    defect, width, severity, urgency, pattern = options[seed % len(options)]
    return {
        "defect_type": defect,
        "confidence": round(0.72 + (seed % 20) / 100, 2),
        "estimated_crack_width_mm": width,
        "crack_pattern": pattern,
        "severity": severity,
        "urgency": urgency,
        "root_causes": [
            "Differential foundation settlement or inadequate soil bearing",
            "Insufficient shear reinforcement / stirrup spacing in the member",
            "Restrained thermal or shrinkage movement without control joints",
            "Corrosion of reinforcement due to low cover or chloride ingress",
        ],
        "recommended_repairs": [
            {"method": "Epoxy injection",
             "description": "Seal and inject cracks > 0.3 mm using low-viscosity epoxy via surface ports.",
             "materials": "Epoxy resin (IS 15988 compatible), injection ports, surface sealant"},
            {"method": "Structural re-grouting",
             "description": "Remove loose concrete, then re-grout with non-shrink cementitious grout.",
             "materials": "Non-shrink grout, bonding agent, anti-corrosive rebar primer"},
            {"method": "Jacketing / strengthening",
             "description": "If shear distress is confirmed, add RC / FRP jacketing as designed by the structural engineer.",
             "materials": "FRP wrap or micro-concrete, additional ties"},
        ],
        "monitoring_plan": "Fix crack gauges / glass tell-tales; log width weekly for 8 weeks, then monthly.",
        "standard_reference": "IS 456:2000 Cl. 35.3.2 (general crack width limit ≈ 0.3 mm); IS 15988 (seismic retrofit)",
        "disclaimer": "Demonstration output. Verify on site with a licensed structural engineer before repair.",
    }


_CHAT_RULES = [
    (("curing", "cure"),
     "**Curing (IS 456 Cl. 13.5):** keep OPC concrete moist for at least 7 days (10 days for blended cement or "
     "hot/dry weather). Use ponding, wet hessian or curing compound; start as soon as the surface can take it "
     "without damage."),
    (("mix", "m20", "m25", "ratio"),
     "**Nominal mixes (IS 456):** M20 ≈ 1:1.5:3, M25 ≈ 1:1:2. For structural members prefer design mixes with a "
     "controlled water-cement ratio (≤ 0.50 for moderate exposure)."),
    (("cover", "rebar", "reinforcement"),
     "**Nominal cover (IS 456 Table 16):** 20 mm slabs/beams (mild), 40 mm columns, 50 mm footings in contact "
     "with soil. Use cover blocks of equal grade at ≤ 1 m spacing."),
    (("shuttering", "formwork", "deshutter", "de-shutter", "stripping", "strip"),
     "**Stripping times (IS 456 Cl. 11.3):** vertical formwork 16–24 h, slab soffits 3 days (props left), beam "
     "soffits 7 days, props to slabs up to 4.5 m span 7 days, props to beams ≤ 6 m 14 days (OPC, 15 °C+)."),
    (("crane", "wind"),
     "Suspend crane lifts when wind exceeds the manufacturer's limit (commonly ~36 km/h), lower the jib to "
     "weathervane, and clear the swing radius."),
    (("ppe", "helmet", "harness"),
     "Minimum PPE: helmet (IS 2925), hi-vis vest, safety shoes (IS 15298), full-body harness (IS 3521) above "
     "1.8 m / 6 ft with 100% tie-off."),
]


def demo_chat(question: str, weather: str) -> str:
    q = question.lower()
    for keys, answer in _CHAT_RULES:
        if any(k in q for k in keys):
            return f"{answer}\n\n_(Demo mode · site weather: {weather})_"
    return (
        "I'm running in demonstration mode. Add a Gemini API key in the sidebar for full conversational answers. "
        "Try asking about **curing**, **concrete mix ratios**, **rebar cover**, **formwork stripping**, "
        "**crane operations** or **PPE**.\n\n"
        f"_(Site weather: {weather})_"
    )


DEMO_ANALYZERS = {"safety": demo_safety, "crack": demo_crack}
