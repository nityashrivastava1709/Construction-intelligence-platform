"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1

Entrypoint only: page config, layout and wiring. Logic lives in `core/`, UI in `ui/`.
Run locally:  streamlit run app.py
"""

import streamlit as st

# set_page_config must be the first Streamlit call
st.set_page_config(
    page_title="Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui import assistant_tab, crack_tab, planning_tab, safety_tab  # noqa: E402
from ui.sidebar import render_sidebar  # noqa: E402
from ui.styles import inject_styles  # noqa: E402

HERO = (
    '<div class="hero"><h1>🏗️ Multimodal Construction Intelligence Platform</h1>'
    "<p>AI-powered site safety audits, structural crack diagnostics, project valuation "
    "and weather-aware site advisory.</p></div>"
)
FOOTER = (
    '<div class="footer">Multimodal Construction Intelligence Platform · '
    "Skill Wallet Capstone Project 1 · Advisory output only</div>"
)


def main() -> None:
    inject_styles()
    api_key, model = render_sidebar()
    st.markdown(HERO, unsafe_allow_html=True)

    tab_safety, tab_crack, tab_plan, tab_assist = st.tabs(
        ["🦺 Safety & PPE Audit", "🧱 Crack Diagnostics", "📐 Planning & Valuation", "🌦️ Site Assistant"]
    )
    with tab_safety:
        safety_tab.render(api_key, model)
    with tab_crack:
        crack_tab.render(api_key, model)
    with tab_plan:
        planning_tab.render()
    with tab_assist:
        assistant_tab.render(api_key, model)

    st.markdown(FOOTER, unsafe_allow_html=True)


main()
