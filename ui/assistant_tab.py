"""Tab 4 - Daily Site Assistant & Weather-Aware Advisory."""

from __future__ import annotations

import streamlit as st

from core.gemini_service import chat_reply
from core.weather_data import WEATHER

from .components import html, metric_card, pill

CHAT_KEY = "chat"
GREETING = "Hi, I'm SiteMate. Ask me about concrete, curing, formwork, safety, IS codes or today's site plan."
QUICK_QUESTIONS = ["Curing requirements for slab?", "M25 mix ratio?", "When can I strip formwork?", "PPE for work at height?"]


def render(api_key: str, model: str) -> None:
    st.subheader("🌦️ Daily Site Assistant & Weather-Aware Advisory")
    weather = _render_advisory()
    st.divider()
    _render_chat(api_key, model, weather)


def _render_advisory() -> str:
    weather = st.radio(
        "Today's site weather",
        list(WEATHER),
        horizontal=True,
        format_func=lambda w: f"{WEATHER[w]['icon']} {w}",
    )
    info = WEATHER[weather]
    label, color = info["level"]
    html(f"**Advisory level:** {pill(label.upper(), color)}")
    for col, (title, value, sub) in zip(st.columns(3), info["cards"]):
        col.markdown(metric_card(title, value, sub), unsafe_allow_html=True)
    st.write("")
    for alert in info["alerts"]:
        html(f'<div class="item {color}">{alert}</div>')
    return weather


def _render_chat(api_key: str, model: str, weather: str) -> None:
    st.markdown("#### 💬 Construction engineering assistant")
    if CHAT_KEY not in st.session_state:
        st.session_state[CHAT_KEY] = [{"role": "assistant", "content": GREETING}]

    clicked = None
    for col, text in zip(st.columns(len(QUICK_QUESTIONS)), QUICK_QUESTIONS):
        if col.button(text, use_container_width=True):
            clicked = text

    box = st.container(height=380)
    for m in st.session_state[CHAT_KEY]:
        box.chat_message(m["role"]).markdown(m["content"])

    question = clicked or st.chat_input("Ask a construction engineering question…")
    if question:
        st.session_state[CHAT_KEY].append({"role": "user", "content": question})
        box.chat_message("user").markdown(question)
        with box.chat_message("assistant"):
            with st.spinner("Thinking…"):
                answer = chat_reply(api_key, model, weather, st.session_state[CHAT_KEY][-12:])
            st.markdown(answer)
        st.session_state[CHAT_KEY].append({"role": "assistant", "content": answer})

    if st.button("🗑️ Clear conversation"):
        st.session_state.pop(CHAT_KEY, None)
        st.rerun()
