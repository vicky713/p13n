"""Full-width detail screens opened from CTAs and offers (demo data only)."""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import streamlit as st


def _back_bar() -> None:
    if st.button("← Back to home", key="detail_back"):
        st.session_state.detail_view = None
        st.rerun()


def render_spending_insights() -> None:
    _back_bar()
    st.header("Spending insights")
    st.caption("Illustrative data for this POC — not your real account.")
    m1, m2, m3 = st.columns(3)
    m1.metric("This month", "£1,248.60", "-4.2%")
    m2.metric("vs last month", "£1,303.20", delta_color="inverse")
    m3.metric("Top category", "Groceries")
    st.subheader("Spend by category")
    st.bar_chart(
        {"Groceries": 420, "Transport": 180, "Dining out": 145, "Shopping": 210, "Bills": 293},
        height=280,
    )
    st.info(
        "In production this view would aggregate **your** transactions, "
        "respect consent, and apply the bank’s data retention rules."
    )


def render_savings_goal() -> None:
    _back_bar()
    st.header("Set a savings goal")
    st.caption("Demo planner — values are not saved beyond this browser session.")
    goal_name = st.text_input("Goal name (optional)", placeholder="e.g. Holiday fund")
    col1, col2 = st.columns(2)
    with col1:
        target = st.number_input("Target amount (£)", min_value=100, value=2000, step=100)
    with col2:
        monthly = st.number_input("Monthly contribution (£)", min_value=10, value=150, step=10)
    saved = st.slider("Already saved towards this goal (£)", 0, int(target), min(400, int(target)))
    pct = min(100, int(saved / target * 100)) if target else 0
    st.progress(pct / 100, text=f"{pct}% of goal")
    months_left = max(0, int((target - saved) / monthly)) if monthly else 0
    label = f"**{goal_name}** — " if goal_name else ""
    st.write(
        f"{label}At **£{monthly}/month**, you could reach **£{target:,.0f}** in about "
        f"**{months_left}** month(s) (illustrative)."
    )


def render_cashback_retailers() -> None:
    _back_bar()
    st.header("Cashback on selected retailers")
    st.caption("Example merchants — offers would be personalised and eligibility-based in production.")
    rows = [
        {"Retailer": "FreshMart", "Rate": "5%", "Cap": "£15/mo", "Status": "Active"},
        {"Retailer": "FuelUp", "Rate": "2%", "Cap": "£8/mo", "Status": "Activate"},
        {"Retailer": "CityRail", "Rate": "10%", "Cap": "£20/mo", "Status": "Active"},
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)
    st.toggle("Remind me before offers end", value=True, key="cashback_remind_demo")


def render_balance_transfer_check() -> None:
    _back_bar()
    st.header("0% balance transfer eligibility check")
    st.caption("Pre-check only — a real journey would run full credit and affordability checks.")
    ok_card = st.checkbox("I have a credit card with this bank", value=True)
    region = st.selectbox("Primary address region", ("England", "Scotland", "Wales", "NI"))
    ok_history = st.radio(
        "Recent payment history (demo)",
        ("No missed payments in 12 months", "Some missed payments"),
        index=0,
    )
    if st.button("Check eligibility (demo)", type="primary", key="bt_check_demo"):
        eligible = ok_card and ok_history.startswith("No missed")
        if eligible:
            st.success(
                f"You may be eligible for a **0% balance transfer** offer (demo: region **{region}**) "
                "subject to full application and underwriting. Representative example and fees would "
                "be shown next."
            )
        else:
            st.warning(
                "Based on your demo answers, a standard offer may apply — "
                "this is not a real decision."
            )
    st.divider()
    st.write(
        "**Footnote:** Balance transfers typically include a **fee** (e.g. a % of the amount). "
        "Always read the summary box before you apply."
    )


def render_card_controls() -> None:
    _back_bar()
    st.header("Card controls")
    st.caption("Demo toggles — not connected to a real card.")
    st.text_input("Card (last 4 digits)", value="•••• 4821", disabled=True)
    st.toggle("Online payments", value=True, key="card_online")
    st.toggle("Contactless", value=True, key="card_contactless")
    st.toggle("ATM withdrawals", value=True, key="card_atm")


