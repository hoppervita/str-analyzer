"""
Short-Term Rental Investment Analyzer
Markets: Lander WY · Alpine WY · Nederland CO · Gilpin County CO
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

from market_data import (
    MARKET_STATS, PRICE_HISTORY, STR_DATA, STR_REGULATIONS,
    STR_OPERATING_COSTS, SAMPLE_PROPERTIES, ZIP_CODES,
    PERMIT_DATA, ENVIRONMENTAL_RISKS,
)
import calculations as calc

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="STR Investment Analyzer",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

MARKETS = list(MARKET_STATS.keys())

COLOR_MAP = {
    "Lander, WY":        "#2196F3",   # blue
    "Alpine, WY":        "#4CAF50",   # green
    "Nederland, CO":     "#FF9800",   # orange
    "Gilpin County, CO": "#9C27B0",   # purple
}

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🏔️ STR Analyzer")
    st.caption("Lander WY · Alpine WY · Nederland CO")
    st.divider()

    st.subheader("Mortgage Parameters")
    down_pct = st.slider("Down Payment (%)", 5, 40, 20, step=5)
    rate = st.slider("Interest Rate (%)", 5.0, 9.0, 7.0, step=0.25)
    term = st.selectbox("Loan Term", [30, 20, 15], index=0)
    closing_pct = st.slider("Closing Costs (%)", 1.5, 4.0, 2.5, step=0.5)

    st.divider()
    st.subheader("STR Assumptions")
    self_manage = st.toggle("Self-Manage (no PM fee)", value=True)
    custom_nightly = st.toggle("Override Nightly Rate", value=False)
    custom_rate = st.number_input("Custom Nightly Rate ($)", 75, 700, 150, step=5,
                                  disabled=not custom_nightly)
    custom_occ = st.toggle("Override Occupancy", value=False)
    custom_occ_val = st.slider("Custom Occupancy (%)", 20, 95, 55,
                               disabled=not custom_occ)

    st.divider()
    st.subheader("Market Filter")
    selected_markets = st.multiselect(
        "Show Markets",
        MARKETS,
        default=MARKETS,
    )
    if not selected_markets:
        selected_markets = MARKETS

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Market Overview",
    "🏠 Property Calculator",
    "📅 STR Income",
    "📋 Regulations",
    "⚖️ Market Comparison",
    "🔨 Permits & Build Difficulty",
    "⚠️ Environmental Risks",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MARKET OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("Market Overview")

    # ── KPI cards ─────────────────────────────────────────────────────────────
    cols = st.columns(len(selected_markets))
    for i, mkt in enumerate(selected_markets):
        ms = MARKET_STATS[mkt]
        str_d = STR_DATA[mkt]
        with cols[i]:
            st.markdown(f"### {mkt}")
            st.metric("Median Home Price", f"${ms['median_price']:,.0f}",
                      f"+{ms['yoy_appreciation']*100:.1f}% YoY")
            st.metric("$/sqft", f"${ms['price_per_sqft']}")
            st.metric("Days on Market", f"{ms['dom']} days")
            st.metric("Avg STR Revenue/yr", f"${str_d['avg_annual_revenue']:,.0f}")
            st.metric("Avg Nightly Rate", f"${str_d['avg_nightly_rate']}")
            st.metric("Avg Occupancy", f"{str_d['avg_occupancy']*100:.0f}%")
            st.caption(ms["description"])

    st.divider()

    # ── Price history chart ────────────────────────────────────────────────────
    st.subheader("Median Home Price History")
    fig = go.Figure()
    for mkt in selected_markets:
        hist = PRICE_HISTORY[mkt]
        years = list(hist.keys())
        prices = list(hist.values())
        fig.add_trace(go.Scatter(
            x=years, y=prices, name=mkt, mode="lines+markers",
            line=dict(color=COLOR_MAP[mkt], width=3),
            marker=dict(size=8),
            hovertemplate="<b>%{fullData.name}</b><br>%{x}: $%{y:,.0f}<extra></extra>",
        ))
    fig.update_layout(
        yaxis_tickprefix="$", yaxis_tickformat=",",
        height=380, margin=dict(t=20, b=20),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Price per sqft + inventory ─────────────────────────────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Price per Sqft Comparison")
        fig2 = go.Figure(go.Bar(
            x=[m for m in selected_markets],
            y=[MARKET_STATS[m]["price_per_sqft"] for m in selected_markets],
            marker_color=[COLOR_MAP[m] for m in selected_markets],
            text=[f"${MARKET_STATS[m]['price_per_sqft']}" for m in selected_markets],
            textposition="outside",
        ))
        fig2.update_layout(yaxis_title="$/sqft", height=300, margin=dict(t=10, b=10),
                           yaxis_tickprefix="$")
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        st.subheader("Market Snapshot")
        rows = []
        for mkt in selected_markets:
            ms = MARKET_STATS[mkt]
            rows.append({
                "Market": mkt,
                "Median Price": f"${ms['median_price']:,.0f}",
                "$/sqft": f"${ms['price_per_sqft']}",
                "DOM": ms["dom"],
                "Inventory": ms["inventory"],
                "YoY Apprec.": f"{ms['yoy_appreciation']*100:.1f}%",
                "Prop Tax Rate": f"{ms['property_tax_rate']*100:.2f}%",
                "HOA Common": "Yes" if ms["hoa_common"] else "No",
            })
        st.dataframe(pd.DataFrame(rows).set_index("Market"), use_container_width=True)

    # ── Tourism & demand drivers ───────────────────────────────────────────────
    st.subheader("Tourism & STR Demand Drivers")
    cols2 = st.columns(len(selected_markets))
    for i, mkt in enumerate(selected_markets):
        with cols2[i]:
            st.markdown(f"**{mkt}**")
            for driver in STR_DATA[mkt]["tourism_drivers"]:
                st.markdown(f"- {driver}")
            st.caption(f"Peak: {', '.join(STR_DATA[mkt]['peak_seasons'])}")
            st.caption(f"Slow: {', '.join(STR_DATA[mkt]['slow_seasons'])}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PROPERTY CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("Property Investment Calculator")
    st.caption("Enter a purchase price to see full financial analysis.")

    col_left, col_right = st.columns([1, 2])

    with col_left:
        market_sel = st.selectbox("Market", selected_markets, key="calc_market")
        ms = MARKET_STATS[market_sel]
        str_d = STR_DATA[market_sel]
        costs = STR_OPERATING_COSTS[market_sel]

        # Market-specific alerts
        if market_sel == "Nederland, CO":
            st.error(
                "⚠️ **Owner-Occupancy Requirement**: Nederland only allows STR of residential "
                "properties if it is your **primary residence**. Non-owner-occupants may only "
                "STR in CBD/GC commercial zones. Verify zoning before purchasing."
            )
            st.warning(
                "🔥 **Wildfire Insurance**: Nederland is a high-risk wildfire zone. Most major "
                "carriers won't write new policies. Budget **$5,000–$10,000+/yr**. "
                "**Verify insurability before making any offer.**"
            )
        if market_sel == "Alpine, WY":
            st.warning(
                "🏘️ **HOA Risk**: Many Alpine properties are in HOA subdivisions (Alpine Meadows, "
                "Alpine Village Resort). STR may be restricted by CC&Rs. **Check HOA docs before buying.**"
            )
            if str_d.get("pct_30day_minimum", 0) > 0.3:
                st.info(
                    f"ℹ️ **30-Day Minimums**: {str_d['pct_30day_minimum']*100:.0f}% of current Alpine "
                    f"listings require 30+ night minimum stays — many are MTR, not true nightly STR. "
                    f"The true nightly-rental market may be smaller than listing counts suggest."
                )
        if market_sel == "Gilpin County, CO":
            st.success(
                "✅ **Investor-Friendly**: No owner-occupancy requirement — pure investors CAN STR "
                "residential properties. Much lighter permitting burden than Boulder County."
            )
            st.error(
                "⛏️ **Mine Subsidence**: Gilpin County sits on extensive historic underground mine workings. "
                "Geotechnical investigation is critical before purchase. Some areas have documented subsidence."
            )
            st.error(
                "☢️ **Radon**: Gilpin County is a Zone 1 radon area (highest risk). "
                "Assume mitigation needed — budget $800–$2,500. Mandatory test during inspection."
            )
            st.warning(
                "🔥 **Wildfire Insurance**: High-risk zone — budget $4,000–$8,000+/yr. "
                "Verify insurability before making any offer."
            )

        # Quick-fill from sample properties
        st.markdown("**Quick-fill from sample listings:**")
        samples = SAMPLE_PROPERTIES[market_sel]
        sample_labels = [f"{s['label']} — ${s['price']:,.0f}" for s in samples]
        sample_sel = st.selectbox("Sample Property", ["Custom"] + sample_labels, key="sample_sel")
        if sample_sel != "Custom":
            idx = sample_labels.index(sample_sel)
            default_price = samples[idx]["price"]
            default_sqft = samples[idx]["sqft"]
        else:
            default_price = ms["median_price"]
            default_sqft = ms["median_sqft"]

        purchase_price = st.number_input("Purchase Price ($)", 100_000, 3_000_000,
                                         value=default_price, step=5_000,
                                         format="%d", key="purchase_price")
        sqft = st.number_input("Square Feet", 500, 6_000, value=default_sqft,
                               step=50, key="sqft")
        st.caption(f"Implied $/sqft: **${purchase_price/sqft:.0f}** "
                   f"(market avg: ${ms['price_per_sqft']})")

        # After-repair value (for remodel buyers like Trevor)
        st.markdown("---")
        remodel_mode = st.toggle("Remodel / Value-Add Analysis", value=False)
        if remodel_mode:
            arv = st.number_input("After-Repair Value ($)", purchase_price,
                                  int(purchase_price * 1.6), value=int(purchase_price * 1.15),
                                  step=5_000, format="%d")
            reno_cost = st.number_input("Renovation Budget ($)", 0, 500_000,
                                        50_000, step=5_000, format="%d")
        else:
            arv = purchase_price
            reno_cost = 0

    with col_right:
        # ── Core mortgage math ─────────────────────────────────────────────────
        eff_price = purchase_price + reno_cost
        monthly_pmt = calc.monthly_mortgage(eff_price, down_pct, rate, term)
        cash_to_close = calc.total_cash_to_close(purchase_price, down_pct, closing_pct) + reno_cost

        # ── STR income ─────────────────────────────────────────────────────────
        nightly = custom_rate if custom_nightly else str_d["avg_nightly_rate"]
        occ = (custom_occ_val / 100) if custom_occ else str_d["avg_occupancy"]
        gross_monthly = calc.str_monthly_revenue(nightly, occ, costs["platform_fee_pct"])

        expenses = calc.str_monthly_expenses(
            arv, market_sel, gross_monthly, self_manage,
            costs["avg_stays_per_mo"], costs
        )
        prop_tax = calc.property_tax_monthly(arv, ms["property_tax_rate"])
        total_expenses_monthly = sum(expenses.values()) + prop_tax

        net_monthly = gross_monthly - total_expenses_monthly
        cash_flow = net_monthly - monthly_pmt

        # ── KPI strip ─────────────────────────────────────────────────────────
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Monthly Mortgage", f"${monthly_pmt:,.0f}")
        k2.metric("STR Net Revenue", f"${net_monthly:,.0f}/mo",
                  help="After platform fee and all operating costs, before mortgage")
        cf_delta = f"{'✅' if cash_flow >= 0 else '⚠️'} vs mortgage"
        k3.metric("Monthly Cash Flow", f"${cash_flow:,.0f}", cf_delta,
                  delta_color="normal" if cash_flow >= 0 else "inverse")
        k4.metric("Cash to Close", f"${cash_to_close:,.0f}")

        # ── Cash flow waterfall ────────────────────────────────────────────────
        st.subheader("Monthly Cash Flow Breakdown")
        categories = (
            ["STR Gross Revenue"]
            + [f"– {k}" for k in expenses.keys()]
            + ["– Property Tax", "– Mortgage Payment"]
        )
        amounts = (
            [gross_monthly]
            + [-v for v in expenses.values()]
            + [-prop_tax, -monthly_pmt]
        )
        colors = ["#4CAF50" if a > 0 else "#F44336" for a in amounts]

        running = 0
        measures = []
        for i, a in enumerate(amounts):
            if i == 0:
                measures.append("absolute")
            else:
                measures.append("relative")

        fig_wf = go.Figure(go.Waterfall(
            orientation="v",
            measure=measures,
            x=categories,
            y=amounts,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#4CAF50"}},
            decreasing={"marker": {"color": "#F44336"}},
            totals={"marker": {"color": "#2196F3"}},
            texttemplate="$%{y:,.0f}",
            textposition="outside",
        ))
        fig_wf.update_layout(height=380, margin=dict(t=10, b=10),
                             yaxis_tickprefix="$", yaxis_tickformat=",",
                             showlegend=False)
        st.plotly_chart(fig_wf, use_container_width=True)

        # ── Break-even occupancy ───────────────────────────────────────────────
        fixed_monthly = total_expenses_monthly - expenses.get("Management", 0)
        be_occ = calc.break_even_occupancy(monthly_pmt, fixed_monthly,
                                           nightly, costs["platform_fee_pct"])
        be_pct = min(be_occ * 100, 100)

        st.subheader("Break-Even Occupancy")
        col_be1, col_be2 = st.columns([2, 1])
        with col_be1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=occ * 100,
                delta={"reference": be_pct, "valueformat": ".1f",
                       "prefix": "vs break-even: "},
                number={"suffix": "%", "valueformat": ".1f"},
                title={"text": "Current Occupancy vs Break-Even"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": COLOR_MAP.get(market_sel, "#2196F3")},
                    "steps": [
                        {"range": [0, be_pct], "color": "#FFCCCC"},
                        {"range": [be_pct, 100], "color": "#CCFFCC"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 3},
                        "thickness": 0.8,
                        "value": be_pct,
                    },
                },
            ))
            fig_gauge.update_layout(height=250, margin=dict(t=30, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)
        with col_be2:
            st.markdown(f"""
            | | |
            |---|---|
            | **Break-even occupancy** | {be_pct:.1f}% |
            | **Current assumption** | {occ*100:.1f}% |
            | **Market avg occupancy** | {str_d['avg_occupancy']*100:.0f}% |
            | **Market peak occupancy** | {str_d['peak_occupancy']*100:.0f}% |
            | **Nights needed/mo** | {be_occ*30:.1f} |
            """)
            if be_occ <= str_d["avg_occupancy"]:
                st.success("✅ Break-even below market average — strong case")
            elif be_occ <= str_d["peak_occupancy"]:
                st.warning("⚠️ Achievable but requires above-avg performance")
            else:
                st.error("❌ Break-even exceeds even peak season occupancy")

        # ── Expense breakdown pie ──────────────────────────────────────────────
        st.subheader("Monthly Expense Breakdown")
        all_exp = dict(expenses)
        all_exp["Property Tax"] = prop_tax
        all_exp["Mortgage P&I"] = monthly_pmt
        fig_pie = go.Figure(go.Pie(
            labels=list(all_exp.keys()),
            values=list(all_exp.values()),
            hole=0.4,
            textinfo="label+percent",
        ))
        fig_pie.update_layout(height=320, margin=dict(t=10, b=10),
                              showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

        # ── Remodel equity ─────────────────────────────────────────────────────
        if remodel_mode:
            st.subheader("Remodel Value-Add")
            instant_equity = arv - (purchase_price + reno_cost)
            col_r1, col_r2 = st.columns(2)
            col_r1.metric("All-In Cost", f"${purchase_price + reno_cost:,.0f}")
            col_r1.metric("After-Repair Value", f"${arv:,.0f}")
            col_r2.metric("Instant Equity Created", f"${instant_equity:,.0f}",
                          delta_color="normal" if instant_equity > 0 else "inverse")
            col_r2.metric("Return on Reno", f"{instant_equity/reno_cost*100:.0f}%" if reno_cost > 0 else "N/A")

    # ── Amortization / appreciation projection ─────────────────────────────────
    st.divider()
    st.subheader(f"10-Year Projection — {market_sel}")
    proj_years = 10
    amort = calc.amortization_schedule(eff_price, down_pct, rate, term)[:proj_years]
    apprec = calc.price_appreciation(arv, ms["yoy_appreciation"], proj_years)

    cf_annual = cash_flow * 12
    fig_proj = make_subplots(specs=[[{"secondary_y": True}]])

    years_x = list(range(1, proj_years + 1))
    fig_proj.add_trace(go.Scatter(
        x=years_x, y=apprec[1:],
        name="Home Value", mode="lines+markers",
        line=dict(color="#4CAF50", width=2),
    ), secondary_y=False)
    fig_proj.add_trace(go.Scatter(
        x=years_x, y=[a["balance"] for a in amort],
        name="Loan Balance", mode="lines+markers",
        line=dict(color="#F44336", width=2, dash="dash"),
    ), secondary_y=False)
    fig_proj.add_trace(go.Bar(
        x=years_x,
        y=[cf_annual * y for y in years_x],
        name="Cumulative Cash Flow",
        marker_color="#2196F3", opacity=0.6,
    ), secondary_y=True)

    fig_proj.update_layout(height=380, margin=dict(t=10, b=10),
                           hovermode="x unified",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02))
    fig_proj.update_yaxes(tickprefix="$", tickformat=",", secondary_y=False)
    fig_proj.update_yaxes(tickprefix="$", tickformat=",", secondary_y=True,
                          title_text="Cum. Cash Flow")
    st.plotly_chart(fig_proj, use_container_width=True)

    # ── Summary ROI table ──────────────────────────────────────────────────────
    equity_yr5 = apprec[5] - amort[4]["balance"]
    equity_yr10 = apprec[10] - amort[9]["balance"]
    init_invest = cash_to_close

    summary_df = pd.DataFrame({
        "Year 5": {
            "Home Value": f"${apprec[5]:,.0f}",
            "Loan Balance": f"${amort[4]['balance']:,.0f}",
            "Equity": f"${equity_yr5:,.0f}",
            "Cumulative Cash Flow": f"${cf_annual*5:,.0f}",
            "Total Return": f"${equity_yr5 + cf_annual*5 - init_invest:,.0f}",
        },
        "Year 10": {
            "Home Value": f"${apprec[10]:,.0f}",
            "Loan Balance": f"${amort[9]['balance']:,.0f}",
            "Equity": f"${equity_yr10:,.0f}",
            "Cumulative Cash Flow": f"${cf_annual*10:,.0f}",
            "Total Return": f"${equity_yr10 + cf_annual*10 - init_invest:,.0f}",
        },
    })
    st.dataframe(summary_df, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — STR INCOME DEEP-DIVE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.header("STR Income Deep-Dive")

    # ── Monthly seasonality chart ──────────────────────────────────────────────
    st.subheader("Estimated Monthly STR Revenue by Market")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig_season = go.Figure()
    for mkt in selected_markets:
        rev = STR_DATA[mkt]["monthly_revenue"]
        fig_season.add_trace(go.Bar(
            name=mkt,
            x=months,
            y=[rev[m] for m in months],
            marker_color=COLOR_MAP[mkt],
            opacity=0.85,
            hovertemplate="<b>%{fullData.name}</b><br>%{x}: $%{y:,.0f}<extra></extra>",
        ))
    fig_season.update_layout(
        barmode="group",
        height=380,
        yaxis_tickprefix="$", yaxis_tickformat=",",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=10, b=10),
    )
    st.plotly_chart(fig_season, use_container_width=True)

    # ── Revenue sensitivity table ──────────────────────────────────────────────
    st.subheader("Revenue Sensitivity — Nightly Rate × Occupancy")
    str_market = st.selectbox("Market", selected_markets, key="str_market")
    str_d2 = STR_DATA[str_market]

    nightly_rates = [100, 125, 150, 175, 200, 225, 250, 300, 350]
    occupancies = [0.35, 0.45, 0.55, 0.65, 0.75, 0.85]

    matrix = []
    for occ_val in occupancies:
        row = {}
        for nr in nightly_rates:
            monthly = nr * 30 * occ_val * (1 - STR_OPERATING_COSTS[str_market]["platform_fee_pct"])
            row[f"${nr}/night"] = f"${monthly:,.0f}"
        matrix.append(row)

    df_matrix = pd.DataFrame(matrix, index=[f"{int(o*100)}% occ" for o in occupancies])
    st.dataframe(df_matrix, use_container_width=True)
    st.caption(f"Gross monthly after {STR_OPERATING_COSTS[str_market]['platform_fee_pct']*100:.0f}% platform fee. "
               f"Market avg nightly: **${str_d2['avg_nightly_rate']}** | "
               f"Market avg occupancy: **{str_d2['avg_occupancy']*100:.0f}%**")

    # ── Occupancy vs mortgage price comparison ─────────────────────────────────
    st.subheader("Can STR Cover the Mortgage? — Occupancy Required by Home Price")
    str_mkt3 = st.selectbox("Market", selected_markets, key="str_mkt3")
    ms3 = MARKET_STATS[str_mkt3]
    str_d3 = STR_DATA[str_mkt3]
    costs3 = STR_OPERATING_COSTS[str_mkt3]

    price_range = list(range(
        ms3["price_range_low"],
        ms3["price_range_high"] + 1,
        int((ms3["price_range_high"] - ms3["price_range_low"]) / 20)
    ))

    nightly3 = custom_rate if custom_nightly else str_d3["avg_nightly_rate"]

    be_occs = []
    monthly_pmts = []
    for p in price_range:
        pmt = calc.monthly_mortgage(p, down_pct, rate, term)
        monthly_pmts.append(pmt)
        fixed_exp = (
            costs3["cleaning_per_stay"] * costs3["avg_stays_per_mo"]
            + costs3["supplies_monthly"]
            + costs3["utilities_monthly"]
            + costs3["insurance_annual"] / 12
            + p * costs3["maintenance_pct"] / 12
            + p * ms3["property_tax_rate"] / 12
        )
        be = calc.break_even_occupancy(pmt, fixed_exp, nightly3, costs3["platform_fee_pct"])
        be_occs.append(min(be * 100, 120))

    fig_be = go.Figure()
    fig_be.add_trace(go.Scatter(
        x=price_range, y=be_occs,
        name="Break-Even Occupancy",
        mode="lines", fill="tozeroy",
        line=dict(color=COLOR_MAP.get(str_mkt3, "#2196F3"), width=3),
        hovertemplate="Price: $%{x:,.0f}<br>Break-Even Occ: %{y:.1f}%<extra></extra>",
    ))
    fig_be.add_hline(y=str_d3["avg_occupancy"] * 100, line_dash="dash",
                     line_color="green",
                     annotation_text=f"Market avg occ ({str_d3['avg_occupancy']*100:.0f}%)",
                     annotation_position="right")
    fig_be.add_hline(y=str_d3["peak_occupancy"] * 100, line_dash="dot",
                     line_color="orange",
                     annotation_text=f"Peak occ ({str_d3['peak_occupancy']*100:.0f}%)",
                     annotation_position="right")
    fig_be.add_hline(y=100, line_color="red", line_width=1,
                     annotation_text="100% (impossible)",
                     annotation_position="right")
    fig_be.update_layout(
        xaxis_title="Purchase Price",
        yaxis_title="Break-Even Occupancy (%)",
        xaxis_tickprefix="$", xaxis_tickformat=",",
        height=400, margin=dict(t=10, b=10),
        yaxis_range=[0, 110],
    )
    st.plotly_chart(fig_be, use_container_width=True)

    # Find max affordable price
    for i, (p, be) in enumerate(zip(price_range, be_occs)):
        if be > str_d3["avg_occupancy"] * 100:
            max_price_avg = price_range[max(0, i - 1)]
            break
    else:
        max_price_avg = price_range[-1]

    for i, (p, be) in enumerate(zip(price_range, be_occs)):
        if be > str_d3["peak_occupancy"] * 100:
            max_price_peak = price_range[max(0, i - 1)]
            break
    else:
        max_price_peak = price_range[-1]

    col_msg1, col_msg2 = st.columns(2)
    col_msg1.info(f"**At {str_mkt3} avg occupancy ({str_d3['avg_occupancy']*100:.0f}%):** "
                  f"STR covers mortgage up to ~**${max_price_avg:,.0f}** purchase price "
                  f"at ${nightly3}/night nightly rate, {down_pct}% down, {rate}% rate.")
    col_msg2.warning(f"**At peak occupancy ({str_d3['peak_occupancy']*100:.0f}%):** "
                     f"STR covers mortgage up to ~**${max_price_peak:,.0f}**. "
                     f"Relying on peak occupancy is risky — plan for average.")

    # ── STR performance tiers ─────────────────────────────────────────────────
    st.subheader("STR Performance Tiers by Market (AirROI 2024–2025)")
    tier_data = {
        "Lander, WY": {
            "Top 10%":    {"ADR": "$316+", "Occupancy": "77%+", "Annual Revenue": "$83,749"},
            "Top 25%":    {"ADR": "$214+", "Occupancy": "64%+", "Annual Revenue": "~$52,000"},
            "Median":     {"ADR": "$154",  "Occupancy": "45%",  "Annual Revenue": "$26,636"},
            "Bottom 25%": {"ADR": "$119",  "Occupancy": "28%",  "Annual Revenue": "~$12,000"},
            "YoY Trend":  "-7.4% (declining)",
        },
        "Alpine, WY": {
            "Top 10%":    {"ADR": "$576+", "Occupancy": "73%+", "Annual Revenue": "~$103,500"},
            "Top 25%":    {"ADR": "$449+", "Occupancy": "54%+", "Annual Revenue": "~$68,000"},
            "Median":     {"ADR": "$305",  "Occupancy": "37%",  "Annual Revenue": "$41,057"},
            "Bottom 25%": {"ADR": "$197",  "Occupancy": "21%",  "Annual Revenue": "~$16,000"},
            "YoY Trend":  "-7.8% (declining)",
        },
        "Nederland, CO": {
            "Top 10%":    {"ADR": "$573+", "Occupancy": "79%+", "Annual Revenue": "$189,610"},
            "Top 25%":    {"ADR": "$348+", "Occupancy": "65%+", "Annual Revenue": "~$85,000"},
            "Median":     {"ADR": "$213",  "Occupancy": "48%",  "Annual Revenue": "$44,338"},
            "Bottom 25%": {"ADR": "$150",  "Occupancy": "31%",  "Annual Revenue": "~$18,000"},
            "YoY Trend":  "+40.5% ✅ (growing strongly)",
        },
        "Gilpin County, CO": {
            "Top 10%":    {"ADR": "$350+", "Occupancy": "72%+", "Annual Revenue": "~$95,000"},
            "Top 25%":    {"ADR": "$265+", "Occupancy": "58%+", "Annual Revenue": "~$55,000"},
            "Median":     {"ADR": "$210",  "Occupancy": "48%",  "Annual Revenue": "~$37,000"},
            "Bottom 25%": {"ADR": "$140",  "Occupancy": "28%",  "Annual Revenue": "~$14,000"},
            "YoY Trend":  "Insufficient data (newer market)",
        },
    }
    tier_cols = st.columns(len(selected_markets))
    for i, mkt in enumerate(selected_markets):
        with tier_cols[i]:
            st.markdown(f"**{mkt}**")
            td = tier_data[mkt]
            for tier, vals in td.items():
                if tier == "YoY Trend":
                    st.caption(f"📈 YoY: {vals}")
                else:
                    st.markdown(
                        f"**{tier}**: {vals['ADR']}/night · {vals['Occupancy']} occ · {vals['Annual Revenue']}/yr"
                    )

    st.divider()

    # ── Operating cost breakdown ───────────────────────────────────────────────
    st.subheader("STR Operating Costs Reference")
    cost_rows = []
    for mkt in selected_markets:
        c = STR_OPERATING_COSTS[mkt]
        ms_c = MARKET_STATS[mkt]
        cost_rows.append({
            "Market": mkt,
            "PM Fee": f"{c['mgmt_fee_pct']*100:.0f}% of rev" if not self_manage else "Self-managed",
            "Cleaning/stay": f"${c['cleaning_per_stay']}",
            "Supplies/mo": f"${c['supplies_monthly']}",
            "Utilities/mo": f"${c['utilities_monthly']}",
            "STR Insurance/yr": f"${c['insurance_annual']:,.0f}",
            "Maintenance": f"{c['maintenance_pct']*100:.1f}% of value/yr",
            "Platform Fee": f"{c['platform_fee_pct']*100:.0f}%",
        })
    st.dataframe(pd.DataFrame(cost_rows).set_index("Market"), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — REGULATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.header("STR Regulations & Compliance")

    for mkt in selected_markets:
        reg = STR_REGULATIONS[mkt]
        risk_colors = {"Very Low": "green", "Low": "green",
                       "Moderate": "orange", "Moderate-High (for investors)": "red", "High": "red"}
        risk_color = risk_colors.get(reg["regulatory_risk"], "gray")

        with st.expander(f"**{mkt}** — {reg['status']} | Risk: :{risk_color}[{reg['regulatory_risk']}]",
                         expanded=True):
            col_r1, col_r2, col_r3 = st.columns(3)
            col_r1.metric("License Required", "Yes" if reg["license_required"] else "No")
            col_r1.metric("License Fee", f"${reg['license_fee']}/yr" if reg["license_required"] else "N/A")
            col_r1.metric("Owner-Occupancy Required", "Yes" if reg["owner_occupancy_required"] else "No")
            col_r2.metric("Lodging Tax Rate", f"{reg['lodging_tax_rate']*100:.1f}%")
            col_r2.metric("Platform Collects Tax", "Yes" if reg["platform_collects_tax"] else "Partially")
            col_r2.metric("Unit Cap", str(reg["cap_on_units"]) if reg["cap_on_units"] else "None")
            col_r3.metric("Regulatory Risk", reg["regulatory_risk"])
            col_r3.caption(reg["risk_explanation"])

            st.markdown("**Key Notes:**")
            for note in reg["notes"]:
                st.markdown(f"- {note}")

            st.caption(f"📋 Reference: {reg['ordinance_ref']}")
            st.caption(f"📞 Contact: {reg['contact']}")

    st.divider()
    st.subheader("Tax Comparison")
    tax_rows = []
    for mkt in selected_markets:
        reg = STR_REGULATIONS[mkt]
        tax_rows.append({
            "Market": mkt,
            "State Income Tax": "None (WY)" if "WY" in mkt else "4.4% (CO)",
            "Lodging Tax (est.)": f"{reg['lodging_tax_rate']*100:.1f}%",
            "Platform Collects?": "Yes" if reg["platform_collects_tax"] else "Partially",
            "Regulatory Risk": reg["regulatory_risk"],
        })
    st.dataframe(pd.DataFrame(tax_rows).set_index("Market"), use_container_width=True)

    st.info("""
    **Important:** Always verify current regulations directly with the relevant local government before purchasing.
    STR regulations can change quickly. Wyoming markets generally have lower regulatory risk due to the state's
    historically hands-off approach to property rights. Colorado's regulatory environment is more active.

    **Recommended steps before buying:**
    1. Contact the city/county planning department to confirm STR is allowed at the specific parcel
    2. Check HOA CC&Rs if property is in a subdivision (especially Alpine, WY)
    3. Register with the state for sales/lodging tax collection
    4. Obtain STR-specific insurance (standard homeowner's won't cover commercial rental activity)
    """)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — MARKET COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.header("Side-by-Side Market Comparison")

    # ── Radar chart ───────────────────────────────────────────────────────────
    st.subheader("Market Scorecard")

    # Normalize metrics 0-10 for radar
    def norm(val, lo, hi, invert=False):
        n = (val - lo) / (hi - lo) * 10
        return 10 - n if invert else n

    radar_categories = [
        "Affordability", "STR Revenue",
        "Occupancy", "Appreciation",
        "Low Regulation", "Tourism Draw", "Low Competition"
    ]

    radar_fig = go.Figure()
    for mkt in selected_markets:
        ms_r = MARKET_STATS[mkt]
        str_r = STR_DATA[mkt]
        reg_risk = {"Very Low": 10, "Low": 8, "Moderate": 5,
                    "Moderate-High (for investors)": 3, "High": 2}.get(
            STR_REGULATIONS[mkt]["regulatory_risk"], 5
        )
        scores = [
            max(0, min(10, norm(ms_r["median_price"], 180_000, 1_400_000, invert=True))),
            max(0, min(10, norm(str_r["avg_annual_revenue"], 20_000, 80_000))),
            max(0, min(10, norm(str_r["avg_occupancy"], 0.35, 0.75))),
            max(0, min(10, norm(ms_r["yoy_appreciation"], 0.03, 0.15))),
            reg_risk,
            max(0, min(10, norm(len(str_r["tourism_drivers"]), 4, 10))),
            max(0, min(10, norm(str_r["active_listings"], 30, 130, invert=True))),
        ]
        radar_fig.add_trace(go.Scatterpolar(
            r=scores + [scores[0]],
            theta=radar_categories + [radar_categories[0]],
            fill="toself",
            name=mkt,
            line_color=COLOR_MAP[mkt],
            opacity=0.6,
        ))

    radar_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        height=450,
        margin=dict(t=20, b=20),
    )
    st.plotly_chart(radar_fig, use_container_width=True)

    # ── Full comparison table ─────────────────────────────────────────────────
    st.subheader("Full Market Comparison Table")
    comp_data = {}
    for mkt in selected_markets:
        ms_c = MARKET_STATS[mkt]
        str_c = STR_DATA[mkt]
        reg_c = STR_REGULATIONS[mkt]
        costs_c = STR_OPERATING_COSTS[mkt]
        sample_pmt = calc.monthly_mortgage(ms_c["median_price"], down_pct, rate, term)
        sample_str = calc.str_monthly_revenue(str_c["avg_nightly_rate"],
                                               str_c["avg_occupancy"],
                                               costs_c["platform_fee_pct"])
        comp_data[mkt] = {
            "Median Price": f"${ms_c['median_price']:,.0f}",
            "$/sqft": f"${ms_c['price_per_sqft']}",
            "Days on Market": ms_c["dom"],
            "YoY Appreciation": f"{ms_c['yoy_appreciation']*100:.1f}%",
            "Prop Tax Rate": f"{ms_c['property_tax_rate']*100:.2f}%",
            "HOA Common": "Yes" if ms_c["hoa_common"] else "No",
            "─── STR ───": "",
            "Avg Nightly Rate": f"${str_c['avg_nightly_rate']}",
            "Avg Occupancy": f"{str_c['avg_occupancy']*100:.0f}%",
            "Peak Occupancy": f"{str_c['peak_occupancy']*100:.0f}%",
            "Avg Annual Revenue": f"${str_c['avg_annual_revenue']:,.0f}",
            "Active Listings": str_c["active_listings"],
            "Best Property Type": str_c["best_property_type"],
            "─── Mortgage ───": "",
            f"Mtg @ median ({down_pct}% dn, {rate}%)": f"${sample_pmt:,.0f}/mo",
            "Gross STR (avg occ)": f"${sample_str:,.0f}/mo",
            "─── Regulations ───": "",
            "License Required": "Yes" if reg_c["license_required"] else "No",
            "License Fee": f"${reg_c['license_fee']}/yr" if reg_c["license_fee"] else "Contact jurisdiction",
            "Lodging Tax": f"{reg_c['lodging_tax_rate']*100:.1f}%",
            "State Income Tax": "None" if "WY" in mkt else "4.4%",
            "Regulatory Risk": reg_c["regulatory_risk"],
        }

    comp_df = pd.DataFrame(comp_data)
    st.dataframe(comp_df, use_container_width=True, height=600)

    # ── Investment verdict ─────────────────────────────────────────────────────
    st.subheader("Investment Verdict")

    verdicts = {
        "Lander, WY": {
            "rating": "⭐⭐⭐ Value Play / Remodel Opportunity",
            "pros": [
                "Most affordable entry — starter buys possible at $220k–$350k",
                "Median DOM of 86 days = real negotiating leverage",
                "Very low regulatory risk — no dedicated STR ordinance",
                "No state income tax (WY)",
                "NOLS HQ provides year-round international visitor base",
                "Fremont County tourism: $170M/yr and growing",
                "Your remodel skills create meaningful equity here",
                "STR covers mortgage at avg occupancy on mid-price properties",
            ],
            "cons": [
                "Summer-heavy seasonality — slow Nov–Apr",
                "STR revenue declining -7.4% YoY",
                "Lowest ADR ($191) and lowest revenue ceiling of the three",
                "Mild population contraction (not a growth market)",
                "Smaller tourist base than the other markets",
            ],
            "verdict": "Best risk-adjusted entry for a buy-and-remodel strategy. "
                       "At $350k purchase + remodel, a well-positioned property can cover "
                       "its mortgage at market-average occupancy (~47%). The slow market "
                       "means you can negotiate. STR is a secondary income play here — "
                       "primary upside is equity from your remodel skills.",
        },
        "Alpine, WY": {
            "rating": "⭐⭐⭐⭐ High Revenue — High Entry Cost",
            "pros": [
                "Highest ADR ($370/night) of the WY markets",
                "World-class snowmobiling (SnoWest Top 4 in West) = genuine dual season",
                "Jackson Hole proximity without Jackson prices",
                "Salt Lake City feeder market (3.5hr) = different buyer than just WY",
                "Very low regulatory environment (no dedicated STR ordinance)",
                "No state income tax",
                "Top 10% operators earn $103,500+/yr",
            ],
            "cons": [
                "Entry prices $450k–$1.3M — much higher than Lander",
                "STR revenue also declining -7.8% YoY",
                "42.9% overall occupancy (lower than it looks — 35% of listings are MTR)",
                "HOA risk is real — Alpine Meadows, AVR subdivisions restrict STR",
                "True STR market smaller than listing counts suggest",
                "Higher insurance cost than Lander",
            ],
            "verdict": "The dual-season snowmobile + summer play is compelling but entry price "
                       "is high. At $750k, mortgage math is challenging even at peak occupancy. "
                       "Best strategy: find a non-HOA property (36+ exist) at $450–$600k range, "
                       "ideally with reservoir/river access. HOA check is non-negotiable step #1.",
        },
        "Nederland, CO": {
            "rating": "⚠️ Complex — Regulations May Bar Pure Investors",
            "pros": [
                "Highest STR revenue potential (median $44k; top 10% to $190k/yr)",
                "ONLY market with growing STR revenue (+40.5% YoY)",
                "Strongest dual-season: Eldora skiing + Indian Peaks summer",
                "Town purchasing Eldora for $120M — long-term demand catalyst",
                "Denver feeder market (45 min, 715k+ pop) = largest demand pool",
                "You already know this market as a local",
                "Boulder County effective property tax rate lowest of the three (0.53%)",
            ],
            "cons": [
                "⚠️ Owner-occupancy required for residential zones — pure investors barred",
                "⚠️ Wildfire insurance: $5,000–$10,000+/yr; many carriers won't write",
                "Highest entry price ($580k–$1.5M range)",
                "Colorado 4.4% state income tax",
                "Unique Nederland lodging tax ($4/bedroom/night) = additional quarterly filing",
                "50% of listings are 30+ day minimum (thin true STR pool)",
                "Boulder County political environment could tighten rules further",
            ],
            "verdict": "The numbers look great but two structural barriers apply to you: "
                       "(1) If you're not making it your primary residence, you legally can't "
                       "STR a residential property in Nederland — period. "
                       "(2) The wildfire insurance situation must be underwritten before any offer. "
                       "If you find a CBD/GC-zoned property or plan to owner-occupy, it could be "
                       "the strongest pure STR play of the three. Otherwise, focus on Lander or Alpine.",
        },
        "Gilpin County, CO": {
            "rating": "⭐⭐⭐⭐ Hidden Gem — Best Value Near Nederland",
            "pros": [
                "Close to Nederland (~10–20 min) at ~40% less ($574k vs $950k median)",
                "No owner-occupancy STR requirement — investors fully welcome",
                "Much lighter permitting than Boulder County (4/10 vs 7/10)",
                "Lower property taxes than Boulder County (~0.43% vs ~0.53%)",
                "⭐ Unincorporated Gilpin (Rollinsville/Pinecliffe): ONLY 2.9% sales tax — lowest of all markets",
                "Casino gambling in Black Hawk/Central City = year-round demand base",
                "Denver weekend market (45–55 min drive)",
                "STR covers mortgage at avg occupancy on mid-range properties",
                "Your remodel skills create significant value — lots of older cabins",
                "Eldora proximity (same ~15 min as Nederland) for ski demand",
            ],
            "cons": [
                "⛏️ Mine subsidence risk is VERY HIGH — geotechnical review essential",
                "☢️ Zone 1 radon (highest risk in CO) — assume mitigation needed",
                "🔥 Wildfire insurance still expensive ($4k–$8k/yr)",
                "Very thin/small market — limited comps and data",
                "Less established STR market than Nederland",
                "Colorado 4.4% state income tax",
                "Small county staff = slower permitting than WY but faster than Boulder",
            ],
            "verdict": "The most compelling market for your specific situation. "
                       "You get Nederland-adjacent location and Eldora ski demand "
                       "at roughly half the price, with investor-friendly STR rules "
                       "and lighter permitting that your remodel skills can exploit. "
                       "The mine subsidence and radon risks are real but manageable with "
                       "proper due diligence — they scare off casual buyers and create "
                       "your buying opportunity. Do geotechnical + radon review on any "
                       "specific parcel before offering.",
        },
    }

    verdict_cols = st.columns(len([m for m in selected_markets if m in verdicts]))
    for col, mkt in zip(verdict_cols, [m for m in selected_markets if m in verdicts]):
        with col:
            v = verdicts[mkt]
            st.markdown(f"### {mkt}")
            st.markdown(f"**{v['rating']}**")
            st.markdown("**Pros:**")
            for p in v["pros"]:
                st.markdown(f"✅ {p}")
            st.markdown("**Cons:**")
            for c_item in v["cons"]:
                st.markdown(f"⚠️ {c_item}")
            st.info(v["verdict"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — PERMITS & BUILD DIFFICULTY
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.header("Building Permits, Costs & Difficulty")
    st.caption(
        "Critical for remodel/value-add investors. Difficulty rating 1 (easiest) → 10 (hardest). "
        "Fee estimates are approximate — always get current fee schedule from the jurisdiction."
    )

    # ── Summary comparison ─────────────────────────────────────────────────────
    st.subheader("Difficulty & Timeline Comparison")

    diff_cols = st.columns(len(selected_markets))
    for i, mkt in enumerate(selected_markets):
        if mkt not in PERMIT_DATA:
            continue
        pd_m = PERMIT_DATA[mkt]
        score = pd_m["difficulty_rating"]
        color = "green" if score <= 3 else ("orange" if score <= 6 else "red")
        with diff_cols[i]:
            st.markdown(f"### {mkt}")
            st.metric("Difficulty", f"{score}/10 — {pd_m['difficulty_label']}")
            st.metric("Typical Timeline", pd_m["timeline_typical"])
            st.metric("Online Portal", "Yes" if pd_m["online_portal"] else "No")
            st.metric("Engineer Stamp Required", "Yes" if pd_m["engineer_stamp_required"] else "Not typically")

    st.divider()

    # ── Difficulty score bar chart ─────────────────────────────────────────────
    st.subheader("Permitting Difficulty Score")
    mkts_with_permits = [m for m in selected_markets if m in PERMIT_DATA]
    scores = [PERMIT_DATA[m]["difficulty_rating"] for m in mkts_with_permits]
    colors_bar = []
    for s in scores:
        if s <= 3:
            colors_bar.append("#4CAF50")
        elif s <= 6:
            colors_bar.append("#FF9800")
        else:
            colors_bar.append("#F44336")

    fig_diff = go.Figure(go.Bar(
        x=mkts_with_permits,
        y=scores,
        marker_color=colors_bar,
        text=[f"{s}/10 — {PERMIT_DATA[m]['difficulty_label']}" for s, m in zip(scores, mkts_with_permits)],
        textposition="outside",
    ))
    fig_diff.add_hline(y=5, line_dash="dash", line_color="gray",
                       annotation_text="Moderate threshold")
    fig_diff.update_layout(
        yaxis_range=[0, 11], yaxis_title="Difficulty (1=easy, 10=hard)",
        height=320, margin=dict(t=10, b=10),
    )
    st.plotly_chart(fig_diff, use_container_width=True)

    # ── Fee comparison table ───────────────────────────────────────────────────
    st.subheader("Estimated Permit Fee Comparison")
    fee_rows = []
    for mkt in selected_markets:
        if mkt not in PERMIT_DATA:
            continue
        pd_m = PERMIT_DATA[mkt]
        fee_rows.append({
            "Market": mkt,
            "New Home (2,000 sqft)": f"${pd_m['new_home_2000sqft_fee']:,.0f}",
            "Major Remodel ($100k)": f"${pd_m['major_remodel_100k_fee']:,.0f}",
            "Addition ($/sqft)": f"${pd_m['addition_fee_per_sqft']:.2f}",
            "ADU Allowed": "Yes" if pd_m["aduAllowed"] else "No",
            "Variance Difficulty": pd_m["variance_difficulty"],
            "Timeline": pd_m["timeline_typical"],
        })
    st.dataframe(pd.DataFrame(fee_rows).set_index("Market"), use_container_width=True)

    # ── What a $100k remodel costs in permits (+ engineering) ─────────────────
    st.subheader("True Cost of a $100k Remodel Project (Fees + Compliance)")
    remo_rows = []
    for mkt in selected_markets:
        if mkt not in PERMIT_DATA:
            continue
        pd_m = PERMIT_DATA[mkt]
        permit_fee = pd_m["major_remodel_100k_fee"]
        eng_cost = 3_500 if pd_m["engineer_stamp_required"] else 0
        compliance = 3_000 if "Boulder" in mkt or "Nederland" in mkt else 500
        total_overhead = permit_fee + eng_cost + compliance
        remo_rows.append({
            "Market": mkt,
            "Permit Fee (est.)": f"${permit_fee:,.0f}",
            "Engineering Stamp": f"${eng_cost:,.0f}" if eng_cost else "Not required",
            "Compliance/Misc.": f"${compliance:,.0f}",
            "Total Overhead": f"${total_overhead:,.0f}",
            "% of $100k Project": f"{total_overhead/100_000*100:.1f}%",
        })
    st.dataframe(pd.DataFrame(remo_rows).set_index("Market"), use_container_width=True)
    st.caption("Engineering stamp cost is for typical structural work. Compliance includes "
               "code review iterations, inspections, and documentation time.")

    # ── Detailed notes per market ──────────────────────────────────────────────
    st.subheader("Detailed Permitting Notes")
    for mkt in selected_markets:
        if mkt not in PERMIT_DATA:
            continue
        pd_m = PERMIT_DATA[mkt]
        score = pd_m["difficulty_rating"]
        label_color = "green" if score <= 3 else ("orange" if score <= 6 else "red")
        with st.expander(f"**{mkt}** — Difficulty {score}/10 ({pd_m['difficulty_label']})", expanded=True):
            st.markdown("**Key considerations:**")
            for note in pd_m["notes"]:
                st.markdown(f"- {note}")
            st.caption(f"📞 Contact: {pd_m['contact']}")
            st.caption(f"🔗 Fee schedule: {pd_m['fee_schedule_url']}")

    st.info(
        "**Trevor's Remodel Advantage:** Your construction experience is most valuable in markets where "
        "permitting is lightweight (Lander, Alpine) — you can move fast and keep overhead low. "
        "In Boulder County / Nederland, plan for 10–15% of project cost just in permitting overhead. "
        "Gilpin County is a middle ground — lighter than Boulder, but mine/radon due diligence adds cost."
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — ENVIRONMENTAL RISKS
# ══════════════════════════════════════════════════════════════════════════════
with tab7:
    st.header("Environmental Risks")
    st.caption(
        "Environmental due diligence is as important as financial analysis. "
        "These risks affect insurance costs, permitting, safety, and resale value."
    )

    # ── Overall risk scorecard ─────────────────────────────────────────────────
    st.subheader("Overall Environmental Risk Score")
    env_mkts = [m for m in selected_markets if m in ENVIRONMENTAL_RISKS]
    env_scores = [ENVIRONMENTAL_RISKS[m]["overall_risk_score"] for m in env_mkts]
    env_labels = [ENVIRONMENTAL_RISKS[m]["overall_label"] for m in env_mkts]
    env_colors = []
    for s in env_scores:
        if s <= 3:
            env_colors.append("#4CAF50")
        elif s <= 5:
            env_colors.append("#FF9800")
        else:
            env_colors.append("#F44336")

    fig_env = go.Figure(go.Bar(
        x=env_mkts,
        y=env_scores,
        marker_color=env_colors,
        text=[f"{s}/10 — {l}" for s, l in zip(env_scores, env_labels)],
        textposition="outside",
    ))
    fig_env.update_layout(
        yaxis_range=[0, 11],
        yaxis_title="Overall Risk Score (1=low, 10=high)",
        height=320, margin=dict(t=10, b=10),
    )
    st.plotly_chart(fig_env, use_container_width=True)

    # ── Risk heatmap ──────────────────────────────────────────────────────────
    st.subheader("Risk Heatmap by Category")
    risk_categories = ["Wildfire", "Flood", "Radon", "Mine Subsidence",
                       "Hail", "Snow Load", "Avalanche", "Landslide", "Earthquake"]

    heat_data = []
    for cat in risk_categories:
        row = {"Risk": cat}
        for mkt in env_mkts:
            risks = ENVIRONMENTAL_RISKS[mkt]["risks"]
            row[mkt] = risks.get(cat, {}).get("score", 0)
        heat_data.append(row)

    heat_df = pd.DataFrame(heat_data).set_index("Risk")

    # Build a Plotly heatmap instead (avoids Arrow type issues with styled df)
    fig_heat = go.Figure(go.Heatmap(
        z=heat_df.values.tolist(),
        x=list(heat_df.columns),
        y=list(heat_df.index),
        colorscale=[[0, "#C8E6C9"], [0.35, "#FFF9C4"], [0.6, "#FFE0B2"], [1.0, "#FFCDD2"]],
        zmin=0, zmax=10,
        text=heat_df.values.tolist(),
        texttemplate="%{text}",
        showscale=True,
        colorbar=dict(title="Risk Score", tickvals=[1,3,5,7,9],
                      ticktext=["Low","Mod-Low","Moderate","High","Very High"]),
    ))
    fig_heat.update_layout(height=380, margin=dict(t=10, b=10))
    st.plotly_chart(fig_heat, use_container_width=True)
    st.caption("Score: 1–2 = Low (green) | 3–4 = Moderate (yellow) | 5–6 = Elevated (orange) | 7–10 = High/Very High (red)")

    # ── Per-market detailed risk breakdown ───────────────────────────────────
    st.subheader("Detailed Risk Analysis by Market")

    risk_level_colors = {
        "Low": "green", "Low-Moderate": "green",
        "Moderate": "orange", "Moderate-High": "orange",
        "High": "red", "Very High": "red",
    }

    for mkt in env_mkts:
        env = ENVIRONMENTAL_RISKS[mkt]
        overall_color = "green" if env["overall_risk_score"] <= 3 else (
            "orange" if env["overall_risk_score"] <= 5 else "red"
        )
        with st.expander(
            f"**{mkt}** — Overall Risk: :{overall_color}[{env['overall_label']} ({env['overall_risk_score']}/10)]",
            expanded=False
        ):
            for risk_name, risk_info in env["risks"].items():
                level = risk_info["level"]
                score = risk_info["score"]
                rc = risk_level_colors.get(level, "gray")

                col_a, col_b = st.columns([1, 3])
                with col_a:
                    st.markdown(f"**{risk_name}**")
                    st.markdown(f":{rc}[{level}] ({score}/10)")
                with col_b:
                    st.markdown(risk_info["details"])
                    if risk_info.get("insurance_impact"):
                        st.caption(f"💰 Insurance: {risk_info['insurance_impact']}")
                    if risk_info.get("action") and risk_info["action"] not in ("N/A", "Not a concern."):
                        st.caption(f"✅ Action: {risk_info['action']}")
                st.divider()

    # ── Due diligence checklist ───────────────────────────────────────────────
    st.subheader("Pre-Purchase Due Diligence Checklist")
    col_dd1, col_dd2 = st.columns(2)
    with col_dd1:
        st.markdown("**All Markets:**")
        st.markdown("""
