"""Global CSS injected once from app.py."""

import streamlit as st

CSS = """
<style>
.block-container {padding-top: 1.4rem; max-width: 1250px;}
.hero {background: linear-gradient(120deg,#0f2027 0%,#203a43 45%,#2c5364 100%);
  padding: 1.6rem 2rem; border-radius: 16px; color: #fff; margin-bottom: 1.2rem;}
.hero h1 {margin: 0; font-size: 1.9rem; font-weight: 800; letter-spacing: -.3px;}
.hero p {margin: .3rem 0 0; opacity: .85; font-size: .98rem;}
.card {background: var(--secondary-background-color); border: 1px solid rgba(128,128,128,.22);
  border-radius: 14px; padding: 1rem 1.2rem; height: 100%;}
.card .label {font-size: .78rem; text-transform: uppercase; letter-spacing: .06em; opacity: .7;}
.card .value {font-size: 1.75rem; font-weight: 800; line-height: 1.25;}
.card .sub {font-size: .82rem; opacity: .7;}
.pill {display:inline-block; padding: .22rem .75rem; border-radius: 999px; font-size: .78rem;
  font-weight: 700; color:#fff; letter-spacing:.03em;}
.pill.green{background:#1e8e5a;} .pill.amber{background:#d98a00;} .pill.orange{background:#e0561b;}
.pill.red{background:#c62828;} .pill.blue{background:#2b6cb0;} .pill.grey{background:#6b7280;}
.item {border-left: 5px solid #6b7280; background: var(--secondary-background-color);
  border-radius: 10px; padding: .75rem 1rem; margin-bottom: .6rem;}
.item.green{border-color:#1e8e5a;} .item.amber{border-color:#d98a00;}
.item.orange{border-color:#e0561b;} .item.red{border-color:#c62828;} .item.blue{border-color:#2b6cb0;}
.item .title {font-weight: 700;} .item .meta {font-size:.85rem; opacity:.8;}
.demo-banner {background:#fff4e0; color:#7a4b00; border:1px solid #f1c27a; padding:.5rem .9rem;
  border-radius:10px; font-size:.88rem; margin-bottom:.8rem;}
.footer {text-align:center; opacity:.55; font-size:.8rem; margin-top:2rem;}
</style>
"""


def inject_styles() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
