"""
Streamlit POC: webpage-style personalization for a retail bank (LBG-inspired demo).

Not affiliated with Lloyds Banking Group. For demonstration only.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Streamlit adds the script directory to sys.path, not the repo root — so
# `import lbg_personalization` fails unless the project is installed editable.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import streamlit as st

from lbg_personalization.content import block_for_segment, theme_for_segment
from lbg_personalization.detail_views import render_detail_view
from lbg_personalization.retail_personas import RETAIL_PERSONA_ORDER, persona_by_id


def _init_session() -> None:
    if "visit_count" not in st.session_state:
        st.session_state.visit_count = 0
    if "last_segment" not in st.session_state:
        st.session_state.last_segment = None
    if "detail_view" not in st.session_state:
        st.session_state.detail_view = None


_CTA_VIEW: dict[tuple[str, str], str] = {
    ("premier", "primary"): "premier_primary",
    ("premier", "secondary"): "premier_secondary",
    ("business", "primary"): "business_primary",
    ("business", "secondary"): "business_secondary",
}

_RETAIL_PRIMARY_VIEW: dict[str, str] = {
    "retail_traits_new": "retail_app_setup",
    "retail_traits_family": "retail_spending_insights",
    "retail_traits_saver_optout": "retail_savings_goal",
}
_RETAIL_SECONDARY_VIEW: dict[str, str] = {
    "retail_traits_new": "retail_first_payment",
    "retail_traits_family": "retail_mortgage_hub",
    "retail_traits_saver_optout": "retail_isa_allowance",
}
_RETAIL_OFFER_VIEW: dict[str, dict[int, str]] = {
    "retail_traits_new": {
        0: "retail_offer_notify",
        1: "retail_offer_pin",
        2: "retail_offer_video",
        3: "retail_isa_alex_intro",
    },
    "retail_traits_family": {
        0: "retail_cashback",
        1: "retail_balance_transfer",
        2: "retail_card_controls",
        3: "retail_isa_topup_nba",
    },
    "retail_traits_saver_optout": {
        0: "retail_compare_savings",
        1: "retail_roundup",
        2: "retail_paperless",
        3: "retail_isa_fixed_jordan",
    },
}


def _retail_isa_hub_tab(retail_persona: str, *, tc) -> None:
    st.markdown(
        f'<p style="color:{tc.muted};margin:0 0 0.75rem 0;">'
        "Shortcuts align with <strong>NBA / allowance</strong> traits — open a full flow with the buttons below.</p>",
        unsafe_allow_html=True,
    )
    if retail_persona == "retail_traits_new":
        st.markdown(
            "**Alex:** NBA #1 = `COMPLETE_APP_SETUP`. **`ISA_TOPUP` also ranked** for a gentle open/top-up path "
            "(empty ISA eligible). Email marketing **on**."
        )
        a1, a2 = st.columns(2)
        with a1:
            if st.button(
                "Open or top up ISA (intro)",
                type="primary",
                use_container_width=True,
                key="isa_hub_alex_intro",
            ):
                st.session_state.detail_view = "retail_isa_alex_intro"
                st.rerun()
        with a2:
            if st.button("ISA allowance (this tax year)", use_container_width=True, key="isa_hub_alex_allow"):
                st.session_state.detail_view = "retail_isa_allowance"
                st.rerun()
    elif retail_persona == "retail_traits_family":
        st.markdown(
            "**Sam:** **NBA = `ISA_TOPUP`** — high savings propensity + household context; mortgage & card rewards on **Home**."
        )
        s1, s2 = st.columns(2)
        with s1:
            if st.button(
                "Top up ISA (NBA journey)",
                type="primary",
                use_container_width=True,
                key="isa_hub_sam_topup",
            ):
                st.session_state.detail_view = "retail_isa_topup_nba"
                st.rerun()
        with s2:
            if st.button("ISA allowance snapshot", use_container_width=True, key="isa_hub_sam_allow"):
                st.session_state.detail_view = "retail_isa_allowance"
                st.rerun()
    else:
        st.markdown(
            "**Jordan:** **NBA = `ISA_ALLOWANCE`** — servicing-first; **email marketing off**; focus on rates, round-up, **fixed ISA**."
        )
        j1, j2, j3 = st.columns(3)
        with j1:
            if st.button("ISA allowance", type="primary", use_container_width=True, key="isa_hub_jor_allow"):
                st.session_state.detail_view = "retail_isa_allowance"
                st.rerun()
        with j2:
            if st.button("Fixed-rate Cash ISA", use_container_width=True, key="isa_hub_jor_fixed"):
                st.session_state.detail_view = "retail_isa_fixed_jordan"
                st.rerun()
        with j3:
            if st.button("Compare savings (servicing)", use_container_width=True, key="isa_hub_jor_cmp"):
                st.session_state.detail_view = "retail_compare_savings"
                st.rerun()


def _render_personalized_dashboard(
    *,
    segment: str,
    persona,
    retail_persona: str | None,
    block,
    pad: str,
    _key_suffix: str,
    tc,
    include_isa_hint_in_expander: bool = False,
) -> None:
    pill = (
        f"Key: {persona.personalization_key}"
        if segment == "retail" and persona is not None
        else "Personalized view"
    )
    st.markdown(
        f'<div class="lbg-hero"><span class="lbg-pill">{pill}</span>'
        f"<h1>{block.headline}</h1><p>{block.subtext}</p></div>",
        unsafe_allow_html=True,
    )

    if segment == "retail" and persona is not None:
        with st.expander("Resolved traits (demo — SQL + ML outputs)"):
            st.markdown("**Rule-based (SQL)**")
            st.json(persona.traits_sql)
            st.markdown("**Models (scores / labels)**")
            st.json(persona.traits_ml)

    if st.session_state.visit_count > 1:
        st.caption(
            f"Simulated visits this session: **{st.session_state.visit_count}** "
            "(increments when you change segment)."
        )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="lbg-card" style="padding:{pad}">'
            f"<h3>Primary action</h3>"
            f'<p class="lbg-muted">{block.primary_cta}</p></div>',
            unsafe_allow_html=True,
        )
        if st.button(
            block.primary_cta,
            type="primary",
            use_container_width=True,
            key=f"p1_{_key_suffix}",
        ):
            if segment == "retail" and retail_persona is not None:
                st.session_state.detail_view = _RETAIL_PRIMARY_VIEW[retail_persona]
            else:
                st.session_state.detail_view = _CTA_VIEW[(segment, "primary")]
            st.rerun()
    with c2:
        st.markdown(
            f'<div class="lbg-card" style="padding:{pad}">'
            f"<h3>Secondary</h3>"
            f'<p class="lbg-muted">{block.secondary_cta}</p></div>',
            unsafe_allow_html=True,
        )
        if st.button(block.secondary_cta, use_container_width=True, key=f"p2_{_key_suffix}"):
            if segment == "retail" and retail_persona is not None:
                st.session_state.detail_view = _RETAIL_SECONDARY_VIEW[retail_persona]
            else:
                st.session_state.detail_view = _CTA_VIEW[(segment, "secondary")]
            st.rerun()
    with c3:
        st.markdown(
            f'<div class="lbg-card" style="padding:{pad}">'
            f"<h3>Quick links</h3>"
            f'<p class="lbg-muted">'
            + "<br>".join(f"• {label}" for label, _ in block.quick_links)
            + "</p></div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<h4 style="color:{tc.primary};margin:1.1rem 0 0.5rem 0;">Tailored for you</h4>',
        unsafe_allow_html=True,
    )
    cols = st.columns(len(block.offers))
    for i, (col, offer) in enumerate(zip(cols, block.offers, strict=True)):
        with col:
            st.markdown(
                f'<div class="lbg-card" style="padding:{pad}"><p class="lbg-muted" '
                f'style="margin:0">{offer}</p></div>',
                unsafe_allow_html=True,
            )
            if segment == "retail":
                label = "View details"
            else:
                label = "View offer"
            if st.button(
                label,
                key=f"offer_btn_{segment}_{_key_suffix}_{i}",
                use_container_width=True,
            ):
                if segment == "retail" and retail_persona is not None:
                    st.session_state.detail_view = _RETAIL_OFFER_VIEW[retail_persona][i]
                else:
                    st.session_state.detail_offer_text = offer
                    st.session_state.detail_view = "generic_offer"
                st.rerun()

    isa_line = (
        "\n            - **Retail ISA:** the **ISA hub** tab holds trait-aligned ISA entry points; "
        "the **fourth offer** on Home often mirrors the same NBA / servicing story.\n"
        if include_isa_hint_in_expander
        else ""
    )
    with st.expander("How this maps to real personalization"):
        st.markdown(
            f"""
            - **Retail:** pick a **profile** = a resolved **personalization key** after **SQL traits + ML**
              (see the data-flow page). Hero, CTAs, offers, and detail screens change per profile.{isa_line}
            - **Premier / business:** one template per segment (no trait sub-picker in this POC).
            - **Segment** also switches the **visual theme** (demo only; real banks stay on-brand and accessible).
            - **High contrast / compact** mimic preference-centre flags — presentation only.
            - **Session counter** increments when you **change segment** (rough stand-in for context change).
            """
        )


def _inject_css(high_contrast: bool, segment: str) -> None:
    t = theme_for_segment(segment)
    surface = t.surface
    card = "#161B22" if high_contrast else "#FFFFFF"
    text = "#F0F6FC" if high_contrast else t.text
    muted = "#8B949E" if high_contrast else t.muted
    primary = t.hc_primary if high_contrast else t.primary
    primary_dark = t.hc_primary_dark if high_contrast else t.primary_dark
    card_border = "#30363D" if high_contrast else t.card_border
    pill_bg = "#21262D" if high_contrast else t.pill_bg
    pill_fg = primary if high_contrast else t.primary
    btn_hover = primary_dark
    st.markdown(
        f"""
        <style>
        .block-container {{ padding-top: 1.25rem; max-width: 1100px;
          background: {"#0d1117" if high_contrast else surface}; }}
        .lbg-hero {{
            background: linear-gradient(135deg, {primary} 0%, {primary_dark} 100%);
            color: #fff;
            padding: 1.75rem 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.25rem;
        }}
        .lbg-hero h1 {{
            font-size: 1.65rem;
            font-weight: 700;
            margin: 0 0 0.5rem 0;
            line-height: 1.25;
        }}
        .lbg-hero p {{ margin: 0; opacity: 0.95; font-size: 1rem; }}
        .lbg-card {{
            background: {card};
            color: {text};
            border-radius: 10px;
            padding: 1rem 1.15rem;
            border: 1px solid {card_border};
            height: 100%;
        }}
        .lbg-card h3 {{
            margin: 0 0 0.5rem 0;
            font-size: 1.05rem;
            color: {text};
        }}
        .lbg-muted {{ color: {muted}; font-size: 0.9rem; }}
        .lbg-pill {{
            display: inline-block;
            background: {pill_bg};
            color: {pill_fg};
            padding: 0.2rem 0.65rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        button[data-testid="baseButton-primary"],
        button[data-testid="stBaseButton-primary"] {{
            background-color: {primary} !important;
            border-color: {primary_dark} !important;
            color: #fff !important;
        }}
        button[data-testid="baseButton-primary"]:hover,
        button[data-testid="stBaseButton-primary"]:hover {{
            background-color: {btn_hover} !important;
            border-color: {btn_hover} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="Personalization POC",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _init_session()

    st.sidebar.markdown("### Simulate visitor")
    segment = st.sidebar.selectbox(
        "Customer segment",
        options=["retail", "premier", "business"],
        format_func=lambda x: x.replace("_", " ").title(),
        help="Drives which hero, offers, and quick links are shown.",
    )
    if st.session_state.last_segment is not None and st.session_state.last_segment != segment:
        st.session_state.visit_count += 1
        st.session_state.detail_view = None
        st.session_state.pop("detail_offer_text", None)
    st.session_state.last_segment = segment

    retail_persona = None
    if segment == "retail":
        retail_persona = st.sidebar.selectbox(
            "Retail profile (from calculated traits)",
            options=list(RETAIL_PERSONA_ORDER),
            format_func=lambda k: persona_by_id(k).display_label,
            help="Each option = a resolved **personalization key** after SQL + ML in the warehouse.",
        )
        if st.session_state.get("last_retail_persona") != retail_persona:
            st.session_state.detail_view = None
            st.session_state.pop("detail_offer_text", None)
        st.session_state.last_retail_persona = retail_persona
        persona = persona_by_id(retail_persona)
        block = persona.block
    else:
        st.session_state.last_retail_persona = None
        persona = None
        block = block_for_segment(segment)

    high_contrast = st.sidebar.toggle(
        "High contrast (accessibility)",
        value=False,
        help="Adjusts colours for readability — analogous to an accessibility preference.",
    )
    compact = st.sidebar.toggle(
        "Compact information density",
        value=False,
        help="Tighter layout for users who prefer less whitespace.",
    )
    st.sidebar.caption(
        "This POC uses **session state** only — no real customer data is stored."
    )
    st.sidebar.caption(f"**Theme:** {theme_for_segment(segment).display_name}")
    if segment == "retail" and persona is not None:
        st.sidebar.caption(f"**Personalization key:** `{persona.personalization_key}`")

    _inject_css(high_contrast, segment)
    pad = "0.35rem" if compact else "0.75rem"
    _key_suffix = persona.id if segment == "retail" and persona else segment

    if st.session_state.detail_view:
        render_detail_view(st.session_state.detail_view, segment=segment)
        return

    tc = theme_for_segment(segment)
    if segment == "retail" and persona is not None:
        tab_home, tab_isa = st.tabs(["Home", "ISA hub"])
        with tab_home:
            _render_personalized_dashboard(
                segment=segment,
                persona=persona,
                retail_persona=retail_persona,
                block=block,
                pad=pad,
                _key_suffix=_key_suffix,
                tc=tc,
                include_isa_hint_in_expander=True,
            )
        with tab_isa:
            st.markdown(
                f'<h4 style="color:{tc.primary};margin:0.5rem 0 0.75rem 0;">ISA hub</h4>',
                unsafe_allow_html=True,
            )
            _retail_isa_hub_tab(retail_persona, tc=tc)
    else:
        _render_personalized_dashboard(
            segment=segment,
            persona=persona,
            retail_persona=retail_persona,
            block=block,
            pad=pad,
            _key_suffix=_key_suffix,
            tc=tc,
            include_isa_hint_in_expander=False,
        )

    st.divider()
    st.subheader("Data → traits → keys")
    st.caption(
        "How signals become a **personalization key** and **marketing templates** — reference page."
    )
    st.page_link(
        "pages/2_Data_and_Personalization_Flow.py",
        label="Open: customer data sources, Snowflake, ML, and personalization keys",
        icon="📊",
    )


if __name__ == "__main__":
    main()
