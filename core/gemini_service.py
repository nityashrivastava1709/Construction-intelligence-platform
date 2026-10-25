"""Gemini integration with graceful fallback to demonstration mode.

This module never imports Streamlit, so it can be unit-tested and reused.
"""

from __future__ import annotations

from dataclasses import dataclass

from PIL import Image

from .demo_data import DEMO_ANALYZERS, demo_chat
from .prompts import CHAT_SYSTEM, PROMPTS
from .schemas import NORMALISERS
from .utils import parse_json

try:
    from google import genai
    from google.genai import types

    GENAI_AVAILABLE = True
except Exception:  # library missing -> demo mode only
    GENAI_AVAILABLE = False


@dataclass
class AnalysisOutcome:
    result: dict
    is_demo: bool
    error: str | None = None  # set when a live call failed and demo data was substituted


def is_live(api_key: str) -> bool:
    return bool(api_key) and GENAI_AVAILABLE


def _gemini_json(api_key: str, model: str, prompt: str, image: Image.Image) -> dict:
    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model=model,
        contents=[prompt, image],
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.2),
    )
    return parse_json(resp.text)


def run_analysis(kind: str, api_key: str, model: str, image: Image.Image, seed: int) -> AnalysisOutcome:
    """Analyse an image. `kind` is 'safety' or 'crack'. Always returns a renderable result."""
    normalise = NORMALISERS[kind]
    if not is_live(api_key):
        return AnalysisOutcome(normalise(DEMO_ANALYZERS[kind](seed)), is_demo=True)
    try:
        return AnalysisOutcome(normalise(_gemini_json(api_key, model, PROMPTS[kind], image)), is_demo=False)
    except Exception as exc:  # network / quota / invalid key / bad JSON
        msg = f"{type(exc).__name__}: {str(exc)[:160]}"
        return AnalysisOutcome(normalise(DEMO_ANALYZERS[kind](seed)), is_demo=True, error=msg)


def chat_reply(api_key: str, model: str, weather: str, history: list[dict]) -> str:
    """Answer the last user message in `history` (list of {role, content})."""
    question = history[-1]["content"]
    if not is_live(api_key):
        return demo_chat(question, weather)
    try:
        client = genai.Client(api_key=api_key)
        contents = [
            types.Content(
                role="user" if m["role"] == "user" else "model",
                parts=[types.Part.from_text(text=m["content"])],
            )
            for m in history
        ]
        resp = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=CHAT_SYSTEM.format(weather=weather), temperature=0.4
            ),
        )
        return resp.text
    except Exception as exc:
        return (
            f"⚠️ Gemini request failed ({type(exc).__name__}). Falling back to demo reply.\n\n"
            + demo_chat(question, weather)
        )
