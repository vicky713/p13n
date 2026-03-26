"""Personalized copy and offers by simulated customer segment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class PersonalizedBlock:
    headline: str
    subtext: str
    primary_cta: str
    secondary_cta: str
    offers: tuple[str, ...]
    quick_links: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class SegmentVisualTheme:
    """Colours for hero, cards, and Streamlit primary buttons (demo only — not official brand)."""

    display_name: str
    primary: str
    primary_dark: str
    surface: str
    text: str
    muted: str
    pill_bg: str
    card_border: str
    hc_primary: str
    hc_primary_dark: str


# Retail: everyday banking — green family. Premier: navy + warm neutrals. Business: blue + cool neutrals.
SEGMENT_THEMES: Final[dict[str, SegmentVisualTheme]] = {
    "retail": SegmentVisualTheme(
        display_name="Retail — everyday (green)",
        primary="#006A4D",
        primary_dark="#004D38",
        surface="#F4F7F5",
        text="#1A1A1A",
        muted="#5C6670",
        pill_bg="#E8F5EF",
        card_border="#E2E8E4",
        hc_primary="#3FB950",
        hc_primary_dark="#238636",
    ),
    "premier": SegmentVisualTheme(
        display_name="Premier — relationship (navy & gold accent)",
        primary="#1B365D",
        primary_dark="#0F2440",
        surface="#F8F6F1",
        text="#1A1A1A",
        muted="#5C5C58",
        pill_bg="#EDE6DC",
        card_border="#E0D9CE",
        hc_primary="#4B8FD9",
        hc_primary_dark="#1B365D",
    ),
    "business": SegmentVisualTheme(
        display_name="Business — corporate (blue)",
        primary="#005A9C",
        primary_dark="#003D6B",
        surface="#F2F6FA",
        text="#1A1A1A",
        muted="#4A5A68",
        pill_bg="#E0ECF7",
        card_border="#C9DAEB",
        hc_primary="#58A6FF",
        hc_primary_dark="#1F6FEB",
    ),
}


def theme_for_segment(segment_key: str) -> SegmentVisualTheme:
    return SEGMENT_THEMES.get(segment_key, SEGMENT_THEMES["retail"])


# Back-compat: retail palette as a flat dict (legacy callers).
THEME: Final[dict[str, str]] = {
    "primary": SEGMENT_THEMES["retail"].primary,
    "primary_dark": SEGMENT_THEMES["retail"].primary_dark,
    "accent": "#00A878",
    "surface": SEGMENT_THEMES["retail"].surface,
    "text": SEGMENT_THEMES["retail"].text,
    "muted": SEGMENT_THEMES["retail"].muted,
}

SEGMENTS: Final[dict[str, PersonalizedBlock]] = {
    "retail": PersonalizedBlock(
        headline="Welcome back — your everyday banking, simplified",
        subtext=(
            "Based on your profile, we’re surfacing savings tools and "
            "card controls you use most."
        ),
        primary_cta="Review your spending insights",
        secondary_cta="Set a savings goal",
        offers=(
            "Cashback on selected retailers this month",
            "0% balance transfer eligibility check",
            "Mobile app: turn cards on/off instantly",
        ),
        quick_links=(
            ("Payments & transfers", "/payments"),
            ("Statements", "/statements"),
            ("Help & support", "/support"),
        ),
    ),
    "premier": PersonalizedBlock(
        headline="Premier — tailored service for how you bank",
        subtext=(
            "Your relationship manager insights and priority servicing "
            "shortcuts are highlighted below."
        ),
        primary_cta="Book a Premier review",
        secondary_cta="Explore wealth planning hub",
        offers=(
            "Dedicated support line — average answer under 2 minutes",
            "Fee-waived international transfers (limits apply)",
            "Exclusive rates on selected savings products",
        ),
        quick_links=(
            ("Premier inbox", "/premier/inbox"),
            ("Travel & insurance", "/premier/travel"),
            ("Investment overview", "/premier/investments"),
        ),
    ),
    "business": PersonalizedBlock(
        headline="Business banking — cash flow at a glance",
        subtext=(
            "We’ve prioritised invoicing, payroll, and lending tools "
            "relevant to your sector."
        ),
        primary_cta="Open cash flow dashboard",
        secondary_cta="Apply for business overdraft",
        offers=(
            "Accounting integrations — sync in one click",
            "Same-day Faster Payments (cut-off times apply)",
            "Sector playbook: managing seasonal demand",
        ),
        quick_links=(
            ("Invoices & receivables", "/business/invoices"),
            ("Payroll", "/business/payroll"),
            ("Lending", "/business/lending"),
        ),
    ),
}


def block_for_segment(segment_key: str) -> PersonalizedBlock:
    return SEGMENTS.get(segment_key, SEGMENTS["retail"])
