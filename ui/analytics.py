"""Budget analytics dashboard.

Turns the budget-allocator output into a visual dashboard: KPI cards
(total / daily / per-person), a Plotly donut of category amounts, a ranked
horizontal bar, and a per-category breakdown with % and ₹. Reads only fields
the workflow already populates on the assessment dict.
"""

from typing import Dict, Any

import streamlit as st
import plotly.graph_objects as go

# Category -> (label, brand colour, icon)
CATEGORIES = [
    ("accommodation_budget_pct", "Accommodation", "#7C3AED", "🏨"),
    ("food_dining_budget_pct", "Food & Dining", "#F97316", "🍽️"),
    ("activities_attractions_budget_pct", "Activities", "#2563EB", "🎢"),
    ("local_transport_budget_pct", "Local Transport", "#0EA5E9", "🚖"),
    ("shopping_misc_budget_pct", "Shopping & Misc", "#EC4899", "🛍️"),
    ("contingency_budget_pct", "Contingency", "#10B981", "🛟"),
]

_PLOTLY_FONT = dict(family="Plus Jakarta Sans, Inter, sans-serif", color="#0F172A")


def _rows(assessment: Dict[str, Any]):
    """Yield (label, pct, amount, color, icon) per category."""
    total = assessment.get("total_budget_inr", 0) or 0
    alloc = assessment.get("budget_allocation", {}) or {}
    amt_keys = ["accommodation", "food_dining", "activities_attractions",
                "local_transport", "shopping_misc", "contingency"]
    for (pct_key, label, color, icon), amt_key in zip(CATEGORIES, amt_keys):
        pct = assessment.get(pct_key, 0) or 0
        amount = alloc.get(amt_key)
        if amount is None:
            amount = total * (pct / 100.0)
        yield label, pct, amount, color, icon


def _kpi(label: str, value: str, icon: str) -> str:
    return f"""
        <div class="glass-card" style="padding:16px 18px;">
            <div style="color:#475569; font-size:.8rem; text-transform:uppercase; letter-spacing:.04em;">
                {icon} {label}
            </div>
            <div style="font-family:'Plus Jakarta Sans'; font-weight:800; font-size:1.5rem; margin-top:6px;">
                {value}
            </div>
        </div>
    """


def render_budget_dashboard(assessment: Dict[str, Any]) -> None:
    rupee = "₹"
    total = assessment.get("total_budget_inr", 0) or 0
    daily = assessment.get("daily_budget", 0) or 0
    group = assessment.get("group_size", 1) or 1
    pp = assessment.get("per_person_budget") or (total / max(group, 1))
    pp_daily = assessment.get("per_person_daily") or (daily / max(group, 1))

    rows = list(_rows(assessment))

    # ---- KPI strip ----
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(_kpi("Total budget", f"{rupee}{total:,.0f}", "💰"), unsafe_allow_html=True)
    k2.markdown(_kpi("Per day", f"{rupee}{daily:,.0f}", "📅"), unsafe_allow_html=True)
    k3.markdown(_kpi("Per person", f"{rupee}{pp:,.0f}", "🧍"), unsafe_allow_html=True)
    k4.markdown(_kpi("Per person / day", f"{rupee}{pp_daily:,.0f}", "🧭"), unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1, 1])

    # ---- Donut ----
    with left:
        labels = [f"{icon} {label}" for (label, _p, _a, _c, icon) in rows]
        values = [a for (_l, _p, a, _c, _i) in rows]
        colors = [c for (_l, _p, _a, c, _i) in rows]
        fig = go.Figure(go.Pie(
            labels=labels, values=values, hole=0.62,
            marker=dict(colors=colors, line=dict(color="rgba(255,255,255,0.85)", width=2)),
            textinfo="percent", textfont=dict(size=12, color="#fff"),
            hovertemplate="%{label}<br>" + rupee + "%{value:,.0f}<extra></extra>",
            sort=False,
        ))
        fig.update_layout(
            title=dict(text="Where your money goes", font=dict(size=16, **_PLOTLY_FONT)),
            showlegend=True, legend=dict(font=dict(size=11, **_PLOTLY_FONT), orientation="v"),
            margin=dict(t=46, b=10, l=10, r=10), height=340,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=_PLOTLY_FONT,
            annotations=[dict(text=f"<b>{rupee}{total:,.0f}</b><br><span style='font-size:11px;color:#64748b'>total</span>",
                              x=0.5, y=0.5, showarrow=False, font=dict(size=18, **_PLOTLY_FONT))],
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ---- Ranked bar ----
    with right:
        srows = sorted(rows, key=lambda r: r[2], reverse=True)
        fig2 = go.Figure(go.Bar(
            x=[a for (_l, _p, a, _c, _i) in srows],
            y=[f"{icon} {label}" for (label, _p, _a, _c, icon) in srows],
            orientation="h",
            marker=dict(color=[c for (_l, _p, _a, c, _i) in srows]),
            text=[f"{rupee}{a:,.0f}" for (_l, _p, a, _c, _i) in srows],
            textposition="auto",
            hovertemplate="%{y}<br>" + rupee + "%{x:,.0f}<extra></extra>",
        ))
        fig2.update_layout(
            title=dict(text="Category amounts", font=dict(size=16, **_PLOTLY_FONT)),
            margin=dict(t=46, b=10, l=10, r=10), height=340,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=_PLOTLY_FONT,
            xaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,0.18)", tickprefix=rupee),
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # ---- Per-category breakdown cards ----
    st.markdown("##### Breakdown")
    cols = st.columns(3)
    for i, (label, pct, amount, color, icon) in enumerate(rows):
        cols[i % 3].markdown(
            f"""
            <div class="glass-card" style="padding:14px 16px; margin-bottom:12px; border-left:4px solid {color};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600;">{icon} {label}</span>
                    <span class="pill" style="margin:0;">{pct:.0f}%</span>
                </div>
                <div style="font-family:'Plus Jakarta Sans'; font-weight:700; font-size:1.18rem; margin-top:6px;">
                    {rupee}{amount:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
