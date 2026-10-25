"""Tab 3 - Planning & Real Estate Valuation."""

from __future__ import annotations

import streamlit as st

from core.rendering import RENDER_STYLES, build_render_prompt, pollinations_url
from core.utils import format_inr
from core.valuation import LAND_SHARE, MILESTONES, STRUCTURES, TIERS, compute_valuation, milestone_states

from .components import html, item_card, metric_card

_STATE_ICON = {"done": ("✅", "green"), "active": ("🔄", "amber"), "pending": ("⬜", "grey")}


def render() -> None:
    st.subheader("📐 Planning & Real Estate Valuation")

    c1, c2 = st.columns(2)
    structure = c1.selectbox("Structure type", list(STRUCTURES))
    tier = c2.selectbox("Location tier", list(TIERS), index=1)
    c3, c4 = st.columns([1, 1.4])
    sqft = c3.number_input("Built-up area (sq ft)", min_value=100, max_value=1_000_000, value=2400, step=100)
    completion = c4.slider("Completion (%)", 0, 100, 45)

    v = compute_valuation(structure, float(sqft), tier, completion)
    _render_financials(v, sqft, completion)
    _render_materials(v)
    _render_milestones(completion)

    with st.expander("Model assumptions"):
        st.markdown(
            "- Budget = area × base cost/sq ft × tier cost multiplier.\n"
            "- Capex incurred scales linearly with completion.\n"
            f"- Asset value = finished market value × ({LAND_SHARE:.0%} land + {1 - LAND_SHARE:.0%} × completion).\n"
            "- Steel and cement use rule-of-thumb intensities per sq ft for the selected structure.\n"
            "- Rates are illustrative planning estimates, not a registered valuation. Edit `core/valuation.py` to tune them."
        )

    _render_3d_section(structure, tier, float(sqft), completion)


def _render_financials(v, sqft: float, completion: int) -> None:
    cols = st.columns(4)
    cols[0].markdown(metric_card("Total project budget", format_inr(v.budget), f"₹{v.budget / sqft:,.0f} / sq ft"), unsafe_allow_html=True)
    cols[1].markdown(metric_card("Capex incurred", format_inr(v.capex), f"{completion}% spent · {format_inr(v.remaining)} to go"), unsafe_allow_html=True)
    cols[2].markdown(metric_card("Current asset valuation", format_inr(v.asset_value), f"At completion: {format_inr(v.full_value)}"), unsafe_allow_html=True)
    cols[3].markdown(metric_card("Value gain vs capex", format_inr(max(v.asset_value - v.capex, 0)), "Land + built value − spend"), unsafe_allow_html=True)


def _render_materials(v) -> None:
    st.write("")
    a, b = st.columns(2)
    a.markdown(metric_card("Steel requirement", f"{v.steel_tonnes:,.1f} tonnes", f"Used so far ≈ {v.steel_tonnes * v.fraction:,.1f} t"), unsafe_allow_html=True)
    b.markdown(
        metric_card(
            "Cement requirement",
            f"{v.cement_bags:,.0f} bags",
            f"≈ {v.cement_bags * 50 / 1000:,.1f} t · used ≈ {v.cement_bags * v.fraction:,.0f} bags",
        ),
        unsafe_allow_html=True,
    )


def _render_milestones(completion: int) -> None:
    st.markdown("#### Milestone progress")
    st.progress(completion / 100, text=f"{completion}% complete")
    for col, (name, end, state) in zip(st.columns(len(MILESTONES)), milestone_states(completion)):
        icon, color = _STATE_ICON[state]
        col.markdown(item_card(color, f"{icon} {name}", f"up to {end}%"), unsafe_allow_html=True)


def _render_3d_section(structure: str, tier: str, sqft: float, completion: int) -> None:
    st.markdown("#### 🎨 Conceptual 3D architectural rendering")
    left, right = st.columns([1, 2])
    style = left.selectbox("Render style", RENDER_STYLES)
    seed = left.number_input("Variation seed", 0, 9999, 42)
    prompt = left.text_area("Prompt (editable)", build_render_prompt(structure, tier, sqft, completion, style), height=170)
    with right:
        if st.button("Generate rendering", type="primary"):
            st.session_state["render_url"] = pollinations_url(prompt, int(seed))
        if st.session_state.get("render_url"):
            st.image(st.session_state["render_url"], caption="Generated via Pollinations AI (free, no key)", use_container_width=True)
            st.caption("If the image doesn't appear, wait a few seconds and click Generate again.")
