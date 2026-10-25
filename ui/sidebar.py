"""Sidebar: secure API key input, model choice, status, architecture and feature guide."""

from __future__ import annotations

import streamlit as st

from core.constants import MODELS
from core.gemini_service import GENAI_AVAILABLE

ARCHITECTURE = """
```
 app.py  (entrypoint · tabs)
   │
   ├─ ui/        Streamlit presentation (one module per tab)
   │
   └─ core/      framework-free logic
        ├─ gemini_service  ─► Gemini (JSON mode) ─► schemas.normalise
        ├─ demo_data       ─► fallback when no key / API error
        ├─ valuation       ─► budget · capex · asset value
        ├─ rendering       ─► Pollinations AI prompt + URL
        └─ weather_data    ─► advisories
   state: st.session_state only · no database
```
"""


def _secret_key() -> str:
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:  # no secrets file present
        return ""


def render_sidebar() -> tuple[str, str]:
    """Render the sidebar and return (api_key, model)."""
    with st.sidebar:
        st.markdown("## 🏗️ Construction Intelligence")
        st.caption("Skill Wallet · Capstone Project 1")

        key_input = st.text_input(
            "Google Gemini API key",
            type="password",
            placeholder="AIza…",
            help="Kept only in this browser session. Leave blank for demonstration mode.",
        )
        api_key = (key_input or _secret_key()).strip()
        model = st.selectbox("Gemini model", MODELS)

        if api_key and GENAI_AVAILABLE:
            st.success("Live mode · Gemini connected", icon="✅")
        else:
            st.warning("Demonstration mode · sample outputs", icon="🧪")
            if api_key and not GENAI_AVAILABLE:
                st.error("`google-genai` is not installed; running in demo mode.")
            st.caption("Get a free key at aistudio.google.com/apikey")

        st.divider()
        st.markdown("### 🧭 Features")
        st.markdown(
            "- 🦺 **Safety & PPE Audit** — Epic 2\n"
            "- 🧱 **Crack Diagnostics** — Epic 2\n"
            "- 📐 **Planning & Valuation** — Epic 3\n"
            "- 🌦️ **Site Assistant** — Epic 5"
        )
        with st.expander("🧩 Architecture overview"):
            st.markdown(ARCHITECTURE)
            st.markdown("**Fail-safe:** any API error falls back to demo data so the UI never breaks.")
        st.caption("⚠️ AI output is advisory. Always verify with a licensed engineer / safety officer.")
    return api_key, model
