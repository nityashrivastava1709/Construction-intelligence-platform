"""Tab 1 - Site Safety & PPE Audit."""

from __future__ import annotations

import json
from datetime import datetime

import streamlit as st

from core.constants import OVERALL_STATUS_COLOR, PPE_LABELS, PPE_STATUS, SEVERITY_COLOR
from core.gemini_service import run_analysis
from core.utils import bytes_seed, load_image

from .components import demo_banner, html, item_card, metric_card, pill

STATE_KEY = "safety_result"


def render(api_key: str, model: str) -> None:
    st.subheader("🦺 Site Safety & PPE Audit")
    st.caption("Upload a site photo. Gemini audits PPE compliance and hazards against OSHA 1926 and IS 456 practices.")

    upload = st.file_uploader("Construction site photo", type=["jpg", "jpeg", "png"], key="safety_up")
    if not upload:
        st.info("Upload a JPG/PNG site photograph to begin.", icon="📷")
        return
    try:
        image = load_image(upload)
    except Exception:
        st.error("Could not read that image. Please upload a valid JPG or PNG.")
        return

    left, right = st.columns([1, 1.25], gap="large")
    with left:
        st.image(image, caption=upload.name, use_container_width=True)
        run = st.button("🔍 Run safety audit", type="primary", use_container_width=True, key="safety_run")

    if run:
        with st.spinner("Analysing site photo…"):
            outcome = run_analysis("safety", api_key, model, image, bytes_seed(upload.getvalue()))
        if outcome.error:
            st.warning(f"Gemini request failed ({outcome.error}). Showing demonstration output instead.")
        st.session_state[STATE_KEY] = (outcome, upload.name)

    stored = st.session_state.get(STATE_KEY)
    if not stored or stored[1] != upload.name:
        return
    outcome, _ = stored
    res = outcome.result

    with right:
        _render_summary(res, outcome.is_demo)
    _render_ppe(res)
    _render_hazards(res)

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_image": upload.name,
        "mode": "demo" if outcome.is_demo else "live",
        **res,
    }
    st.download_button(
        "⬇️ Download JSON report",
        json.dumps(report, indent=2),
        file_name="safety_audit_report.json",
        mime="application/json",
    )


def _render_summary(res: dict, is_demo: bool) -> None:
    demo_banner(is_demo)
    score = res["safety_score"]
    fallback = "green" if score >= 80 else "amber" if score >= 60 else "orange" if score >= 40 else "red"
    status_color = OVERALL_STATUS_COLOR.get(res["overall_status"], fallback)
    serious = sum(h["severity"] in ("High", "Critical") for h in res["hazards"])

    c1, c2, c3 = st.columns(3)
    c1.markdown(metric_card("Safety score", f"{score}/100", pill(res["overall_status"], status_color)), unsafe_allow_html=True)
    c2.markdown(metric_card("Workers detected", str(res["workers_detected"]), "in frame"), unsafe_allow_html=True)
    c3.markdown(metric_card("High / Critical", str(serious), f"of {len(res['hazards'])} hazards"), unsafe_allow_html=True)
    st.progress(score / 100)
    if res["summary"]:
        st.write(res["summary"])


def _render_ppe(res: dict) -> None:
    st.markdown("#### PPE compliance checklist")
    for col, (key, (icon, label)) in zip(st.columns(4), PPE_LABELS.items()):
        item = res["ppe_detection"][key]
        text, color = PPE_STATUS.get(item["status"], PPE_STATUS["not_visible"])
        col.markdown(
            item_card(
                color,
                f"{icon} {label}",
                f'Workers observed: {item["workers_observed"]}<br>{item["notes"]}',
                extra=pill(text, color),
            ),
            unsafe_allow_html=True,
        )


def _render_hazards(res: dict) -> None:
    st.markdown("#### Identified site hazards")
    if not res["hazards"]:
        st.success("No hazards identified in this image.")
        return
    for h in res["hazards"]:
        color = SEVERITY_COLOR[h["severity"]]
        html(
            item_card(
                color,
                f'{h.get("hazard", "Hazard")} &nbsp;{pill(h["severity"].upper(), color)}',
                f'📍 {h.get("location", "—")} · 📘 {h.get("standard_reference", "—")}<br>'
                f'🛠️ <b>Remedy:</b> {h.get("remedy", "—")}',
            )
        )
