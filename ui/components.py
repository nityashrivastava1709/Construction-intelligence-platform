"""Small reusable UI building blocks."""

from __future__ import annotations

import streamlit as st


def html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


def pill(text: str, color: str = "grey") -> str:
    return f'<span class="pill {color}">{text}</span>'


def metric_card(label: str, value: str, sub: str = "") -> str:
    return (
        f'<div class="card"><div class="label">{label}</div>'
        f'<div class="value">{value}</div><div class="sub">{sub}</div></div>'
    )


def item_card(color: str, title: str, meta: str = "", extra: str = "") -> str:
    """Left-bordered info card. `extra` is raw HTML placed between title and meta (e.g. a pill)."""
    meta_html = f'<div class="meta">{meta}</div>' if meta else ""
    return f'<div class="item {color}"><div class="title">{title}</div>{extra}{meta_html}</div>'


def demo_banner(is_demo: bool) -> None:
    if is_demo:
        html(
            '<div class="demo-banner">🧪 <b>Demonstration output</b> — '
            "add a Gemini API key for real image analysis.</div>"
        )
