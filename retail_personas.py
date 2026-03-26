"""
Three retail experiences driven by illustrative calculated traits (SQL + ML).

Aligned with the trait tables on the data-flow page — demo only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from lbg_personalization.content import PersonalizedBlock


@dataclass(frozen=True)
class RetailPersona:
    """Resolved retail template + traits that justified it (for sidebar / hero labelling)."""

    id: str
    display_label: str
    personalization_key: str
    traits_sql: dict[str, str]
    traits_ml: dict[str, str]
    block: PersonalizedBlock


RETAIL_PERSONAS: Final[dict[str, RetailPersona]] = {
    "retail_traits_new": RetailPersona(
        id="retail_traits_new",
        display_label="Alex — new customer, low digital engagement",
        personalization_key="RETAIL_ONBOARD_LOW_ENGAGEMENT_V1",
        traits_sql={
            "has_active_mortgage": "false",
            "segment_retail_premier": "RETAIL_CORE",
            "high_card_spend_90d": "false (under threshold)",
            "marketing_email_opt_in": "true",
            "digital_engagement_tier": "low",
        },
        traits_ml={
            "propensity_savings": "0.41",
            "churn_risk": "low (new)",
            "nba_top": "COMPLETE_APP_SETUP",
            "nba_also_surfaced": "ISA_TOPUP (gentle — empty ISA eligible)",
            "behaviour_cluster": "C1_dormant_web",
        },
        block=PersonalizedBlock(
            headline="Welcome — let’s finish setting up your account",
            subtext=(
                "Your traits show **early relationship** and **lighter app use** — we prioritise **setup** first, "
                "but models also surface a **soft ISA path** (`ISA_TOPUP` ranked #2) once basics are in place."
            ),
            primary_cta="Complete app setup checklist",
            secondary_cta="Make your first payment",
            offers=(
                "Turn on app notifications for payment alerts",
                "Order a debit card PIN reminder (demo)",
                "Video: how to pay someone safely",
                "ISA: open or top up from £1 (NBA also ranked — demo)",
            ),
            quick_links=(
                ("Get help", "/support"),
                ("Card & PIN", "/cards"),
                ("ISA hub (tab above)", "/isa"),
            ),
        ),
    ),
    "retail_traits_family": RetailPersona(
        id="retail_traits_family",
        display_label="Sam — mortgage, high card spend, high engagement",
        personalization_key="RETAIL_FAMILY_MORTGAGE_HIGH_SPEND_V2",
        traits_sql={
            "has_active_mortgage": "true",
            "segment_retail_premier": "RETAIL_CORE",
            "high_card_spend_90d": "true (above threshold)",
            "marketing_email_opt_in": "true",
            "digital_engagement_tier": "high",
        },
        traits_ml={
            "propensity_savings": "0.72",
            "churn_risk": "0.08",
            "nba_top": "ISA_TOPUP",
            "behaviour_cluster": "C4_budget_conscious_active",
        },
        block=PersonalizedBlock(
            headline="Welcome back — your household money in one place",
            subtext=(
                "Traits: **mortgage holder**, **high card spend (90d)**, **high digital engagement** — "
                "payments, mortgage, **card rewards**, and **ISA top-up** (`ISA_TOPUP` NBA) surface together."
            ),
            primary_cta="Review your spending insights",
            secondary_cta="View mortgage & home hub",
            offers=(
                "Cashback on selected retailers this month",
                "0% balance transfer eligibility check",
                "Mobile app: turn cards on/off instantly",
                "Top up your ISA — NBA ranked **ISA_TOPUP** for you",
            ),
            quick_links=(
                ("Payments & transfers", "/payments"),
                ("Mortgage overview", "/mortgage"),
                ("ISA hub (tab above)", "/isa"),
            ),
        ),
    ),
    "retail_traits_saver_optout": RetailPersona(
        id="retail_traits_saver_optout",
        display_label="Jordan — engaged saver, marketing email opted out",
        personalization_key="RETAIL_SERVICING_SAVER_OPTOUT_V1",
        traits_sql={
            "has_active_mortgage": "false",
            "segment_retail_premier": "RETAIL_CORE",
            "high_card_spend_90d": "false",
            "marketing_email_opt_in": "false",
            "digital_engagement_tier": "high",
        },
        traits_ml={
            "propensity_savings": "0.81",
            "churn_risk": "0.05",
            "nba_top": "ISA_ALLOWANCE",
            "behaviour_cluster": "C2_saver_digital_heavy",
        },
        block=PersonalizedBlock(
            headline="Welcome back — savings and servicing, without marketing noise",
            subtext=(
                "Traits: **high engagement**, **strong savings propensity**, **email marketing off** — "
                "**Servicing-only** tiles: ISA allowance, rate comparison, round-up, and **fixed ISA** renewal cues."
            ),
            primary_cta="Set a savings goal",
            secondary_cta="Check ISA allowance this tax year",
            offers=(
                "Compare instant-access vs fixed savings (servicing)",
                "Round-up spare change into savings",
                "Paperless statements — security & footprint",
                "Fixed-rate Cash ISA — lock rate before window closes (servicing)",
            ),
            quick_links=(
                ("Savings & ISAs", "/savings"),
                ("Statements", "/statements"),
                ("ISA hub (tab above)", "/isa"),
            ),
        ),
    ),
}

RETAIL_PERSONA_ORDER: Final[tuple[str, ...]] = tuple(RETAIL_PERSONAS.keys())


def persona_by_id(persona_id: str) -> RetailPersona:
    return RETAIL_PERSONAS.get(persona_id, RETAIL_PERSONAS["retail_traits_new"])
