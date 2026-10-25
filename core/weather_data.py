"""Weather-aware site advisories (content only; rendering lives in ui/assistant_tab.py)."""

from __future__ import annotations

WEATHER: dict[str, dict] = {
    "Normal": {
        "icon": "🌤️",
        "level": ("Normal Operations", "green"),
        "cards": [("Crane Ops", "Permitted", "Standard lift plan"),
                  ("Electrical", "Low risk", "Routine checks"),
                  ("Concreting", "Go ahead", "Standard curing")],
        "alerts": [
            "Conduct the daily toolbox talk and PPE check before shift start.",
            "Inspect scaffolds, ladders and lifting tackle; record in the site register.",
            "Standard curing: keep concrete moist for 7+ days.",
        ],
    },
    "High Wind": {
        "icon": "💨",
        "level": ("High Alert", "orange"),
        "cards": [("Crane Ops", "SUSPEND", "Above OEM wind limit (~36 km/h)"),
                  ("Work at Height", "Restricted", "Stop scaffold/roof work"),
                  ("Loose Material", "Secure", "Tie down sheets, formwork")],
        "alerts": [
            "🚫 **Suspend all crane and hoist operations** when wind exceeds the manufacturer's limit; park jib in weathervane mode.",
            "Stop work on scaffolds, roof edges and open slabs; evacuate personnel from the swing and drop zones.",
            "Secure or remove loose sheeting, formwork panels, bricks and tools; lash down stored materials.",
            "Check scaffold ties, bracing and debris netting before resuming; get a competent-person sign-off.",
        ],
    },
    "Heavy Rain": {
        "icon": "🌧️",
        "level": ("Severe Alert", "red"),
        "cards": [("Electrical", "HIGH RISK", "Shock / short-circuit hazard"),
                  ("Excavations", "Inspect", "Dewater + check shoring"),
                  ("Concreting", "Postpone", "Cover fresh pours")],
        "alerts": [
            "⚡ **Electrical hazard mitigation:** de-energise temporary distribution boards in wet areas, verify RCCB/ELCB (≤ 30 mA) function, keep cables off the ground and use IP65-rated connectors.",
            "Postpone concreting; if already placed, cover with tarpaulin to prevent washout of cement paste and surface damage.",
            "Dewater excavations and inspect shoring/trench walls for slips before re-entry.",
            "Slip hazard: restrict ladder and scaffold use, add anti-skid treads, keep walkways drained.",
            "Protect cement bags on pallets under cover; raise reinforcement off the ground to limit rust and mud contamination.",
        ],
    },
    "Extreme Heat": {
        "icon": "🔥",
        "level": ("Heat Alert", "orange"),
        "cards": [("Concrete Temp", "≤ 40 °C", "IS 7861 (Part 1) limit"),
                  ("Worker Rest", "10 min / hr", "Shade + ORS"),
                  ("Curing", "Intensive", "Wet cure 10+ days")],
        "alerts": [
            "🥵 **Heat-stress control:** provide shaded rest areas, potable chilled water/ORS, rotate heavy tasks, and schedule hard work before 11 am / after 4 pm.",
            "🧱 **Concrete curing protocol (hot weather):** pour in early morning or at night, chill aggregates and mixing water, use retarding admixtures, and keep placement temperature ≤ 40 °C.",
            "Start curing immediately: wet hessian + continuous sprinkling or curing compound; maintain for at least 10 days for blended cements.",
            "Install windbreaks / sunshades over fresh slabs to limit plastic shrinkage cracking.",
            "Monitor workers for heat exhaustion symptoms (dizziness, cramps, confusion) and stop work if the heat index is extreme.",
        ],
    },
}
