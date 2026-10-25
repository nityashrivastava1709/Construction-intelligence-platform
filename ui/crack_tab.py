"""Tab 2 - Crack Diagnostics & Structural Integrity."""

from __future__ import annotations

import json
from datetime import datetime

import streamlit as st

from core.constants import SEVERITY_COLOR, URGENCY_COLOR
from core.gemini_service import run_analysis
from core.utils import bytes_seed, load_image

from .components import demo_banner, html, item_card, metric_card, pill

STATE_KEY = "crack_result"


def render(api_key: str, model: str) -> None:
    st.subheader("🧱 Crack Diagnostics & Structural Integrity")
    st.caption("Upload a concrete or wall surface photo. Include a coin or scale for better width estimation.")

    upload = st.file_uploader("Concrete / wall surface photo", type=["jpg", "jpeg", "png"], key="crack_up")
    if not upload:
        st.info("Upload a close-up of the crack or damaged surface.", icon="🔎")
        return
    try:
        image = load_image(upload)
    except Exception:
        st.error("Could not read that image. Please upload a valid JPG or PNG.")
        return

    left, right = st.columns([1, 1.25], gap="large")
    with left:
        st.image(image, caption=upload.name, use_container_width=True)
        run = st.button("🧪 Diagnose defect", type="primary", use_container_width=True, key="crack_run")

    if run:
        with st.spinner("Running structural diagnostics…"):
            outcome = run_analysis("crack", api_key, model, image, bytes_seed(upload.getvalue()))
        if outcome.error:
            st.warning(f"Gemini request failed ({outcome.error}). Showing demonstration output instead.")
        st.session_state[STATE_KEY] = (outcome, upload.name)

    stored = st.session_state.get(STATE_KEY)
    if not stored or stored[1] != upload.name:
        return
    outcome, _ = stored
    res = outcome.result
    sev_color, urg_color = SEVERITY_COLOR[res["severity"]], URGENCY_COLOR[res["urgency"]]

    with right:
        demo_banner(outcome.is_demo)
        c1, c2 = st.columns(2)
        c1.markdown(
            metric_card("Defect type", res["defect_type"], f"Confidence {res['confidence']:.0%} · {res['crack_pattern']}"),
            unsafe_allow_html=True,
        )
        c2.markdown(
            metric_card("Est. crack width", f"{res['estimated_crack_width_mm']:.2f} mm", "IS 456 general limit ≈ 0.3 mm"),
            unsafe_allow_html=True,
        )
        st.write("")
        html(
            f"**Severity:** {pill(res['severity'].upper(), sev_color)} &nbsp; "
            f"**Urgency:** {pill(res['urgency'].upper(), urg_color)}"
        )
        st.progress(min(res["estimated_crack_width_mm"] / 3.0, 1.0), text="Width vs. 3 mm severe-damage reference")

    causes_col, repairs_col = st.columns(2, gap="large")
    with causes_col:
        st.markdown("#### Probable root causes")
        for cause in res["root_causes"]:
            st.markdown(f"- {cause}")
        st.markdown("#### Monitoring plan")
        st.write(res["monitoring_plan"])
    with repairs_col:
        st.markdown("#### Recommended engineering repairs")
        for r in res["recommended_repairs"]:
            html(
                item_card(
                    sev_color,
                    f"🔧 {r.get('method', 'Repair')}",
                    f"{r.get('description', '')}<br><b>Materials:</b> {r.get('materials', '—')}",
                )
            )

    st.caption(f"📘 {res['standard_reference']}  ·  ⚠️ {res['disclaimer']}")
    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_image": upload.name,
        "mode": "demo" if outcome.is_demo else "live",
        **res,
    }
    st.download_button(
        "⬇️ Download JSON report",
        json.dumps(report, indent=2),
        file_name="crack_diagnostic_report.json",
        mime="application/json",
    )
