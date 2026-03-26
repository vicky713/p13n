"""Multipage: data → Snowflake → keys → templates. Run: streamlit run lbg_personalization/app.py"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

_FLOW_DIR = Path(__file__).resolve().parent.parent / "assets" / "flow"


def _flow_img(name: str) -> str:
    return str(_FLOW_DIR / name)


def _tbl_product_holding() -> pd.DataFrame:
    """Feeds trait: has_active_mortgage (join / filter on product_group + status)."""
    return pd.DataFrame(
        [
            {
                "customer_sk": "cst_h7k2…",
                "product_code": "MORT_FIX_5Y",
                "product_group": "mortgage",
                "status": "active",
                "opened_on": "2019-06-01",
                "closed_on": None,
            },
            {
                "customer_sk": "cst_h7k2…",
                "product_code": "CCA_STD",
                "product_group": "current_account",
                "status": "active",
                "opened_on": "2018-03-10",
                "closed_on": None,
            },
            {
                "customer_sk": "cst_h7k2…",
                "product_code": "CC_REWARD",
                "product_group": "credit_card",
                "status": "active",
                "opened_on": "2021-01-05",
                "closed_on": None,
            },
        ]
    )


def _tbl_crm_segment() -> pd.DataFrame:
    """Feeds trait: segment_retail_premier (CRM attribute / rule)."""
    return pd.DataFrame(
        [
            {
                "customer_sk": "cst_h7k2…",
                "segment_code": "RETAIL_CORE",
                "premier_eligible": "N",
                "relationship_mngr_id": None,
                "effective_from": "2024-01-01",
            },
        ]
    )


def _tbl_card_spend_lines() -> pd.DataFrame:
    """Feeds trait: high_card_spend_90d — `sum(amount_gbp)` over last 90 days vs threshold."""
    return pd.DataFrame(
        [
            {"customer_sk": "cst_h7k2…", "posting_date": "2025-01-02", "amount_gbp": 142.3, "mcc_group": "groceries"},
            {"customer_sk": "cst_h7k2…", "posting_date": "2025-01-19", "amount_gbp": 89.0, "mcc_group": "fuel"},
            {"customer_sk": "cst_h7k2…", "posting_date": "2025-02-04", "amount_gbp": 210.55, "mcc_group": "travel"},
            {"customer_sk": "cst_h7k2…", "posting_date": "2025-02-28", "amount_gbp": 64.2, "mcc_group": "dining"},
            {"customer_sk": "cst_h7k2…", "posting_date": "2025-03-15", "amount_gbp": 178.9, "mcc_group": "shopping"},
        ]
    )


def _tbl_marketing_consent() -> pd.DataFrame:
    """Feeds trait: marketing_email_opt_in (consent dimension)."""
    return pd.DataFrame(
        [
            {
                "customer_sk": "cst_h7k2…",
                "channel": "email",
                "is_opted_in": "Y",
                "legal_basis": "consent",
                "captured_at": "2025-01-10 11:20:00",
            },
            {
                "customer_sk": "cst_h7k2…",
                "channel": "sms",
                "is_opted_in": "N",
                "legal_basis": "consent",
                "captured_at": "2025-01-10 11:20:00",
            },
            {
                "customer_sk": "cst_h7k2…",
                "channel": "phone_outbound",
                "is_opted_in": "Y",
                "legal_basis": "legitimate_interest_servicing",
                "captured_at": "2024-08-01 09:00:00",
            },
        ]
    )


def _tbl_login_events() -> pd.DataFrame:
    """Feeds trait: digital_engagement_tier — bucket from login frequency (e.g. count in 30d)."""
    return pd.DataFrame(
        [
            {"customer_sk": "cst_h7k2…", "login_ts": "2025-03-01 07:55:00", "channel": "ios_app"},
            {"customer_sk": "cst_h7k2…", "login_ts": "2025-03-03 12:10:00", "channel": "web"},
            {"customer_sk": "cst_h7k2…", "login_ts": "2025-03-05 08:02:00", "channel": "ios_app"},
            {"customer_sk": "cst_h7k2…", "login_ts": "2025-03-08 19:40:00", "channel": "web"},
            {"customer_sk": "cst_h7k2…", "login_ts": "2025-03-12 07:30:00", "channel": "ios_app"},
            {"customer_sk": "cst_h7k2…", "login_ts": "2025-03-18 13:22:00", "channel": "web"},
        ]
    )


def _tbl_ml_feature_snapshot() -> pd.DataFrame:
    """Illustrative feature row models read for propensity, churn, NBA, clusters (bias/fairness reviewed)."""
    return pd.DataFrame(
        [
            {
                "customer_sk": "cst_h7k2…",
                "as_of_date": "2025-03-20",
                "logins_30d": 18,
                "sessions_30d": 24,
                "distinct_app_features_30d": 9,
                "card_spend_90d_gbp": 684.95,
                "n_active_products": 3,
                "has_mortgage": 1,
                "has_active_cc": 1,
                "days_since_last_login": 2,
                "email_marketing_opt_in": 1,
                "help_page_views_30d": 2,
                "savings_balance_band": "mid",
            },
        ]
    )


def _tbl_ml_scores_output() -> pd.DataFrame:
    """Example outputs (usually separate tables) — versioned for audit."""
    return pd.DataFrame(
        [
            {
                "customer_sk": "cst_h7k2…",
                "model_id": "prop_savings_v3",
                "score": 0.72,
                "effective_at": "2025-03-20",
            },
            {
                "customer_sk": "cst_h7k2…",
                "model_id": "churn_engage_v2",
                "score": 0.14,
                "effective_at": "2025-03-20",
            },
            {
                "customer_sk": "cst_h7k2…",
                "model_id": "nba_rank_v5",
                "top_action_code": "ISA_TOPUP",
                "effective_at": "2025-03-20",
            },
            {
                "customer_sk": "cst_h7k2…",
                "model_id": "behaviour_cluster_v1",
                "cluster_id": "C4_budget_conscious_active",
                "effective_at": "2025-03-20",
            },
        ]
    )


st.set_page_config(
    page_title="Data & personalization flow",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("From customer signals to personalized experiences")
st.caption(
    "Reference architecture for demo discussions — not a specific bank’s production design. "
    "Governance, consent, and PII handling must wrap every step. "
    "Icons are **generic illustrations**, not vendor logos."
)

st.header("Visual flow")
st.markdown(
    "**Sources** → **unify** → **destinations**; in Snowflake, **curated tables** (holdings, consent, spend, "
    "logins, **ML features**) are what **SQL rules and models actually analyse** to produce traits and scores, "
    "then a **personalization key** → **marketing templates**."
)

# --- Sources ---
st.subheader("1. Customer data sources")
c1, c2, c3 = st.columns(3)
with c1:
    st.image(_flow_img("icon_digital.svg"), width=100)
    st.caption("**Digital** — tags, page/app views, track & identify")
with c2:
    st.image(_flow_img("icon_forms.svg"), width=100)
    st.caption("**Forms & service** — enquiries, logged-in events")
with c3:
    st.image(_flow_img("icon_crm.svg"), width=100)
    st.caption("**Systems of record** — CRM, core banking, campaigns")

st.markdown("<div style='text-align:center;font-size:1.75rem;margin:0.25rem 0'>↓</div>", unsafe_allow_html=True)

# --- Unify ---
u1, u2, u3 = st.columns([1, 2, 1])
with u2:
    st.image(_flow_img("icon_unify.svg"), use_container_width=True)
    st.caption("**Unify & stream** — identity resolution, bronze/silver, curated tables")

st.markdown("<div style='text-align:center;font-size:1.75rem;margin:0.25rem 0'>↓</div>", unsafe_allow_html=True)

# --- Destinations ---
st.subheader("2. Destinations (examples)")
d1, d2, d3 = st.columns(3)
with d1:
    st.image(_flow_img("icon_analytics.svg"), width=100)
    st.caption("**Product analytics** — e.g. **Google Analytics** / GA4 funnels & campaigns")
with d2:
    st.image(_flow_img("icon_warehouse.svg"), width=100)
    st.caption("**Data warehouse** — **Snowflake** for SQL traits, features, audiences")
with d3:
    st.image(_flow_img("icon_cdp.svg"), width=100)
    st.caption("**CDP / reverse ETL** — sync segments to ads, email, in-app tools")

st.markdown("<div style='text-align:center;font-size:1.75rem;margin:0.25rem 0'>↓</div>", unsafe_allow_html=True)

# --- Inputs analysed before traits (replaces generic event stream) ---
st.subheader("3. Data analysed before trait calculation (illustrative)")
st.markdown(
    """
