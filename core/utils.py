"""Framework-agnostic helpers."""

from __future__ import annotations

import hashlib
import json
import re

from PIL import Image


def format_inr(amount: float) -> str:
    """Format a rupee amount in Crores / Lakhs."""
    if amount >= 1e7:
        return f"₹ {amount / 1e7:,.2f} Cr"
    if amount >= 1e5:
        return f"₹ {amount / 1e5:,.2f} Lakhs"
    return f"₹ {amount:,.0f}"


def parse_json(text: str) -> dict:
    """Parse JSON from a model response, tolerating code fences and stray text."""
    cleaned = re.sub(r"^```(?:json)?|```$", "", (text or "").strip(), flags=re.M).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start != -1 and end > start:
            return json.loads(cleaned[start : end + 1])
        raise ValueError("Model did not return valid JSON.")


def load_image(file_like) -> Image.Image:
    """Open an uploaded image, convert to RGB and cap the size for API efficiency."""
    img = Image.open(file_like).convert("RGB")
    img.thumbnail((1600, 1600))
    return img


def bytes_seed(data: bytes) -> int:
    """Deterministic integer seed from file bytes (keeps demo output stable per image)."""
    return int(hashlib.md5(data).hexdigest()[:8], 16)