- [ ] Pull FEMA Flood Insurance Rate Map (FIRM) for specific parcel
- [ ] Get insurance quote (including STR coverage) **before** making offer
- [ ] Radon test during inspection period
- [ ] Roof inspection — verify snow load compliance for local ground snow load
- [ ] Wildfire insurance availability check (CO markets especially)
- [ ] Confirm STR is permitted at the specific parcel/zone
- [ ] Check for HOA and review CC&Rs (Alpine especially)
        """)
    with col_dd2:
        st.markdown("**Gilpin County Specific:**")
        st.markdown("""
- [ ] Colorado Geological Survey mine hazard map review
- [ ] Geotechnical engineer site visit (mine subsidence)
- [ ] Radon test — assume positive; budget mitigation
- [ ] CGS landslide hazard mapping for parcel
- [ ] Wildfire defensible space assessment
- [ ] Confirm property is in unincorporated Gilpin (not Black Hawk/Central City)
- [ ] Check for any mine shaft/adit on or near parcel
        """)

    st.info(
        "**Resources:** FEMA Flood Map: msc.fema.gov | "
        "Colorado Geological Survey mine hazards: cgsmines.mines.edu | "
        "Colorado Avalanche Information Center: avalanche.state.co.us | "
        "EPA Radon Zone Map: epa.gov/radon/find-information-about-local-radon-zones"
    )


# ─── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Data sources: AirROI, AirDNA, Zillow, Redfin, RocketHomes, Avalara MyLodgeTax, "
    "Colorado Geological Survey, FEMA, county building departments, local government sites. "
    "STR revenue figures are estimates — actual results vary. "
    "Regulations and environmental data accurate as of early 2026 — verify before purchasing. "
    "This tool is for informational purposes only, not financial or legal advice."
)