The traits below are **not** pulled from thin air — they come from **specific tables or aggregates** in the warehouse
(silver / gold layers, feature store). All IDs are **synthetic**.

Use the tabs: **SQL** shows the kind of rows each **rule-based trait** reads; **ML** shows a **feature snapshot** and
example **model outputs** (propensity, churn, NBA, clusters).
"""
)

sql_tab, ml_tab = st.tabs(["Rule-based SQL — input tables", "ML — features & example outputs"])

with sql_tab:
    st.caption("Demo customer **cst_h7k2…** — excerpts only; real jobs scan full history.")

    st.markdown("**`has_active_mortgage`** ← join / filter on **product holding**")
    st.dataframe(_tbl_product_holding(), use_container_width=True, hide_index=True)

    st.markdown("**`segment_retail_premier`** ← **CRM / segment** attribute")
    st.dataframe(_tbl_crm_segment(), use_container_width=True, hide_index=True)

    st.markdown("**`high_card_spend_90d`** ← **sum(`amount_gbp`)** over rolling 90 days vs threshold (sample lines)")
    st.dataframe(_tbl_card_spend_lines(), use_container_width=True, hide_index=True)
    st.caption("Sum of sample rows ≈ **£684.95** — compare to feature snapshot used by ML.")

    st.markdown("**`marketing_email_opt_in`** ← **consent / preference** dimension")
    st.dataframe(_tbl_marketing_consent(), use_container_width=True, hide_index=True)

    st.markdown("**`digital_engagement_tier`** ← **bucket** from login frequency (e.g. logins in last 30 days)")
    st.dataframe(_tbl_login_events(), use_container_width=True, hide_index=True)
    st.caption("Excerpt of logins; tiering uses the **full** window — e.g. **18** logins in 30d → `high` tier in SQL.")

with ml_tab:
    st.markdown(
        "**Propensity**, **churn / engagement**, **next-best-action**, and **behaviour clusters** consume "
        "**feature rows** like this (often time-stamped, versioned, with **bias / fairness** review on training)."
    )
    st.dataframe(_tbl_ml_feature_snapshot(), use_container_width=True, hide_index=True)
    st.caption(
        "Built from joins across holdings, digital behaviour, consent, and aggregates — same underlying facts as SQL, "
        "plus engineered columns."
    )
    st.markdown("##### Example scored outputs (separate tables in production)")
    st.dataframe(_tbl_ml_scores_output(), use_container_width=True, hide_index=True)
    st.caption("Each row: **model_id + version**, effective date, auditable for rollback.")

st.markdown("<div style='text-align:center;font-size:1.75rem;margin:0.25rem 0'>↓</div>", unsafe_allow_html=True)

# --- Warehouse intelligence ---
st.subheader("4. In the warehouse: trait calculation (SQL + ML)")
w1, w2 = st.columns(2)
with w1:
    st.image(_flow_img("icon_sql.svg"), width=88)
    st.markdown("**Rule-based SQL** — segments, holdings, consent flags, rolling spend…")
with w2:
    st.image(_flow_img("icon_ml.svg"), width=88)
    st.markdown("**ML & analytics** — propensity, engagement, clusters, NBA ranking…")

st.markdown("<div style='text-align:center;font-size:1.75rem;margin:0.25rem 0'>↓</div>", unsafe_allow_html=True)

# --- Key + templates ---
st.subheader("5. Key → templates")
k1, k2 = st.columns(2)
with k1:
    st.image(_flow_img("icon_key.svg"), width=88)
    st.markdown("**Personalization key** — resolved trait bundle / codes for delivery systems")
with k2:
    st.image(_flow_img("icon_templates.svg"), width=88)
    st.markdown("**Templates** — marketing-owned layouts & copy (CMS, feature flags, app config)")

st.divider()

with st.expander("Text diagram (same flow, ASCII)"):
    st.markdown(
        r"""
