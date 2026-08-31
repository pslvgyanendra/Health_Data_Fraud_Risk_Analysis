from pathlib import Path
import json

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ================================================================
# PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="Health Provider Fraud Risk & Financial Anomaly Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ================================================================
# PROFESSIONAL UI
# ================================================================
st.markdown(
    """
    <style>
    .stApp {
        background: #BDBFC2;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.0rem;
        padding-bottom: 1.5rem;
    }

    .dashboard-shell {
        background: #BDBFC2;
        border-radius: 18px;
        padding: 8px 8px 20px 8px;
    }

    .main-header {
        background: linear-gradient(135deg, #0B1F3A 0%, #123B63 55%, #175B86 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 15px;
        margin-bottom: 12px;
        box-shadow: 0 5px 16px rgba(11,31,58,.15);
    }

    .main-header h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 750;
        line-height: 1.2;
    }

    .main-header p {
        margin: 7px 0 0 0;
        font-size: 13px;
        opacity: .9;
    }

    .info-note {
        background: #EFF6FF;
        border-left: 4px solid #2563EB;
        border-radius: 8px;
        padding: 9px 12px;
        color: #334155;
        font-size: 11px;
        margin-bottom: 12px;
    }

    .section-title {
        font-size: 17px;
        font-weight: 750;
        color: #0B1F3A;
        margin: 13px 0 7px 0;
    }

    .filter-box {
        background: #D5D6D4;
        border: 1px solid #AEB2B7;
        border-radius: 12px;
        padding: 9px 12px 5px 12px;
        margin-bottom: 11px;
        box-shadow: 0 3px 10px rgba(15,23,42,.05);
    }

    .filter-heading {
        color: #040243;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 3px;
    }

    div[data-baseweb="select"] > div {
        background: white;
        border-radius: 8px;
    }

    div[data-testid="stSlider"] {
        padding-top: 0;
    }

    .kpi-card {
        background: #D5D6D4;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 12px 13px;
        min-height: 112px;
        box-shadow: 0 3px 10px rgba(15,23,42,.05);
    }

    .kpi-icon {
        font-size: 17px;
        margin-bottom: 5px;
    }

    .kpi-title {
        font-size: 12px;
        font-weight: 800;
        color: #040243;
        text-transform: uppercase;
        letter-spacing: .3px;
    }

    .kpi-value {
        font-size: 21px;
        font-weight: 750;
        color: #040243;
        margin-top: 3px;
    }

    .kpi-small {
        font-size: 10px;
        color: #040243;
        margin-top: 3px;
    }

    .chart-card {
        background: white;
        border: 1px solid #000000;
        border-radius: 12px;
        padding: 3px 5px 0 5px;
        margin-bottom: 9px;
        box-shadow: 0 3px 10px rgba(15,23,42,.05);
    }

    .provider-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 13px;
        margin-top: 8px;
        box-shadow: 0 3px 10px rgba(15,23,42,.05);
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ================================================================
# CONSTANTS
# ================================================================
RISK_COLORS = {
    "Normal": "#16A34A",
    "Watch": "#F59E0B",
    "High": "#EA580C",
    "Critical": "#DC2626",
}

NAVY = "#0B1F3A"
BLUE = "#2563EB"
TEAL = "#0F766E"

REQUIRED_COLUMNS = [
    "provider_id",
    "agency_name",
    "state",
    "total_episodes_non_lupa",
    "distinct_beneficiaries_non_lupa",
    "average_number_of_total_visits_per_episode_non_lupa",
    "total_hha_charge_amount_non_lupa",
    "total_hha_medicare_payment_amount_non_lupa",
    "total_hha_medicare_standard_payment_amount_non_lupa",
    "outlier_payments_as_a_percent_of_medicare_payment_amount_non_lupa",
    "total_lupa_episodes",
    "average_age",
    "average_hcc_score",
]

NUMERIC_COLUMNS = [
    "total_episodes_non_lupa",
    "distinct_beneficiaries_non_lupa",
    "average_number_of_total_visits_per_episode_non_lupa",
    "total_hha_charge_amount_non_lupa",
    "total_hha_medicare_payment_amount_non_lupa",
    "total_hha_medicare_standard_payment_amount_non_lupa",
    "outlier_payments_as_a_percent_of_medicare_payment_amount_non_lupa",
    "total_lupa_episodes",
    "average_age",
    "average_hcc_score",
]


# ================================================================
# HELPERS
# ================================================================
def safe_divide(a, b):
    a = pd.to_numeric(a, errors="coerce")
    b = pd.to_numeric(b, errors="coerce")
    return np.where(b.notna() & (b != 0), a / b, np.nan)


def money(value):
    if pd.isna(value):
        return "N/A"
    value = float(value)
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.0f}"


def number(value):
    if pd.isna(value):
        return "N/A"
    return f"{float(value):,.0f}"


def assign_risk(score):
    if pd.isna(score):
        return "Unknown"
    if score >= 75:
        return "Critical"
    if score >= 50:
        return "High"
    if score >= 25:
        return "Watch"
    return "Normal"


def compact_layout(fig, title, x_title=None, y_title=None, height=315):
    fig.update_layout(
        title=dict(
            text=title,
            x=0.02,
            xanchor="left",
            font=dict(size=15, color=NAVY),
        ),
        height=height,
        margin=dict(l=55, r=20, t=52, b=50),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Arial", color="#111827", size=11),
        hoverlabel=dict(bgcolor="white", font_size=11, font_family="Arial"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="right",
            x=1,
            font=dict(size=10),
        ),
    )
    fig.update_xaxes(
        title_text=x_title,
        title_font=dict(size=11, color="#111827"),
        tickfont=dict(size=10, color="#111827"),
        showgrid=True,
        gridcolor="#E8EDF3",
        zeroline=False,
    )
    fig.update_yaxes(
        title_text=y_title,
        title_font=dict(size=11, color="#111827"),
        tickfont=dict(size=10, color="#111827"),
        showgrid=True,
        gridcolor="#E8EDF3",
        zeroline=False,
    )
    return fig


# ================================================================
# DATA LOAD + PREPARATION
# ================================================================
@st.cache_data(show_spinner="Loading 100K health-provider records...")
def load_and_prepare_data(data_path):
    path = Path(data_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    data = pd.DataFrame(raw)

    missing = [c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing:
        raise ValueError(
            "Required columns missing hain:\n" + "\n".join(missing)
        )

    # Match notebook's numeric conversion for dashboard-required columns.
    for col in NUMERIC_COLUMNS:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    # Match notebook derived metrics.
    data["dashboard_total_episodes"] = (
        data["total_episodes_non_lupa"].fillna(0)
        + data["total_lupa_episodes"].fillna(0)
    )

    data["dashboard_lupa_rate"] = (
        safe_divide(
            data["total_lupa_episodes"],
            data["dashboard_total_episodes"],
        ) * 100
    )

    data["dashboard_payment_per_episode"] = safe_divide(
        data["total_hha_medicare_payment_amount_non_lupa"],
        data["total_episodes_non_lupa"],
    )

    data["dashboard_charge_payment_ratio"] = safe_divide(
        data["total_hha_charge_amount_non_lupa"],
        data["total_hha_medicare_payment_amount_non_lupa"],
    )

    data["dashboard_beneficiaries_per_episode"] = safe_divide(
        data["distinct_beneficiaries_non_lupa"],
        data["total_episodes_non_lupa"],
    )

    data["dashboard_payment_vs_standard"] = safe_divide(
        data["total_hha_medicare_payment_amount_non_lupa"],
        data["total_hha_medicare_standard_payment_amount_non_lupa"],
    )

    data["dashboard_payment_per_beneficiary"] = safe_divide(
        data["total_hha_medicare_payment_amount_non_lupa"],
        data["distinct_beneficiaries_non_lupa"],
    )

    # Notebook age buckets.
    data["dashboard_age_segment"] = pd.cut(
        data["average_age"],
        bins=[-np.inf, 70, 80, np.inf],
        labels=["Below 70", "70–80", "Above 80"],
        right=False,
    )

    # Notebook visit buckets.
    visit_column = "average_number_of_total_visits_per_episode_non_lupa"
    data["dashboard_visit_intensity"] = pd.cut(
        data[visit_column],
        bins=[-np.inf, 12, 20, np.inf],
        labels=["Low", "Medium", "High"],
        right=False,
    )

    # Notebook 90th-percentile anomaly thresholds.
    payment_threshold = data["dashboard_payment_per_episode"].quantile(.90)
    visit_threshold = data[visit_column].quantile(.90)
    lupa_threshold = data["dashboard_lupa_rate"].quantile(.90)

    outlier_column = (
        "outlier_payments_as_a_percent_of_medicare_payment_amount_non_lupa"
    )
    outlier_threshold = data[outlier_column].quantile(.90)

    charge_payment_threshold = data["dashboard_charge_payment_ratio"].quantile(.90)
    payment_standard_threshold = data["dashboard_payment_vs_standard"].quantile(.90)

    data["signal_payment_episode"] = (
        data["dashboard_payment_per_episode"] >= payment_threshold
    ).fillna(False)

    data["signal_visit_intensity"] = (
        data[visit_column] >= visit_threshold
    ).fillna(False)

    data["signal_lupa_rate"] = (
        data["dashboard_lupa_rate"] >= lupa_threshold
    ).fillna(False)

    data["signal_outlier_payment"] = (
        data[outlier_column] >= outlier_threshold
    ).fillna(False)

    data["signal_charge_payment"] = (
        data["dashboard_charge_payment_ratio"] >= charge_payment_threshold
    ).fillna(False)

    data["signal_payment_standard"] = (
        data["dashboard_payment_vs_standard"] >= payment_standard_threshold
    ).fillna(False)

    signal_columns = [
        "signal_payment_episode",
        "signal_visit_intensity",
        "signal_lupa_rate",
        "signal_outlier_payment",
        "signal_charge_payment",
        "signal_payment_standard",
    ]

    data["dashboard_signal_count"] = data[signal_columns].sum(axis=1)

    data["dashboard_suspicion_score"] = (
        data["dashboard_signal_count"] / len(signal_columns)
    ) * 100

    data["dashboard_risk_level"] = (
        data["dashboard_suspicion_score"].apply(assign_risk)
    )

    return data


# ================================================================
# FIND DATASET
# ================================================================
DATA_PATH = Path(__file__).resolve().parent / "data" / "health_data_100k.json"

try:
    data = load_and_prepare_data(str(DATA_PATH))
except Exception as exc:
    st.error("❌ Dashboard data load nahi ho paaya.")
    st.code(str(exc))
    st.stop()


# ================================================================
# HEADER
# ================================================================
st.markdown(
    """
    <div class="main-header">
        <h1>🏥 Health Provider Fraud Risk & Financial Anomaly Dashboard</h1>
        <p>
            Executive monitoring of Medicare payment, provider utilization,
            LUPA intensity and unusual financial patterns
        </p>
    </div>

    <div class="info-note">
        <b>Purpose:</b> Prioritize providers showing unusual financial and
        utilization patterns for further investigation.
        &nbsp;&nbsp;
        <b>Note:</b> Risk score is an analytical screening signal, not proof of fraud.
    </div>
    """,
    unsafe_allow_html=True,
)


# ================================================================
# HORIZONTAL FILTERS — ABOVE KPIs, NOT SIDEBAR
# ================================================================
st.markdown('<div class="filter-box">', unsafe_allow_html=True)
st.markdown('<div class="filter-heading">🎛️ Interactive Filters</div>', unsafe_allow_html=True)

states = sorted(data["state"].dropna().astype(str).unique().tolist())
providers = sorted(data["agency_name"].dropna().astype(str).unique().tolist())

f1, f2, f3, f4, f5, f6, f7 = st.columns(
    [1.0, 1.65, 1.0, 1.0, 1.0, 1.25, .65],
    gap="small",
)

with f1:
    selected_state = st.selectbox(
        "State",
        ["All States"] + states,
        key="state_filter",
    )

with f2:
    selected_provider = st.selectbox(
        "Provider",
        ["All Providers"] + providers,
        key="provider_filter",
    )

with f3:
    selected_risk = st.selectbox(
        "Risk",
        ["All Risk Levels", "Normal", "Watch", "High", "Critical"],
        key="risk_filter",
    )

with f4:
    selected_age = st.selectbox(
        "Age",
        ["All Age Segments", "Below 70", "70–80", "Above 80"],
        key="age_filter",
    )

with f5:
    selected_visits = st.selectbox(
        "Visits",
        ["All Visit Levels", "Low", "Medium", "High"],
        key="visit_filter",
    )

with f6:
    selected_score = st.slider(
        "Risk Score",
        min_value=0,
        max_value=100,
        value=(0, 100),
        step=5,
        key="score_filter",
    )

with f7:
    st.write("")
    st.write("")
    if st.button("↻", help="Reset all filters", use_container_width=True):
        for key in [
            "state_filter",
            "provider_filter",
            "risk_filter",
            "age_filter",
            "visit_filter",
            "score_filter",
        ]:
            st.session_state.pop(key, None)
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)


# ================================================================
# FILTER DATA
# ================================================================
filtered = data.copy()

if selected_state != "All States":
    filtered = filtered[filtered["state"].astype(str) == selected_state]

if selected_provider != "All Providers":
    filtered = filtered[
        filtered["agency_name"].astype(str) == selected_provider
    ]

if selected_risk != "All Risk Levels":
    filtered = filtered[
        filtered["dashboard_risk_level"] == selected_risk
    ]

if selected_age != "All Age Segments":
    filtered = filtered[
        filtered["dashboard_age_segment"].astype(str) == selected_age
    ]

if selected_visits != "All Visit Levels":
    filtered = filtered[
        filtered["dashboard_visit_intensity"].astype(str) == selected_visits
    ]

filtered = filtered[
    filtered["dashboard_suspicion_score"].between(
        selected_score[0], selected_score[1]
    )
]

if filtered.empty:
    st.warning("⚠️ No providers match the selected filters.")
    st.stop()


# ================================================================
# KPI CARDS
# ================================================================
st.markdown('<div class="section-title">📊 Executive KPIs</div>', unsafe_allow_html=True)

providers_count = filtered["provider_id"].nunique()
episodes = filtered["dashboard_total_episodes"].sum()
payment = filtered[
    "total_hha_medicare_payment_amount_non_lupa"
].sum()
payment_episode = filtered["dashboard_payment_per_episode"].mean()
lupa_rate = filtered["dashboard_lupa_rate"].mean()

high_critical = filtered[
    filtered["dashboard_risk_level"].isin(["High", "Critical"])
]["provider_id"].nunique()

risk_score = filtered["dashboard_suspicion_score"].mean()

kpi_values = [
    ("👥", "Providers Screened", number(providers_count), "Unique provider agencies"),
    ("🏥", "Total Episodes", number(episodes), "LUPA + Non-LUPA"),
    ("💰", "Medicare Payment", money(payment), "Non-LUPA payment"),
    ("💵", "Payment / Episode", money(payment_episode), "Average"),
    ("📉", "Average LUPA Rate", f"{lupa_rate:.1f}%", "LUPA intensity"),
    ("🚨", "High / Critical", number(high_critical), "Providers for review"),
    ("🎯", "Avg Risk Score", f"{risk_score:.1f}", "Out of 100"),
]

kcols = st.columns(7, gap="small")

for col, (icon, title, value, small) in zip(kcols, kpi_values):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-small">{small}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ================================================================
# SECTION 1 — RISK OVERVIEW
# ================================================================
st.markdown(
    '<div class="section-title">🚨 Executive Risk Overview</div>',
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2, gap="small")

with c1:
    risk_summary = (
        filtered["dashboard_risk_level"]
        .value_counts()
        .reindex(["Normal", "Watch", "High", "Critical"], fill_value=0)
        .reset_index()
    )
    risk_summary.columns = ["Risk Level", "Provider Count"]

    fig1 = px.pie(
        risk_summary,
        names="Risk Level",
        values="Provider Count",
        hole=.58,
        color="Risk Level",
        color_discrete_map=RISK_COLORS,
    )

    fig1.update_traces(
        textposition="outside",
        textinfo="label+percent",
        textfont=dict(color="#111827"),
        hovertemplate=(
            "<b>Risk Level:</b> %{label}<br>"
            "<b>Providers:</b> %{value:,}<br>"
            "<b>Share:</b> %{percent}<extra></extra>"
        ),
    )

    fig1.update_layout(
        title=dict(
            text="Provider Risk Distribution",
            x=.02,
            xanchor="left",
            font=dict(size=15, color=NAVY),
        ),
        height=315,
        margin=dict(l=15, r=15, t=50, b=15),
        paper_bgcolor="white",
        showlegend=True,
        legend=dict(
            font=dict(color="#111827", size=10),
        ),
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True, config={"displaylogo": False})
    st.markdown("</div>", unsafe_allow_html=True)


with c2:
    top = (
        filtered.sort_values(
            "dashboard_suspicion_score",
            ascending=False,
        )
        .head(8)
        .copy()
    )

    top["Provider"] = (
        top["agency_name"]
        .fillna(top["provider_id"].astype(str))
        .astype(str)
        .str[:28]
    )

    fig2 = go.Figure()

    for risk_level in ["Normal", "Watch", "High", "Critical"]:
        part = top[top["dashboard_risk_level"] == risk_level]

        if part.empty:
            continue

        customdata = np.column_stack(
            [
                part["agency_name"].astype(str),
                part["state"].astype(str),
                part["dashboard_suspicion_score"],
                part["dashboard_signal_count"],
                part["dashboard_payment_per_episode"],
                part["dashboard_lupa_rate"],
            ]
        )

        fig2.add_trace(
            go.Bar(
                x=part["dashboard_suspicion_score"],
                y=part["Provider"],
                orientation="h",
                name=risk_level,
                marker_color=RISK_COLORS[risk_level],
                customdata=customdata,
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "State: %{customdata[1]}<br>"
                    "Risk Score: %{customdata[2]:.1f}/100<br>"
                    "Signals: %{customdata[3]:.0f}<br>"
                    "Payment / Episode: $%{customdata[4]:,.0f}<br>"
                    "LUPA Rate: %{customdata[5]:.1f}%"
                    "<extra></extra>"
                ),
            )
        )

    fig2.update_layout(barmode="group")
    fig2 = compact_layout(
        fig2,
        "Top Providers by Fraud Risk Screening Score",
        "Risk Screening Score (0–100)",
        "Provider",
    )
    fig2.update_xaxes(range=[0, 100])

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True, config={"displaylogo": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ================================================================
# SECTION 2 — FINANCIAL & UTILIZATION
# ================================================================
st.markdown(
    '<div class="section-title">💰 Financial & Utilization Intelligence</div>',
    unsafe_allow_html=True,
)

c3, c4 = st.columns(2, gap="small")

with c3:
    state_summary = (
        filtered.groupby("state", dropna=False)
        .agg(
            Providers=("provider_id", "nunique"),
            Total_Episodes=("dashboard_total_episodes", "sum"),
            Medicare_Payment=(
                "total_hha_medicare_payment_amount_non_lupa",
                "sum",
            ),
            Avg_Risk=("dashboard_suspicion_score", "mean"),
        )
        .reset_index()
        .sort_values("Medicare_Payment", ascending=False)
        .head(10)
        .sort_values("Medicare_Payment")
    )

    customdata = np.column_stack(
        [
            state_summary["Providers"],
            state_summary["Total_Episodes"],
            state_summary["Avg_Risk"],
        ]
    )

    fig3 = go.Figure(
        go.Bar(
            x=state_summary["Medicare_Payment"],
            y=state_summary["state"],
            orientation="h",
            marker_color=TEAL,
            customdata=customdata,
            hovertemplate=(
                "<b>State: %{y}</b><br>"
                "Medicare Payment: $%{x:,.0f}<br>"
                "Providers: %{customdata[0]:,.0f}<br>"
                "Episodes: %{customdata[1]:,.0f}<br>"
                "Avg Risk Score: %{customdata[2]:.1f}"
                "<extra></extra>"
            ),
        )
    )

    fig3 = compact_layout(
        fig3,
        "Top 10 States by Medicare Payment",
        "Total Medicare Payment ($)",
        "State",
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True, config={"displaylogo": False})
    st.markdown("</div>", unsafe_allow_html=True)


with c4:
    visit_column = "average_number_of_total_visits_per_episode_non_lupa"

    scatter_data = filtered.dropna(
        subset=[visit_column, "dashboard_payment_per_episode"]
    )

    fig4 = px.scatter(
        scatter_data,
        x=visit_column,
        y="dashboard_payment_per_episode",
        color="dashboard_risk_level",
        color_discrete_map=RISK_COLORS,
        size="dashboard_total_episodes",
        hover_name="agency_name",
        labels={
            visit_column: "Average Visits per Episode",
            "dashboard_payment_per_episode": "Medicare Payment per Episode ($)",
            "dashboard_risk_level": "Risk Level",
        },
    )

    fig4.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Average Visits / Episode: %{x:.2f}<br>"
            "Payment / Episode: $%{y:,.0f}<extra></extra>"
        )
    )

    fig4 = compact_layout(
        fig4,
        "Payment Intensity vs Service Utilization",
        "Average Visits per Episode",
        "Medicare Payment per Episode ($)",
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True, config={"displaylogo": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ================================================================
# SECTION 3 — PAYMENT PATTERN & OPERATIONAL ANOMALY
# ================================================================
st.markdown(
    '<div class="section-title">⚠️ Payment Pattern & Operational Anomaly Signals</div>',
    unsafe_allow_html=True,
)

c5, c6 = st.columns(2, gap="small")

with c5:
    scatter_lupa = filtered.dropna(
        subset=["dashboard_lupa_rate", "dashboard_payment_per_episode"]
    )

    fig5 = px.scatter(
        scatter_lupa,
        x="dashboard_lupa_rate",
        y="dashboard_payment_per_episode",
        color="dashboard_risk_level",
        color_discrete_map=RISK_COLORS,
        size="dashboard_total_episodes",
        hover_name="agency_name",
        labels={
            "dashboard_lupa_rate": "LUPA Rate (%)",
            "dashboard_payment_per_episode": "Medicare Payment per Episode ($)",
            "dashboard_risk_level": "Risk Level",
        },
    )

    fig5.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "LUPA Rate: %{x:.1f}%<br>"
            "Payment / Episode: $%{y:,.0f}<extra></extra>"
        )
    )

    fig5 = compact_layout(
        fig5,
        "LUPA Rate vs Medicare Payment",
        "LUPA Rate (%)",
        "Medicare Payment per Episode ($)",
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=True, config={"displaylogo": False})
    st.markdown("</div>", unsafe_allow_html=True)


with c6:
    outlier_column = (
        "outlier_payments_as_a_percent_of_medicare_payment_amount_non_lupa"
    )

    outlier_data = (
        filtered.nlargest(8, outlier_column)
        .copy()
    )

    outlier_data["Provider"] = (
        outlier_data["agency_name"]
        .fillna(outlier_data["provider_id"].astype(str))
        .astype(str)
        .str[:28]
    )

    customdata = np.column_stack(
        [
            outlier_data["state"].astype(str),
            outlier_data[outlier_column],
            outlier_data["dashboard_payment_per_episode"],
            outlier_data["dashboard_suspicion_score"],
        ]
    )

    fig6 = go.Figure(
        go.Bar(
            x=outlier_data[outlier_column],
            y=outlier_data["Provider"],
            orientation="h",
            marker_color="#DC2626",
            customdata=customdata,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "State: %{customdata[0]}<br>"
                "Outlier Payment: %{x:.1f}%<br>"
                "Payment / Episode: $%{customdata[2]:,.0f}<br>"
                "Risk Score: %{customdata[3]:.1f}/100"
                "<extra></extra>"
            ),
        )
    )

    fig6 = compact_layout(
        fig6,
        "Providers with Highest Outlier Payment Percentage",
        "Outlier Payment (% of Medicare Payment)",
        "Provider",
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig6, use_container_width=True, config={"displaylogo": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ================================================================
# SECTION 4 — CLINICAL COMPLEXITY & PAYMENT BENCHMARK
# ================================================================
st.markdown(
    '<div class="section-title">🧬 Clinical Complexity & Payment Benchmark</div>',
    unsafe_allow_html=True,
)

c7, c8 = st.columns(2, gap="small")

with c7:
    hcc_data = filtered.dropna(
        subset=["average_hcc_score", "dashboard_payment_per_episode"]
    )

    fig7 = px.scatter(
        hcc_data,
        x="average_hcc_score",
        y="dashboard_payment_per_episode",
        color="dashboard_risk_level",
        color_discrete_map=RISK_COLORS,
        size="dashboard_total_episodes",
        hover_name="agency_name",
        labels={
            "average_hcc_score": "Average HCC Score",
            "dashboard_payment_per_episode": "Medicare Payment per Episode ($)",
            "dashboard_risk_level": "Risk Level",
        },
    )

    fig7.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Average HCC Score: %{x:.2f}<br>"
            "Payment / Episode: $%{y:,.0f}<extra></extra>"
        )
    )

    fig7 = compact_layout(
        fig7,
        "Beneficiary Complexity vs Payment per Episode",
        "Average HCC Score",
        "Medicare Payment per Episode ($)",
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig7, use_container_width=True, config={"displaylogo": False})
    st.markdown("</div>", unsafe_allow_html=True)


with c8:
    benchmark_data = filtered.dropna(
        subset=[
            "dashboard_payment_vs_standard",
            "dashboard_payment_per_episode",
        ]
    )

    fig8 = px.scatter(
        benchmark_data,
        x="dashboard_payment_vs_standard",
        y="dashboard_payment_per_episode",
        color="dashboard_risk_level",
        color_discrete_map=RISK_COLORS,
        size="dashboard_total_episodes",
        hover_name="agency_name",
        labels={
            "dashboard_payment_vs_standard": "Actual Payment / Standard Payment",
            "dashboard_payment_per_episode": "Medicare Payment per Episode ($)",
            "dashboard_risk_level": "Risk Level",
        },
    )

    fig8.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Actual / Standard Payment: %{x:.2f}<br>"
            "Payment / Episode: $%{y:,.0f}<extra></extra>"
        )
    )

    fig8.add_vline(
        x=1,
        line_dash="dash",
        line_width=1,
        line_color="#64748B",
    )

    fig8 = compact_layout(
        fig8,
        "Actual Payment vs Standard Medicare Payment",
        "Actual Payment / Standard Payment",
        "Medicare Payment per Episode ($)",
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig8, use_container_width=True, config={"displaylogo": False})
    st.markdown("</div>", unsafe_allow_html=True)


# ================================================================
# PROVIDER INVESTIGATION QUEUE
# ================================================================
st.markdown(
    '<div class="section-title">🔎 Provider Investigation Queue</div>',
    unsafe_allow_html=True,
)

investigation = (
    filtered.sort_values(
        "dashboard_suspicion_score",
        ascending=False,
    )
    .head(15)
    .copy()
)

investigation["Provider"] = (
    investigation["agency_name"]
    .fillna(investigation["provider_id"].astype(str))
    .astype(str)
)

table = pd.DataFrame(
    {
        "Provider": investigation["Provider"],
        "State": investigation["state"],
        "Risk Level": investigation["dashboard_risk_level"],
        "Risk Score": investigation["dashboard_suspicion_score"].round(1),
        "Signals": investigation["dashboard_signal_count"].astype(int),
        "Medicare Payment": investigation[
            "total_hha_medicare_payment_amount_non_lupa"
        ].round(0),
        "Payment / Episode": investigation[
            "dashboard_payment_per_episode"
        ].round(0),
        "LUPA Rate %": investigation[
            "dashboard_lupa_rate"
        ].round(1),
        "Visits / Episode": investigation[
            visit_column
        ].round(2),
    }
)

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True,
    height=520,
    column_config={
        "Risk Score": st.column_config.ProgressColumn(
            "Risk Score",
            min_value=0,
            max_value=100,
            format="%.1f",
        ),
        "Medicare Payment": st.column_config.NumberColumn(
            "Medicare Payment",
            format="$%d",
        ),
        "Payment / Episode": st.column_config.NumberColumn(
            "Payment / Episode",
            format="$%d",
        ),
        "LUPA Rate %": st.column_config.NumberColumn(
            "LUPA Rate %",
            format="%.1f%%",
        ),
        "Visits / Episode": st.column_config.NumberColumn(
            "Visits / Episode",
            format="%.2f",
        ),
    },
)


# ================================================================
# SELECTED PROVIDER PROFILE
# ================================================================
if selected_provider != "All Providers":
    selected_rows = filtered[
        filtered["agency_name"].astype(str) == selected_provider
    ]

    if not selected_rows.empty:
        row = selected_rows.iloc[0]

        st.markdown(
            '<div class="section-title">🏥 Selected Provider Profile</div>',
            unsafe_allow_html=True,
        )

        p1, p2, p3, p4 = st.columns(4)

        with p1:
            st.metric("Risk Level", row["dashboard_risk_level"])

        with p2:
            st.metric(
                "Risk Score",
                f"{row['dashboard_suspicion_score']:.1f}/100",
            )

        with p3:
            st.metric(
                "Signals",
                f"{int(row['dashboard_signal_count'])}/6",
            )

        with p4:
            st.metric("State", str(row["state"]))

        st.markdown(
            f"""
            <div class="provider-card">
                <b style="font-size:16px;color:#0B1F3A;">
                    {selected_provider}
                </b>
                <br><br>
                <b>Medicare Payment:</b>
                {money(row["total_hha_medicare_payment_amount_non_lupa"])}
                &nbsp;&nbsp; | &nbsp;&nbsp;
                <b>Payment / Episode:</b>
                {money(row["dashboard_payment_per_episode"])}
                &nbsp;&nbsp; | &nbsp;&nbsp;
                <b>LUPA:</b>
                {row["dashboard_lupa_rate"]:.1f}%
                &nbsp;&nbsp; | &nbsp;&nbsp;
                <b>HCC:</b>
                {row["average_hcc_score"]:.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )
