"""Conceptual 3D rendering via Pollinations AI (free, keyless image endpoint)."""

from __future__ import annotations

import urllib.parse

RENDER_STYLES = [
    "3D architectural rendering",
    "Isometric 3D cutaway model",
    "Photorealistic exterior visualization",
    "Blueprint-style concept art",
]


def _stage_description(completion: int) -> str:
    if completion < 10:
        return "empty plot with site marking"
    if completion < 30:
        return "foundation and plinth work in progress"
    if completion < 60:
        return "RCC frame under construction with scaffolding and cranes"
    if completion < 85:
        return "structure complete with brick masonry and plastering underway"
    if completion < 100:
        return "near-complete building with finishing work"
    return "fully completed building, landscaped surroundings"


def build_render_prompt(structure: str, tier: str, sqft: float, completion: int, style: str) -> str:
    return (
        f"{style} of a {structure.lower()} building, approx {int(sqft)} sq ft built-up area, "
        f"Indian {tier.split(' ')[0].lower()} city setting, {_stage_description(completion)}, "
        "golden hour lighting, photorealistic, highly detailed, wide angle, 8k"
    )


def pollinations_url(prompt: str, seed: int = 42, width: int = 1024, height: int = 640) -> str:
    return (
        "https://image.pollinations.ai/prompt/"
        + urllib.parse.quote(prompt)
        + f"?width={width}&height={height}&nologo=true&seed={seed}"
    )