```
Sources → Unify / stream → GA · Snowflake · CDP
                              ↓
              Curated tables + ML feature snapshots
                              ↓
                    SQL traits + ML scores
                              ↓
              Personalization key → Experience templates
```
"""
    )

st.header("Detail: customer data sources")
st.write(
    "Typical **first-party** inputs. Collected under **privacy notice**, **consent** (where required), "
    "and **retention** policies."
)

c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("Digital properties")
    st.markdown(
        """
- **Tag / script on site & app** — page views, journeys, tech context  
- **Track & identify events** — logins, clicks, errors, funnel steps  
- **Session tooling** (if used) — often highly restricted  
        """
    )
with c2:
    st.subheader("Forms & service")
    st.markdown(
        """
- **Enquiry & lead forms** — intent, product interest  
- **Logged-in servicing** — holdings-aware events (masked in analytics layers)  
- **Secure messaging / chat** — usually **not** raw text to Snowflake without controls  
        """
    )
with c3:
    st.subheader("Systems of record")
    st.markdown(
        """
- **Core banking / CRM** — segment, products, consent flags  
- **Campaign tools** — responses, suppressions  
- **Partners** — only with contracts & lawful basis  
        """
    )

st.header("Detail: unification & streaming")
st.markdown(
    """
- **Identity resolution** — stitch anonymous device → known customer when allowed (often **logged-in** id).  
- **Streaming or batch** — **bronze / silver** layers, then **curated** tables.  
- **Destinations:** **Google Analytics** (e.g. GA4), **Snowflake**, **CDP / reverse ETL** to channels.  
    """
)

st.header("Detail: Snowflake — traits from SQL and ML")
t1, t2 = st.tabs(["Rule-based SQL", "ML / advanced analytics"])
with t1:
    st.markdown(
        """
