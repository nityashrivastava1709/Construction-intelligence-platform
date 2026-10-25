"""Project budget, asset valuation and material-requirement model.

All rates are illustrative planning assumptions (INR). Tune the tables below
to match local schedules of rates or your rubric.
"""

from __future__ import annotations

from dataclasses import dataclass

# cost: INR / sq ft | steel: kg / sq ft | cement: 50 kg bags / sq ft | premium: market-value factor
STRUCTURES: dict[str, dict[str, float]] = {
    "RCC Framed Residential": dict(cost=2200, steel=4.0, cement=0.45, premium=1.00),
    "Load-Bearing Masonry (G+1)": dict(cost=1800, steel=2.2, cement=0.40, premium=0.90),
    "Commercial Complex (RCC)": dict(cost=2800, steel=4.8, cement=0.50, premium=1.35),
    "Steel / PEB Industrial Shed": dict(cost=1700, steel=9.0, cement=0.20, premium=0.80),
    "High-Rise Residential (10+ floors)": dict(cost=3200, steel=5.5, cement=0.55, premium=1.25),
}

# cost_mult: construction-cost multiplier | market: finished market value, INR / sq ft
TIERS: dict[str, dict[str, float]] = {
    "Tier 1 (Mumbai, Delhi NCR, Bengaluru…)": dict(cost_mult=1.25, market=11000),
    "Tier 2 (Indore, Jaipur, Pune…)": dict(cost_mult=1.00, market=5500),
    "Tier 3 (Smaller cities & towns)": dict(cost_mult=0.82, market=3000),
}

MILESTONES: list[tuple[str, int]] = [
    ("Site prep & foundation", 15),
    ("Plinth & substructure", 30),
    ("Superstructure frame", 55),
    ("Masonry & slabs", 70),
    ("MEP & plastering", 85),
    ("Finishes & handover", 100),
]

LAND_SHARE = 0.30  # share of finished market value attributed to land


@dataclass(frozen=True)
class Valuation:
    budget: float
    capex: float
    remaining: float
    full_value: float
    asset_value: float
    steel_tonnes: float
    cement_bags: float
    fraction: float


def compute_valuation(structure: str, sqft: float, tier: str, completion: int) -> Valuation:
    s, t = STRUCTURES[structure], TIERS[tier]
    c = max(0, min(100, completion)) / 100
    budget = sqft * s["cost"] * t["cost_mult"]
    full_value = sqft * t["market"] * s["premium"]
    return Valuation(
        budget=budget,
        capex=budget * c,
        remaining=budget * (1 - c),
        full_value=full_value,
        asset_value=full_value * (LAND_SHARE + (1 - LAND_SHARE) * c),
        steel_tonnes=sqft * s["steel"] / 1000,
        cement_bags=sqft * s["cement"],
        fraction=c,
    )


def milestone_states(completion: int) -> list[tuple[str, int, str]]:
    """Return (name, end_pct, state) where state is done | active | pending."""
    out, prev = [], 0
    for name, end in MILESTONES:
        state = "done" if completion >= end else "active" if completion > prev else "pending"
        out.append((name, end, state))
        prev = end
    return out
