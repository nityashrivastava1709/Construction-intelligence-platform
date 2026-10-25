# 🏗️ Multimodal Construction Intelligence Platform

Skill Wallet Capstone Project 1: a Streamlit app that uses Google Gemini for construction site intelligence.
It runs in **demonstration mode** without an API key, so it always works out of the box.

## Modules

| Tab | Epic | What it does |
|---|---|---|
| 🦺 Safety & PPE Audit | 2 | Photo → PPE checklist, hazards with severity and remedies, safety score, JSON report |
| 🧱 Crack Diagnostics | 2 | Photo → defect type, crack width (mm), root causes, repairs, urgency |
| 📐 Planning & Valuation | 3 | Budget, capex, asset value (INR), steel/cement needs, milestones, 3D render prompt |
| 🌦️ Site Assistant | 5 | Weather-aware safety advisories + multi-turn engineering chatbot |

## Project structure

```
construction-intelligence-platform/
├── app.py                      # entrypoint: page config, layout, tab wiring
├── requirements.txt
├── .streamlit/
│   ├── config.toml             # server/theme settings
│   └── secrets.toml.example    # copy to secrets.toml and add GEMINI_API_KEY
├── core/                       # business logic (no Streamlit imports)
│   ├── constants.py            # severity scales, colours, model list
│   ├── prompts.py              # all LLM prompts
│   ├── gemini_service.py       # Gemini calls + automatic demo fallback
│   ├── schemas.py              # normalise model JSON into safe structures
│   ├── demo_data.py            # demonstration-mode outputs
│   ├── valuation.py            # cost / valuation / material model (tunable tables)
│   ├── rendering.py            # Pollinations AI prompt + URL builder
│   ├── weather_data.py         # advisory content per weather condition
│   └── utils.py                # format_inr, parse_json, image helpers
├── ui/                         # Streamlit presentation layer
│   ├── styles.py               # global CSS
│   ├── components.py           # pill, metric_card, item_card, demo_banner
│   ├── sidebar.py              # API key, model, architecture, feature guide
│   ├── safety_tab.py           # Tab 1
│   ├── crack_tab.py            # Tab 2
│   ├── planning_tab.py         # Tab 3
│   └── assistant_tab.py        # Tab 4
└── tests/
    └── test_core.py            # unit tests for the core package
```

**Design rule:** `core/` never imports Streamlit, and `ui/` holds no business logic. To add a feature,
add logic to `core/` and one render module to `ui/`, then register it in `app.py`.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Paste a Gemini API key (free at https://aistudio.google.com/apikey) in the sidebar, or store it in
`.streamlit/secrets.toml` as `GEMINI_API_KEY`.

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repository (`secrets.toml` is git-ignored).
2. On https://share.streamlit.io choose **New app**, select the repo, and set the main file to `app.py`.
3. Optional: under **App settings → Secrets**, add `GEMINI_API_KEY = "..."`.

## Tests

```bash
pip install pytest
pytest -q
```

## Notes

- Valuation rates in `core/valuation.py` are illustrative planning assumptions, not a registered valuation.
- AI output is advisory; verify with a licensed structural engineer / safety officer.
- If a Gemini model name is retired, update `MODELS` in `core/constants.py`.