| Trait | Example logic |
|-------|----------------|
| `has_active_mortgage` | join to product table |
| `segment_retail_premier` | CRM attribute |
| `high_card_spend_90d` | sum over window |
| `marketing_email_opt_in` | consent dimension |
| `digital_engagement_tier` | buckets from login frequency |
        """
    )
with t2:
    st.markdown(
        """
- **Propensity** — with **bias / fairness** review  
- **Churn / engagement** scores  
- **Next-best-action** ranking  
- **Behaviour clusters** — versioned, auditable outputs  
        """
    )

st.header("Personalization key (example)")
st.write(
    "Contract between **analytics** and **delivery**: which **template** or config to apply "
    "(single code or **composite**)."
)

st.code(
    """{
  "customer_id": "hashed_id_…",
  "segment": "retail",
  "trait_bundle_version": "2025-03-01",
  "keys": [
    "RETAIL_FAMILY_HIGH_ENGAGEMENT",
    "MORTGAGE_HOLDER",
    "MARKETING_OPT_IN"
  ],
  "scores": {
    "propensity_savings": 0.72,
    "engagement_tier": 3
  }
}""",
    language="json",
)

st.info(
    "CMS / feature flags map **resolved keys** to **templates**; **priority rules** when several match."
)

st.header("Marketing-owned templates")
st.markdown(
    """
**Marketing / content** owns templates per key (and channel). **Design** ensures accessibility; **legal** approves copy. **A/B tests** can wrap templates without redefining Snowflake traits.

The **app** home page in this POC shows a simplified logged-in experience once a key resolves.
    """
)

st.divider()
st.page_link("app.py", label="← Back to personalization POC (home)", icon="🏠")