def render_generic_offer() -> None:
    _back_bar()
    text = st.session_state.get("detail_offer_text", "").strip()
    st.header("Offer details")
    if not text:
        st.caption("No offer text in session (demo).")
        return
    st.subheader(text)
    st.caption("Illustrative breakdown — not a real offer or contract.")
    st.markdown(
        """
**What you might see next in a real journey**

- Clear **eligibility** rules and any fees  
- **Representative APR** or rate examples where regulated  
- How to **opt in or decline**, and how **marketing preferences** are honoured  
        """
    )
    st.divider()
    st.checkbox(
        "I understand this is a demo and not a real product offer",
        value=False,
        key="generic_offer_ack",
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Tell me more (demo)", type="primary", key="generic_offer_interest"):
            st.success(
                "In production this would start a guided journey or hand you to an adviser queue."
            )
    with c2:
        if st.button("Not for me (demo)", key="generic_offer_decline"):
            st.info(
                "Preference saved for this session only — a real app would update consent/marketing flags."
            )


def render_premier_review_booking() -> None:
    _back_bar()
    st.header("Book a Premier review")
    st.caption(
        "Schedule time with your Premier team (video, phone, or branch). "
        "Demo only — no appointment is created."
    )
    col_a, col_b = st.columns(2)
    with col_a:
        channel = st.radio(
            "How would you like to meet?",
            ("Video", "Telephone", "In branch"),
            horizontal=True,
        )
    with col_b:
        default_day = date.today() + timedelta(days=3)
        chosen = st.date_input("Preferred date", value=default_day, min_value=date.today())

    slot = st.selectbox(
        "Preferred time",
        (
            "09:00 – 10:00",
            "10:00 – 11:00",
            "11:00 – 12:00",
            "13:00 – 14:00",
            "14:00 – 15:00",
            "15:00 – 16:00",
        ),
    )
    topics = st.multiselect(
        "Topics you’d like to cover",
        [
            "Day-to-day banking & cards",
            "Savings & cash balances",
            "Investments & wealth (overview)",
            "Mortgages & borrowing",
            "Protection & insurance",
            "Something else",
        ],
        default=["Day-to-day banking & cards"],
    )
    notes = st.text_area(
        "Notes for your manager (optional)",
        placeholder="e.g. Prefer morning calls",
        height=68,
    )
    if st.button("Request appointment (demo)", type="primary", key="premier_book_demo"):
        topic_str = ", ".join(topics) if topics else "General review"
        st.success(
            f"**Request recorded (demo).** {channel} on **{chosen}**, **{slot}**. "
            f"Topics: {topic_str}. "
            "A real app would confirm by secure message or email."
        )
        if notes:
            st.caption(f"Your note: {notes}")
    st.info(
        "Premier reviews are **servicing** conversations. Anything that counts as **regulated advice** "
        "would follow separate agreements and disclosures."
    )


def render_premier_wealth_hub() -> None:
    _back_bar()
    st.header("Wealth planning hub")
    st.caption("Education and next steps — demo content only.")
    guides, calculators, specialists = st.tabs(["Guides", "Calculators", "Book a specialist"])
    with guides:
        for title, blurb in (
            ("Your first annual review", "What to prepare and what to expect from a Premier check-in."),
            ("ISA & pension basics", "Allowances, deadlines, and how to think about long-term pots."),
            ("Protection checklist", "Life, income, and home cover at a glance."),
        ):
            with st.expander(title):
                st.write(blurb)
    with calculators:
        st.write("**Retirement gap (illustrative)**")
        age = st.slider("Your age", 25, 70, 45)
        retire = st.slider("Target retirement age", 50, 75, 65)
        monthly = st.number_input("Monthly pension/ISA contribution (£)", min_value=0, value=400, step=50)
        years = max(0, retire - age)
        rough = monthly * 12 * max(years, 1) * 1.04 ** (min(years, 40) / 20)
        st.metric("Very rough pot estimate (demo)", f"£{rough:,.0f}")
        st.caption("Not advice — a real tool would use growth assumptions you agree to.")
    with specialists:
        st.selectbox(
            "Specialist type",
            ("Investment specialist", "Mortgage adviser", "Protection specialist", "Private banking intro"),
        )
        st.write(
            "We’ll match you to the right team and share **costs, risks, and documents** before any meeting."
        )
        if st.button("Request a call-back (demo)", key="premier_specialist_demo"):
            st.success(
                "Thanks — a real journey would offer slots and confirm by your preferred channel."
            )


def render_business_cash_flow() -> None:
    _back_bar()
    st.header("Cash flow dashboard")
    st.caption("Demo snapshot for your business account — not live data.")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Money in (30d)", "£48,320", "+6%")
    m2.metric("Money out (30d)", "£44,910", "-2%")
    m3.metric("Net", "£3,410")
    m4.metric("Runway (demo)", "~11 weeks")
    weeks = ["Wk -5", "Wk -4", "Wk -3", "Wk -2", "Wk -1", "This wk"]
    st.subheader("Weekly net cash flow")
    chart_df = pd.DataFrame({"Week": weeks, "Net (£k)": [2.1, 0.8, 3.4, -0.5, 1.9, 2.7]})
    st.bar_chart(chart_df.set_index("Week"), height=260)
    st.subheader("Upcoming (next 14 days)")
    st.dataframe(
        [
            {"Type": "In", "Counterparty": "Acme Retail Ltd", "Amount": "£12,400", "Due": "Tue"},
            {"Type": "Out", "Counterparty": "Payroll (BACS)", "Amount": "£18,200", "Due": "Thu"},
            {"Type": "Out", "Counterparty": "HMRC (VAT)", "Amount": "£4,350", "Due": "Fri"},
            {"Type": "In", "Counterparty": "Invoice #4412", "Amount": "£6,120", "Due": "Mon"},
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.toggle("Alert me if projected balance drops below £5,000", value=False, key="biz_cf_alert_demo")


def render_business_overdraft() -> None:
    _back_bar()
    st.header("Business overdraft")
    st.caption("Revolving credit for short-term gaps — demo pricing only.")
    limit_k = st.slider("Facility limit (£ thousands)", 5, 250, 50)
    limit = limit_k * 1000
    term = st.selectbox("Review period", ("12 months", "24 months"))
    illustrative_rate = 9.4 if limit_k <= 50 else 8.9
    st.metric("Illustrative annual rate (demo)", f"{illustrative_rate:.1f}% variable")
    st.write(
        f"For a **£{limit:,.0f}** limit on a **{term}** review, a real application would show "
        "**fees, security, guarantees,** and **affordability** checks."
    )
    if st.button("Start application (demo)", type="primary", key="biz_od_apply_demo"):
        st.success(
            "You’d continue to **identity, turnover evidence,** and **credit search** steps. "
            "Nothing here is submitted."
        )
    st.warning(
        "**Security:** Overdrafts may need personal guarantees or charges over assets — always read the "
        "offer pack."
    )


def render_retail_app_setup() -> None:
    _back_bar()
    st.header("Complete app setup")
    st.caption("Checklist driven by **onboarding / low-engagement** personalization.")
    st.checkbox("Biometric login enabled", value=False, key="setup_bio")
    st.checkbox("Push notifications for payments", value=True, key="setup_push")
    st.checkbox("Paperless statements", value=False, key="setup_paper")
    if st.button("Mark checklist done (demo)", key="setup_done"):
        st.success("In production this would persist to your profile.")


def render_retail_first_payment() -> None:
    _back_bar()
    st.header("Make your first payment")
    st.caption("Demo pay flow — no money moves.")
    st.number_input("Amount (£)", min_value=1.0, value=10.0, step=1.0, key="fp_amt")
    st.selectbox("Payee", ("Saved: Mum · · · 421", "New payee"), key="fp_payee")
    if st.button("Continue (demo)", type="primary", key="fp_go"):
        st.warning("Next step: **strong customer authentication** — not implemented here.")


def render_retail_mortgage_hub() -> None:
    _back_bar()
    st.header("Mortgage & home hub")
    st.caption("Surfaced because **has_active_mortgage** = true in traits.")
    m1, m2, m3 = st.columns(3)
    m1.metric("Outstanding", "£142,680")
    m2.metric("Next payment", "£1,024", "due 1 Apr")
    m3.metric("Rate type", "Fixed · 2.1y left")
    st.info("Overpayments, change date, and documents would live here in a real app.")


def render_retail_isa_allowance() -> None:
    _back_bar()
    st.header("ISA allowance this tax year")
    st.caption("Strong **savings propensity** + **servicing-first** retail profile.")
    used = 12_400
    limit = 20_000
    st.progress(min(1.0, used / limit), text=f"£{used:,} of £{limit:,} used (illustrative)")
    st.write("Room left this year: **£7,600** (demo figures).")


def render_retail_offer_notify() -> None:
    _back_bar()
    st.header("Payment alerts")
    st.toggle("Alert when balance drops below £100", value=True, key="al_bal")
    st.toggle("Alert on card spend abroad", value=False, key="al_abroad")


def render_retail_offer_pin() -> None:
    _back_bar()
    st.header("PIN & card security")
    st.write("Order a **PIN reminder** or **view PIN in app** after SCA (demo only).")
    st.button("Request PIN reminder (demo)", key="pin_rem")


def render_retail_offer_video() -> None:
    _back_bar()
    st.header("How to pay someone safely")
    st.caption("Demo placeholder — use your bank’s approved content in production.")
    st.info("Topics: **payee check**, **SCA**, **scam warnings**.")


def render_retail_compare_savings() -> None:
    _back_bar()
    st.header("Compare savings options")
    st.caption("Servicing content — no marketing email required.")
    st.dataframe(
        [
            {"Product": "Instant access", "Gross AER (demo)": "4.10%", "Access": "Same day"},
            {"Product": "1-year fixed", "Gross AER (demo)": "4.55%", "Access": "Maturity"},
        ],
        hide_index=True,
        use_container_width=True,
    )


def render_retail_roundup() -> None:
    _back_bar()
    st.header("Round-up savings")
    st.toggle("Round card purchases to the nearest £1", value=True, key="ru_en")
    st.selectbox("Destination pot", ("Holiday fund", "Rainy day"), key="ru_pot")


def render_retail_paperless() -> None:
    _back_bar()
    st.header("Paperless statements")
    st.toggle("Turn on paperless for all accounts", value=False, key="pp_on")
    st.caption("Reduces post and keeps documents in one secure place.")


def render_retail_isa_alex_intro() -> None:
    _back_bar()
    st.header("Start with an ISA")
    st.caption("**Alex profile** — `COMPLETE_APP_SETUP` is NBA #1; **`ISA_TOPUP` also surfaced** for eligible empty ISA.")
    st.info(
        "You can often open a **Cash ISA** from **£1** and top up toward your **annual allowance**. "
        "Tax treatment depends on individual circumstances — not advice."
    )
    st.number_input("First top-up amount (£)", min_value=1, value=25, step=1, key="alex_isa_amt")
    if st.button("Continue to ISA journey (demo)", type="primary", key="alex_isa_go"):
        st.success("Next: **identity**, **ISA declaration**, **funding** — not implemented here.")


def render_retail_isa_topup_nba() -> None:
    _back_bar()
    st.header("Top up your ISA")
    st.caption("**Sam profile** — **NBA = `ISA_TOPUP`** (model-ranked next action).")
    used = 14_200
    limit = 20_000
    st.progress(min(1.0, used / limit), text=f"£{used:,} of £{limit:,} allowance used (illustrative)")
    st.write(f"**Room left this tax year:** £{limit - used:,} (demo).")
    if st.button("Top up now (demo)", type="primary", key="sam_isa_top"):
        st.warning("Would continue to **payment** with SCA — demo only.")


def render_retail_isa_fixed_jordan() -> None:
    _back_bar()
    st.header("Fixed-rate Cash ISA")
    st.caption("**Jordan profile** — **servicing** reminder; **marketing email opted out**.")
    st.write(
        "Lock a **fixed rate** before the **rate-change window** closes (illustrative dates). "
        "Early withdrawal charges may apply — read the summary box."
    )
    st.metric("Illustrative 1-year fixed (demo)", "4.55% AER", "fixed until maturity")
    if st.button("See full terms (demo)", key="jordan_fixed"):
        st.info("Would open pre-contract information — not implemented.")


def render_detail_view(view: str, *, segment: str) -> None:
    if view == "retail_spending_insights":
        render_spending_insights()
    elif view == "retail_savings_goal":
        render_savings_goal()
    elif view == "retail_cashback":
        render_cashback_retailers()
    elif view == "retail_balance_transfer":
        render_balance_transfer_check()
    elif view == "retail_card_controls":
        render_card_controls()
    elif view == "retail_app_setup":
        render_retail_app_setup()
    elif view == "retail_first_payment":
        render_retail_first_payment()
    elif view == "retail_mortgage_hub":
        render_retail_mortgage_hub()
    elif view == "retail_isa_allowance":
        render_retail_isa_allowance()
    elif view == "retail_offer_notify":
        render_retail_offer_notify()
    elif view == "retail_offer_pin":
        render_retail_offer_pin()
    elif view == "retail_offer_video":
        render_retail_offer_video()
    elif view == "retail_compare_savings":
        render_retail_compare_savings()
    elif view == "retail_roundup":
        render_retail_roundup()
    elif view == "retail_paperless":
        render_retail_paperless()
    elif view == "retail_isa_alex_intro":
        render_retail_isa_alex_intro()
    elif view == "retail_isa_topup_nba":
        render_retail_isa_topup_nba()
    elif view == "retail_isa_fixed_jordan":
        render_retail_isa_fixed_jordan()
    elif view == "premier_primary":
        render_premier_review_booking()
    elif view == "premier_secondary":
        render_premier_wealth_hub()
    elif view == "business_primary":
        render_business_cash_flow()
    elif view == "business_secondary":
        render_business_overdraft()
    elif view == "generic_offer":
        render_generic_offer()
    else:
        _back_bar()
        st.error("Unknown view.")
        st.caption(view)
