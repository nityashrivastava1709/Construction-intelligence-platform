"""Shared constants: severity scales, status colours, model list, labels."""

MODELS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]
DEFAULT_MODEL = MODELS[0]

# Severity scale (ordered low -> high)
SEVERITY_ORDER = ["Low", "Medium", "High", "Critical"]
SEVERITY_COLOR = {"Low": "blue", "Medium": "amber", "High": "orange", "Critical": "red"}

# Safety audit
PPE_LABELS = {
    "helmet": ("⛑️", "Safety Helmet"),
    "high_vis_vest": ("🦺", "High-Vis Vest"),
    "steel_toe_boots": ("🥾", "Steel-Toe Boots"),
    "safety_harness": ("🪢", "Safety Harness"),
}
PPE_STATUS = {
    "compliant": ("COMPLIANT", "green"),
    "non_compliant": ("NON-COMPLIANT", "red"),
    "not_visible": ("NOT VISIBLE", "grey"),
}
OVERALL_STATUS_COLOR = {
    "Compliant": "green",
    "Needs Improvement": "amber",
    "Non-Compliant": "orange",
    "Critical Risk": "red",
}

# Crack diagnostics
DEFECTS = ["Hairline", "Settlement", "Structural Shear", "Thermal Expansion", "Spalling"]
URGENCY_COLOR = {
    "Monitor": "green",
    "Repair within 30 days": "amber",
    "Repair within 7 days": "orange",
    "Immediate action": "red",
}
