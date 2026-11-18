"""
app.py - SupeRR Selector: Rajasthan Royals IPL 2027 Auction War Room
World-Class Interactive Sports Analytics Platform
Two Rigorous Analytical Layers:
Layer 1: Overall Pressure Rankings (Official Unstop Evaluation)
Layer 2: Rajasthan Royals Recruitment Intelligence (Contextual Auction Strategy)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Streamlit Page Setup
st.set_page_config(
    page_title="RR SupeRR Selector | IPL 2027 Auction War Room",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Rajasthan Royals CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 15% 10%, #151a2e 0%, #080c18 55%, #040711 100%);
        color: #f1f5f9;
    }
    
    /* Top Hero Header */
    .rr-hero-banner {
        background: linear-gradient(135deg, rgba(20, 29, 53, 0.95) 0%, rgba(35, 17, 56, 0.95) 50%, rgba(55, 12, 46, 0.95) 100%);
        border: 1px solid rgba(234, 26, 127, 0.35);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.12);
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        overflow: hidden;
    }
    
    .rr-hero-banner::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(234, 26, 127, 0.25) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .rr-logo-title {
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #ea1a7f 0%, #ff6db3 45%, #ffd700 80%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.15;
    }
    
    .rr-badge {
        display: inline-block;
        background: rgba(234, 26, 127, 0.15);
        color: #ff6db3;
        border: 1px solid rgba(234, 26, 127, 0.5);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
    }
    
    /* 6-Column KPI Grid */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 12px;
        margin-bottom: 24px;
    }
    
    @media (max-width: 1100px) {
        .kpi-container {
            grid-template-columns: repeat(3, 1fr);
        }
    }
    
    .kpi-card {
        background: linear-gradient(180deg, rgba(26, 36, 62, 0.7) 0%, rgba(13, 20, 38, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px 16px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
        transition: all 0.25s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: rgba(234, 26, 127, 0.6);
        box-shadow: 0 8px 24px rgba(234, 26, 127, 0.25);
    }
    
    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: linear-gradient(180deg, #ea1a7f 0%, #17387e 100%);
    }
    
    .kpi-title {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94a3b8;
        margin-bottom: 4px;
    }
    
    .kpi-value {
        font-size: 1.55rem;
        font-weight: 900;
        color: #f8fafc;
        margin: 0;
        letter-spacing: -0.5px;
        font-family: 'Outfit', sans-serif;
    }
    
    .kpi-sub {
        font-size: 0.7rem;
        color: #38bdf8;
        margin-top: 3px;
        font-weight: 500;
    }
    
    /* Callout & Architecture Banner */
    .arch-banner {
        background: rgba(15, 23, 42, 0.7);
        border-left: 4px solid #ea1a7f;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 20px;
        font-size: 0.88rem;
        line-height: 1.45;
    }
    
    /* Recruitment Card */
    .recruitment-card {
        background: linear-gradient(180deg, rgba(20, 29, 54, 0.85) 0%, rgba(10, 16, 34, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        transition: all 0.2s ease;
    }
    
    .recruitment-card:hover {
        border-color: rgba(234, 26, 127, 0.5);
    }
    
    .badge-rank-1 {
        background: linear-gradient(135deg, #ffd700 0%, #b8860b 100%);
        color: #000;
        padding: 3px 10px;
        border-radius: 12px;
        font-weight: 800;
        font-size: 0.75rem;
    }
    
    .badge-rank-2 {
        background: linear-gradient(135deg, #e2e8f0 0%, #94a3b8 100%);
        color: #000;
        padding: 3px 10px;
        border-radius: 12px;
        font-weight: 800;
        font-size: 0.75rem;
    }
    
    .badge-rank-3 {
        background: linear-gradient(135deg, #cd7f32 0%, #8b4513 100%);
        color: #fff;
        padding: 3px 10px;
        border-radius: 12px;
        font-weight: 800;
        font-size: 0.75rem;
    }
    
    .badge-rank-other {
        background: rgba(255, 255, 255, 0.1);
        color: #cbd5e1;
        padding: 3px 9px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.75rem;
    }
    
    .badge-stat {
        background: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.3);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .badge-rec {
        background: rgba(234, 26, 127, 0.15);
        color: #ff6db3;
        border: 1px solid rgba(234, 26, 127, 0.35);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-cat-rr {
        background: rgba(234, 26, 127, 0.2);
        color: #ff6db3;
        border: 1px solid #ea1a7f;
        padding: 2px 7px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
    }
    
    .badge-cat-ipl {
        background: rgba(14, 165, 233, 0.2);
        color: #38bdf8;
        border: 1px solid #0ea5e9;
        padding: 2px 7px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
    }
    
    .badge-cat-intl {
        background: rgba(255, 215, 0, 0.15);
        color: #ffd700;
        border: 1px solid #ffd700;
        padding: 2px 7px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Data Caching
@st.cache_data
def load_all_war_room_data():
    base = Path(__file__).resolve().parent.parent
    top_bat = pd.read_csv(base / "data/outputs/top_10_batters_under_pressure.csv")
    top_bowl = pd.read_csv(base / "data/outputs/top_10_bowlers_under_pressure.csv")
    all_bat = pd.read_csv(base / "data/outputs/all_eligible_batters.csv")
    all_bowl = pd.read_csv(base / "data/outputs/all_eligible_bowlers.csv")
    bat_split = pd.read_parquet(base / "data/outputs/batter_pace_spin_pressure.parquet")
    bowl_style = pd.read_parquet(base / "data/outputs/bowler_delivery_style_pressure.parquet")
    speed_summary = pd.read_csv(base / "data/outputs/pace_speed_bins_pressure.csv")
    
    # Layer 2 Recruitment datasets
    rec_bat = pd.read_parquet(base / "data/outputs/rr_recruitment_batters.parquet")
    rec_bowl = pd.read_parquet(base / "data/outputs/rr_recruitment_bowlers.parquet")
    
    # Load format splits
    bat_fmt_path = base / "data/outputs/top_batters_format_split.parquet"
    bowl_fmt_path = base / "data/outputs/top_bowlers_format_split.parquet"
    bat_fmt = pd.read_parquet(bat_fmt_path) if bat_fmt_path.exists() else None
    bowl_fmt = pd.read_parquet(bowl_fmt_path) if bowl_fmt_path.exists() else None
    
    return top_bat, top_bowl, all_bat, all_bowl, bat_split, bowl_style, speed_summary, bat_fmt, bowl_fmt, rec_bat, rec_bowl

top_bat, top_bowl, all_bat, all_bowl, bat_split, bowl_style, speed_summary, bat_fmt, bowl_fmt, rec_bat, rec_bowl = load_all_war_room_data()

# Ensure correct sorting strictly by reliability score
top_bat = top_bat.sort_values(by='reliability_score', ascending=False).reset_index(drop=True)
top_bat['Rank'] = range(1, len(top_bat) + 1)

top_bowl = top_bowl.sort_values(by='reliability_score', ascending=False).reset_index(drop=True)
top_bowl['Rank'] = range(1, len(top_bowl) + 1)

# Helper function for rank badge formatting
def format_rank_badge(rank):
    if rank == 1:
        return "🥇 Rank 1"
    elif rank == 2:
        return "🥈 Rank 2"
    elif rank == 3:
        return "🥉 Rank 3"
    else:
        return f"#{rank}"

# Sidebar with Official RR SVG Crest
svg_crest = """
<div style="text-align: center; padding: 12px 0 16px 0;">
    <svg width="90" height="90" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="50" r="46" fill="#141d38" stroke="#ea1a7f" stroke-width="3"/>
        <path d="M50 16 L56 32 L72 32 L59 42 L64 58 L50 48 L36 58 L41 42 L28 32 L44 32 Z" fill="#ffd700"/>
        <text x="50" y="74" font-family="'Outfit', sans-serif" font-weight="900" font-size="20" fill="#ffffff" text-anchor="middle">RR</text>
        <circle cx="50" cy="50" r="44" stroke="#ffd700" stroke-width="1" stroke-dasharray="2 3"/>
    </svg>
    <div style="font-weight: 800; font-size: 0.95rem; color: #f8fafc; letter-spacing: 1px; margin-top: 6px;">RAJASTHAN ROYALS</div>
    <div style="font-weight: 600; font-size: 0.68rem; color: #ea1a7f; letter-spacing: 1.5px;">ANALYTICS WAR ROOM</div>
</div>
"""
st.sidebar.markdown(svg_crest, unsafe_allow_html=True)
st.sidebar.markdown("---")

nav = st.sidebar.radio(
    "Navigation Modules",
    [
        "🏆 Executive Auction Dashboard",
        "🏏 Layer 1: Overall Batters Pressure Rankings",
        "🎯 Layer 1: Overall Bowlers Pressure Rankings",
        "👑 Layer 2: RR Recruitment Intelligence & Categories",
        "⚡ Proprietary Ball Mechanics (Pace/Spin & Variations)",
        "🔬 Head-to-Head Player Comparison",
        "⚙️ Mathematical Engine & Pressure Formulation"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("""
<div style='font-size:0.73rem; color:#94a3b8; line-height: 1.5; padding: 0 4px;'>
    <b style="color:#f8fafc;">War Room Verified Dataset:</b><br/>
    • <b>200,999</b> Deliveries (2022–2026)<br/>
    • <b>192,445</b> Legal Balls Analyzed<br/>
    • <b>371</b> IPL + <b>496</b> T20I Matches<br/>
    • <b>MCC Cricket Rules Compliant</b>
</div>
""", unsafe_allow_html=True)

# Top Hero Header
st.markdown("""
<div class="rr-hero-banner">
    <div>
        <div class="rr-badge">Exclusive War Room Platform • Round 1 Analytics</div>
        <h1 class="rr-logo-title">RAJASTHAN ROYALS • SUPERR SELECTOR</h1>
        <p style="margin: 6px 0 0 0; color: #94a3b8; font-size: 0.92rem; font-weight: 400;">
            IPL 2027 Auction Intelligence System | Quantitative Pressure Reliability Engine
        </p>
    </div>
    <div style="text-align: right; z-index: 1;">
        <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,215,0,0.3); padding: 8px 16px; border-radius: 12px;">
            <span style="font-size: 1.4rem;">👑</span>
            <div style="text-align: left;">
                <div style="font-size: 0.68rem; color: #ffd700; font-weight: 700; letter-spacing: 1px;">HALLA BOL</div>
                <div style="font-size: 0.85rem; color: #fff; font-weight: 800;">AUCTION 2027</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Architecture explanation note
st.markdown("""
<div class="arch-banner">
    <b style="color:#ea1a7f;">Analytical Architecture Note:</b> This system maintains <b>two strictly separated analytical layers</b>:
    <br/>• <b>Layer 1 (Official Overall Pressure Rankings):</b> Evaluates all eligible players across the supplied IPL & T20I datasets based purely on high-pressure performance metrics, irrespective of franchise affiliation.
    <br/>• <b>Layer 2 (Rajasthan Royals Recruitment Intelligence):</b> Analyzes historical playing appearances, IPL vs T20I splits, batting positions, and auction availability to formulate realistic recruitment strategies for RR.
</div>
""", unsafe_allow_html=True)

# ==================== MODULE 1: EXECUTIVE DASHBOARD ====================
if nav == "🏆 Executive Auction Dashboard":
    st.markdown("### 📊 High-Leverage Tournament Overview")
    
    # 6 Premium KPI Cards
    st.markdown("""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-title">Total Deliveries</div>
            <div class="kpi-value">200,999</div>
            <div class="kpi-sub">All Balls (2022–2026)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Legal Deliveries</div>
            <div class="kpi-value">192,445</div>
            <div class="kpi-sub">8,554 Wides / No-Balls Excluded</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Matches Analyzed</div>
            <div class="kpi-value">867</div>
            <div class="kpi-sub">371 IPL | 496 T20I Active</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Pressure Deliveries</div>
            <div class="kpi-value">48,324</div>
            <div class="kpi-sub">24.04% High-Leverage Balls</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Qualified Batters</div>
            <div class="kpi-value">132</div>
            <div class="kpi-sub">≥60 Pressure Balls & ≥10 Matches</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Qualified Bowlers</div>
            <div class="kpi-value">158</div>
            <div class="kpi-sub">≥60 Pressure Balls & ≥10 Matches</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### 🏏 Layer 1: Batting Strike Rate Elevation Under Pressure")
        top_bat_chart = top_bat.sort_values(by='Rank', ascending=False)
        fig_bat = go.Figure()
        fig_bat.add_trace(go.Bar(
            y=top_bat_chart['player_name'],
            x=top_bat_chart['norm_strike_rate'],
            name='Normal Strike Rate',
            orientation='h',
            marker=dict(color='#334155', line=dict(color='rgba(255,255,255,0.1)', width=1)),
            hovertemplate='%{y}<br>Normal SR: %{x:.1f}<extra></extra>'
        ))
        fig_bat.add_trace(go.Bar(
            y=top_bat_chart['player_name'],
            x=top_bat_chart['press_strike_rate'],
            name='Pressure Strike Rate',
            orientation='h',
            marker=dict(color='#ea1a7f', line=dict(color='#ff6db3', width=1)),
            hovertemplate='%{y}<br>Pressure SR: %{x:.1f}<extra></extra>'
        ))
        fig_bat.update_layout(
            barmode='group',
            bargap=0.25,
            bargroupgap=0.1,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.4)',
            font=dict(color='#e2e8f0', family='Outfit'),
            margin=dict(l=0, r=20, t=10, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(title="Strike Rate (Runs per 100 Balls)", gridcolor='#1e293b', range=[100, 240]),
            yaxis=dict(gridcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_bat, use_container_width=True)
        
    with col_b:
        st.markdown("#### 🎯 Layer 1: Bowling Economy Rate Under Pressure (Runs Per Over)")
        top_bowl_chart = top_bowl.sort_values(by='Rank', ascending=False)
        fig_bowl = go.Figure()
        fig_bowl.add_trace(go.Bar(
            y=top_bowl_chart['player_name'],
            x=top_bowl_chart['norm_economy'],
            name='Normal Economy',
            orientation='h',
            marker=dict(color='#334155', line=dict(color='rgba(255,255,255,0.1)', width=1)),
            hovertemplate='%{y}<br>Normal Econ: %{x:.2f} rpo<extra></extra>'
        ))
        fig_bowl.add_trace(go.Bar(
            y=top_bowl_chart['player_name'],
            x=top_bowl_chart['press_economy'],
            name='Pressure Economy',
            orientation='h',
            marker=dict(color='#0ea5e9', line=dict(color='#38bdf8', width=1)),
            hovertemplate='%{y}<br>Pressure Econ: %{x:.2f} rpo<extra></extra>'
        ))
        fig_bowl.update_layout(
            barmode='group',
            bargap=0.25,
            bargroupgap=0.1,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.4)',
            font=dict(color='#e2e8f0', family='Outfit'),
            margin=dict(l=0, r=20, t=10, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(title="Economy Rate (Runs Per Over — Lower is Better)", gridcolor='#1e293b', range=[0, 11]),
            yaxis=dict(gridcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_bowl, use_container_width=True)
        
    st.divider()
    
    st.markdown("### 🏆 Recommended Top 10 Rankings – Unstop Entry")
    st.caption("Official model-generated rankings across all eligible players in the supplied dataset. Zero duplicate entries.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🏏 Recommended Top 10 Batters")
        bat_disp = top_bat[['Rank', 'player_name', 'team_name', 'press_balls_faced', 'norm_strike_rate', 'press_strike_rate', 'sr_lift', 'reliability_score']].copy()
        bat_disp['Rank_Badge'] = bat_disp['Rank'].apply(format_rank_badge)
        bat_disp = bat_disp[['Rank_Badge', 'player_name', 'team_name', 'press_balls_faced', 'norm_strike_rate', 'press_strike_rate', 'sr_lift', 'reliability_score']]
        bat_disp.columns = ['Rank', 'Player Name', 'Primary Team', 'Pressure Balls', 'Norm SR', 'Press SR', 'SR Lift (Δ)', 'Reliability Score']
        
        st.dataframe(
            bat_disp.style.format({
                'Norm SR': '{:.1f}',
                'Press SR': '{:.1f}',
                'SR Lift (Δ)': '+{:.1f}',
                'Reliability Score': '{:.2f}'
            }),
            use_container_width=True,
            hide_index=True
        )
        
    with c2:
        st.markdown("#### 🎯 Recommended Top 10 Bowlers")
        bowl_disp = top_bowl[['Rank', 'player_name', 'team_name', 'press_legal_balls', 'norm_economy', 'press_economy', 'econ_suppression', 'reliability_score']].copy()
        bowl_disp['Rank_Badge'] = bowl_disp['Rank'].apply(format_rank_badge)
        bowl_disp = bowl_disp[['Rank_Badge', 'player_name', 'team_name', 'press_legal_balls', 'norm_economy', 'press_economy', 'econ_suppression', 'reliability_score']]
        bowl_disp.columns = ['Rank', 'Player Name', 'Primary Team', 'Pressure Balls', 'Norm Econ', 'Press Econ', 'Econ Supp (Δ)', 'Reliability Score']
        
        st.dataframe(
            bowl_disp.style.format({
                'Norm Econ': '{:.2f}',
                'Press Econ': '{:.2f}',
                'Econ Supp (Δ)': '{:+.2f}',
                'Reliability Score': '{:.2f}'
            }),
            use_container_width=True,
            hide_index=True
        )

# ==================== MODULE 2: LAYER 1 - BATTERS RANKINGS ====================
elif nav == "🏏 Layer 1: Overall Batters Pressure Rankings":
    st.markdown("### 🏏 Layer 1: Overall Batters Pressure Rankings")
    st.markdown("Global evaluation of all 132 qualified batters across IPL and T20 International data based strictly on high-pressure performance.")
    
    # Scatter plot: Pressure SR vs Pressure Average with bubble size = volume
    fig_scatter = px.scatter(
        all_bat[all_bat['press_balls_faced'] >= 80],
        x='press_average',
        y='press_strike_rate',
        size='press_balls_faced',
        color='reliability_score',
        hover_name='player_name',
        hover_data=['team_name', 'sr_lift', 'press_boundary_pct'],
        color_continuous_scale='Magma',
        title="Clutch Frontier: Pressure Average vs Pressure Strike Rate (Min 80 Pressure Balls)",
        labels={'press_average': 'Pressure Batting Average', 'press_strike_rate': 'Pressure Strike Rate', 'reliability_score': 'Reliability Score'}
    )
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.6)',
        font=dict(color='#e2e8f0', family='Outfit'),
        xaxis=dict(gridcolor='#1e293b', title="Pressure Batting Average (Runs per Dismissal)"),
        yaxis=dict(gridcolor='#1e293b', title="Pressure Strike Rate")
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Format Comparison for Top Batters (IPL vs T20I)
    if bat_fmt is not None:
        st.markdown("#### 🌐 IPL vs T20I Format Breakdown (Top 10 Batters Under Pressure)")
        fig_bat_fmt = px.bar(
            bat_fmt[bat_fmt['is_high_pressure']],
            x='striker_name',
            y='sr',
            color='comp_type',
            barmode='group',
            title="Pressure Strike Rate by Tournament Format (IPL vs T20I)",
            labels={'striker_name': 'Player Name', 'sr': 'Pressure Strike Rate', 'comp_type': 'Competition Type'},
            color_discrete_map={'IPL': '#ea1a7f', 'T20I': '#0ea5e9', 'Other T20': '#ffd700'}
        )
        fig_bat_fmt.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.4)',
            font=dict(color='#e2e8f0', family='Outfit'),
            xaxis=dict(gridcolor='#1e293b', title=""),
            yaxis=dict(gridcolor='#1e293b', title="Pressure Strike Rate")
        )
        st.plotly_chart(fig_bat_fmt, use_container_width=True)
    
    st.markdown("#### 📋 Qualified Batters Master Table (Interactive Search & Sorting)")
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        search_bat = st.text_input("🔍 Search Batter by Name:", placeholder="Type player name (e.g., Virat, Rinku, Buttler)...")
    with col_f2:
        min_balls = st.slider("Filter by Minimum Pressure Balls Faced:", min_value=60, max_value=600, value=80, step=20)
        
    filtered_bat = all_bat[all_bat['press_balls_faced'] >= min_balls].copy()
    if search_bat:
        filtered_bat = filtered_bat[filtered_bat['player_name'].str.contains(search_bat, case=False, na=False)]
        
    filtered_bat = filtered_bat.sort_values(by='reliability_score', ascending=False).reset_index(drop=True)
    
    display_bat_master = filtered_bat[['player_name', 'team_name', 'norm_matches', 'press_innings', 'press_balls_faced', 
                                       'norm_strike_rate', 'press_strike_rate', 'sr_lift', 'norm_average', 'press_average', 
                                       'press_boundary_pct', 'press_dot_pct', 'reliability_score']].copy()
    display_bat_master.columns = ['Player Name', 'Team', 'Matches', 'Press Inns', 'Press Balls', 
                                  'Norm SR', 'Press SR', 'SR Lift (Δ)', 'Norm Avg', 'Press Avg', 
                                  'Boundary %', 'Dot %', 'Reliability Score']
    
    st.dataframe(
        display_bat_master.style.format({
            'Norm SR': '{:.1f}',
            'Press SR': '{:.1f}',
            'SR Lift (Δ)': '{:+.1f}',
            'Norm Avg': '{:.1f}',
            'Press Avg': '{:.1f}',
            'Boundary %': '{:.1f}%',
            'Dot %': '{:.1f}%',
            'Reliability Score': '{:.2f}'
        }),
        use_container_width=True,
        hide_index=True
    )

# ==================== MODULE 3: LAYER 1 - BOWLERS RANKINGS ====================
elif nav == "🎯 Layer 1: Overall Bowlers Pressure Rankings":
    st.markdown("### 🎯 Layer 1: Overall Bowlers Pressure Rankings")
    st.markdown("Global evaluation of all 158 qualified bowlers across IPL and T20 International data based strictly on high-pressure performance.")
    
    fig_bowl_scatter = px.scatter(
        all_bowl[all_bowl['press_legal_balls'] >= 80],
        x='press_economy',
        y='press_wickets',
        size='press_legal_balls',
        color='reliability_score',
        hover_name='player_name',
        hover_data=['team_name', 'econ_suppression', 'press_dot_pct'],
        color_continuous_scale='Viridis',
        title="Defensive Fortress: Pressure Economy vs Wickets Taken (Min 80 Pressure Balls)",
        labels={'press_economy': 'Pressure Economy (Runs/Over — Lower is Better)', 'press_wickets': 'Pressure Wickets Taken', 'reliability_score': 'Reliability Score'}
    )
    fig_bowl_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.6)',
        font=dict(color='#e2e8f0', family='Outfit'),
        xaxis=dict(gridcolor='#1e293b', autorange="reversed", title="Pressure Economy (Runs Per Over - Reversed Scale)"),
        yaxis=dict(gridcolor='#1e293b', title="Pressure Wickets Taken")
    )
    st.plotly_chart(fig_bowl_scatter, use_container_width=True)
    
    # Format Comparison for Top Bowlers (IPL vs T20I)
    if bowl_fmt is not None:
        st.markdown("#### 🌐 IPL vs T20I Format Breakdown (Top 10 Bowlers Under Pressure)")
        fig_bowl_fmt = px.bar(
            bowl_fmt[bowl_fmt['is_high_pressure']],
            x='bowler_name',
            y='econ',
            color='comp_type',
            barmode='group',
            title="Pressure Economy by Tournament Format (IPL vs T20I — Lower is Better)",
            labels={'bowler_name': 'Player Name', 'econ': 'Pressure Economy (Runs/Over)', 'comp_type': 'Competition Type'},
            color_discrete_map={'IPL': '#ea1a7f', 'T20I': '#0ea5e9', 'Other T20': '#ffd700'}
        )
        fig_bowl_fmt.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.4)',
            font=dict(color='#e2e8f0', family='Outfit'),
            xaxis=dict(gridcolor='#1e293b', title=""),
            yaxis=dict(gridcolor='#1e293b', title="Runs Per Over")
        )
        st.plotly_chart(fig_bowl_fmt, use_container_width=True)
    
    st.markdown("#### 📋 Qualified Bowlers Master Table")
    col_fb1, col_fb2 = st.columns([2, 1])
    with col_fb1:
        search_bowl = st.text_input("🔍 Search Bowler by Name:", placeholder="Type player name (e.g., Kuldeep, Narine, Rashid)...")
    with col_fb2:
        min_bowl_balls = st.slider("Filter by Minimum Pressure Legal Balls:", min_value=60, max_value=800, value=100, step=20)
        
    filtered_bowl = all_bowl[all_bowl['press_legal_balls'] >= min_bowl_balls].copy()
    if search_bowl:
        filtered_bowl = filtered_bowl[filtered_bowl['player_name'].str.contains(search_bowl, case=False, na=False)]
        
    filtered_bowl = filtered_bowl.sort_values(by='reliability_score', ascending=False).reset_index(drop=True)
    
    display_bowl_master = filtered_bowl[['player_name', 'team_name', 'norm_matches', 'press_legal_balls', 
                                         'norm_economy', 'press_economy', 'econ_suppression', 'press_wickets', 
                                         'norm_average', 'press_average', 'press_dot_pct', 'press_boundary_conceded_pct', 'reliability_score']].copy()
    display_bowl_master.columns = ['Player Name', 'Team', 'Matches', 'Press Balls', 
                                   'Norm Econ', 'Press Econ', 'Econ Supp (Δ)', 'Press Wkts', 
                                   'Norm Avg', 'Press Avg', 'Dot %', 'Bound Conc %', 'Reliability Score']
    
    st.dataframe(
        display_bowl_master.style.format({
            'Norm Econ': '{:.2f}',
            'Press Econ': '{:.2f}',
            'Econ Supp (Δ)': '{:+.2f}',
            'Norm Avg': '{:.1f}',
            'Press Avg': '{:.1f}',
            'Dot %': '{:.1f}%',
            'Bound Conc %': '{:.1f}%',
            'Reliability Score': '{:.2f}'
        }),
        use_container_width=True,
        hide_index=True
    )

# ==================== MODULE 4: LAYER 2 - RR RECRUITMENT INTELLIGENCE ====================
elif nav == "👑 Layer 2: RR Recruitment Intelligence & Categories":
    st.markdown("### 👑 Layer 2: Rajasthan Royals Recruitment Intelligence")
    st.markdown("Contextual auction strategy utilizing historical appearances (`playing_eleven.csv`), roster mappings (`competition_team_player_mapping.csv`), and tournament format breakdowns.")
    
    st.info("💡 **Methodology Rule:** Historical team affiliation denotes past playing appearances in the supplied 2022–2026 data. It does not imply current squad retention or automatic availability for the IPL 2027 Auction.")
    
    cat_tab1, cat_tab2, cat_tab3, cat_tab4 = st.tabs([
        "👑 1. Historical Rajasthan Royals Players",
        "🏢 2. Players from Other IPL Franchises",
        "🌍 3. International-Only Appearances",
        "🎯 4. Potential Auction Recruitment Candidates"
    ])
    
    with cat_tab1:
        st.markdown("#### 1. Historical Rajasthan Royals Players")
        st.caption("Players who have represented Rajasthan Royals (Team ID: 3) in official match records.")
        
        role_filter_rr = st.radio("Filter by Role:", ["Batters", "Bowlers"], horizontal=True, key="rr_role")
        if role_filter_rr == "Batters":
            rr_b = rec_bat[rec_bat['category'] == 'Historical Rajasthan Royals'].sort_values(by='reliability_score', ascending=False)
            disp_rr_b = rr_b[['player_name', 'batting_role', 'matches_played_p11', 'press_balls_faced', 'reliability_score', 'ipl_p_sr', 't20i_p_sr', 'ipl_franchises']].copy()
            disp_rr_b.columns = ['Player Name', 'Batting Position Role', 'Matches Played', 'Pressure Balls', 'Reliability Score', 'IPL Press SR', 'T20I Press SR', 'IPL Franchises Represented']
            st.dataframe(
                disp_rr_b.style.format({
                    'Reliability Score': '{:.2f}',
                    'IPL Press SR': '{:.1f}',
                    'T20I Press SR': '{:.1f}'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            rr_bw = rec_bowl[rec_bowl['category'] == 'Historical Rajasthan Royals'].sort_values(by='reliability_score', ascending=False)
            disp_rr_bw = rr_bw[['player_name', 'matches_played_p11', 'press_legal_balls', 'press_wickets', 'reliability_score', 'ipl_p_econ', 't20i_p_econ', 'ipl_franchises']].copy()
            disp_rr_bw.columns = ['Player Name', 'Matches Played', 'Pressure Balls', 'Pressure Wickets', 'Reliability Score', 'IPL Press Econ', 'T20I Press Econ', 'IPL Franchises Represented']
            st.dataframe(
                disp_rr_bw.style.format({
                    'Reliability Score': '{:.2f}',
                    'IPL Press Econ': '{:.2f}',
                    'T20I Press Econ': '{:.2f}'
                }),
                use_container_width=True,
                hide_index=True
            )
            
    with cat_tab2:
        st.markdown("#### 2. Players from Other IPL Franchises")
        st.caption("Players with confirmed appearances in the IPL playing XI for franchises other than Rajasthan Royals.")
        
        role_filter_ipl = st.radio("Filter by Role:", ["Batters", "Bowlers"], horizontal=True, key="other_ipl_role")
        if role_filter_ipl == "Batters":
            other_b = rec_bat[rec_bat['category'] == 'Other IPL Franchise'].sort_values(by='reliability_score', ascending=False)
            disp_other_b = other_b[['player_name', 'batting_role', 'matches_played_p11', 'press_balls_faced', 'reliability_score', 'ipl_p_sr', 't20i_p_sr', 'ipl_franchises']].head(25).copy()
            disp_other_b.columns = ['Player Name', 'Batting Position Role', 'Matches Played', 'Pressure Balls', 'Reliability Score', 'IPL Press SR', 'T20I Press SR', 'IPL Franchises Represented']
            st.dataframe(
                disp_other_b.style.format({
                    'Reliability Score': '{:.2f}',
                    'IPL Press SR': '{:.1f}',
                    'T20I Press SR': '{:.1f}'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            other_bw = rec_bowl[rec_bowl['category'] == 'Other IPL Franchise'].sort_values(by='reliability_score', ascending=False)
            disp_other_bw = other_bw[['player_name', 'matches_played_p11', 'press_legal_balls', 'press_wickets', 'reliability_score', 'ipl_p_econ', 't20i_p_econ', 'ipl_franchises']].head(25).copy()
            disp_other_bw.columns = ['Player Name', 'Matches Played', 'Pressure Balls', 'Pressure Wickets', 'Reliability Score', 'IPL Press Econ', 'T20I Press Econ', 'IPL Franchises Represented']
            st.dataframe(
                disp_other_bw.style.format({
                    'Reliability Score': '{:.2f}',
                    'IPL Press Econ': '{:.2f}',
                    'T20I Press Econ': '{:.2f}'
                }),
                use_container_width=True,
                hide_index=True
            )
            
    with cat_tab3:
        st.markdown("#### 3. Players with International-Only Appearances")
        st.caption("Players who have competed in bilateral T20I series or ICC World Cups without appearances in the IPL dataset.")
        
        role_filter_intl = st.radio("Filter by Role:", ["Batters", "Bowlers"], horizontal=True, key="intl_role")
        if role_filter_intl == "Batters":
            intl_b = rec_bat[rec_bat['category'] == 'International-Only'].sort_values(by='reliability_score', ascending=False)
            disp_intl_b = intl_b[['player_name', 'historical_teams', 'batting_role', 'matches_played_p11', 'press_balls_faced', 'reliability_score', 't20i_p_sr', 'press_average']].head(25).copy()
            disp_intl_b.columns = ['Player Name', 'National Team', 'Batting Position Role', 'T20I Matches', 'Pressure Balls', 'Reliability Score', 'T20I Press SR', 'Pressure Average']
            st.dataframe(
                disp_intl_b.style.format({
                    'Reliability Score': '{:.2f}',
                    'T20I Press SR': '{:.1f}',
                    'Pressure Average': '{:.1f}'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            intl_bw = rec_bowl[rec_bowl['category'] == 'International-Only'].sort_values(by='reliability_score', ascending=False)
            disp_intl_bw = intl_bw[['player_name', 'historical_teams', 'matches_played_p11', 'press_legal_balls', 'press_wickets', 'reliability_score', 't20i_p_econ', 'press_dot_pct']].head(25).copy()
            disp_intl_bw.columns = ['Player Name', 'National Team', 'T20I Matches', 'Pressure Balls', 'Pressure Wickets', 'Reliability Score', 'T20I Press Econ', 'Dot %']
            st.dataframe(
                disp_intl_bw.style.format({
                    'Reliability Score': '{:.2f}',
                    'T20I Press Econ': '{:.2f}',
                    'Dot %': '{:.1f}%'
                }),
                use_container_width=True,
                hide_index=True
            )
            
    with cat_tab4:
        st.markdown("#### 4. Potential Auction Recruitment Candidates (Shortlist)")
        st.caption("Shortlisted targets evaluated on pressure reliability, franchise tactical gaps (finishing, wrist-spin, death overs), and verified auction dynamics.")
        
        rec_choice = st.radio("Shortlist Category:", ["Target Batters", "Target Bowlers"], horizontal=True)
        
        if rec_choice == "Target Batters":
            target_batters = [
                {
                    "name": "Jos Buttler", "category": "Historical Rajasthan Royals", "role": "Top Order (Opener)", "team": "Rajasthan Royals",
                    "score": 87.39, "press_sr": 195.8, "ipl_sr": 201.0, "t20i_sr": 179.0, "balls": 261,
                    "strengths": "Proven RR anchor with a 201.0 IPL pressure SR and +40.4 SR lift under match pressure.",
                    "auction_note": "Core retention / RTM priority for Rajasthan Royals' top order."
                },
                {
                    "name": "Tristan Stubbs", "category": "Other IPL Franchise", "role": "Middle-Overs Finisher (No. 5-7)", "team": "Delhi Capitals",
                    "score": 86.01, "press_sr": 182.7, "ipl_sr": 190.4, "t20i_sr": 169.1, "balls": 457,
                    "strengths": "457 pressure balls faced; 39.8 pressure average; 190.4 IPL pressure strike rate against elite death bowling.",
                    "auction_note": "High-priority auction target if released; fills RR's middle-order power hitting void."
                },
                {
                    "name": "Glenn Phillips", "category": "Other IPL Franchise", "role": "Top-Middle Order (No. 3-4)", "team": "Sunrisers Hyderabad",
                    "score": 87.32, "press_sr": 201.4, "ipl_sr": 187.5, "t20i_sr": 203.1, "balls": 219,
                    "strengths": "Massive +52.7 SR lift under pressure; 203.1 T20I pressure SR; elite boundary clearing against spin and pace.",
                    "auction_note": "Versatile overseas paddle target capable of wicketkeeping and bowling part-time off-spin."
                },
                {
                    "name": "Namboori Tilak Varma", "category": "Other IPL Franchise", "role": "Top-Middle Order (No. 3-4)", "team": "Mumbai Indians",
                    "score": 83.93, "press_sr": 181.3, "ipl_sr": 180.2, "t20i_sr": 183.5, "balls": 562,
                    "strengths": "562 pressure balls at 181.3 SR and 36.4 average; absorbs collapses and accelerates with 180+ strike rate.",
                    "auction_note": "Long-term domestic cornerstone (age 23); ideal left-handed stabilizer for Sawai Mansingh Stadium."
                },
                {
                    "name": "Dhruv Jurel", "category": "Historical Rajasthan Royals", "role": "Middle-Overs Finisher (No. 5-7)", "team": "Rajasthan Royals",
                    "score": 76.16, "press_sr": 176.3, "ipl_sr": 178.5, "t20i_sr": 50.0, "balls": 232,
                    "strengths": "178.5 IPL pressure SR; 34.1 pressure average; homegrown RR finisher proven in high-stakes run chases.",
                    "auction_note": "Uncapped/Domestic retention target; crucial Indian middle-order continuity."
                }
            ]
            
            for p in target_batters:
                st.markdown(f"""
                <div class="recruitment-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <div>
                            <span style="font-size: 1.25rem; font-weight: 800; color: #f8fafc;">{p['name']}</span>
                            <span style="margin-left: 8px;" class="badge-cat-rr" if "{p['category']}" == "Historical Rajasthan Royals" else "badge-cat-ipl">{p['category']}</span>
                            <div style="font-size: 0.82rem; color: #38bdf8; font-weight: 600; margin-top: 3px;">{p['role']} • {p['team']}</div>
                        </div>
                        <div style="text-align: right;">
                            <span class="badge-rec">Reliability Score: {p['score']:.2f}</span>
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px; margin: 10px 0; flex-wrap: wrap;">
                        <span class="badge-stat">Overall Press SR: {p['press_sr']}</span>
                        <span class="badge-stat">IPL Press SR: {p['ipl_sr']}</span>
                        <span class="badge-stat">T20I Press SR: {p['t20i_sr']}</span>
                        <span class="badge-stat">Volume: {p['balls']} Balls</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #cbd5e1; margin-top: 4px;">
                        <b>📊 Empirical Strengths:</b> {p['strengths']}
                    </div>
                    <div style="font-size: 0.82rem; color: #ff6db3; margin-top: 4px;">
                        <b>🎯 Auction Availability & Strategy:</b> {p['auction_note']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        else:
            target_bowlers = [
                {
                    "name": "Kuldeep Yadav", "category": "Other IPL Franchise", "role": "Left-Arm Wrist Spinner", "team": "Delhi Capitals",
                    "score": 99.55, "press_econ": 6.84, "ipl_econ": 7.13, "t20i_econ": 5.93, "wickets": 41, "balls": 379,
                    "strengths": "Economy drops to 6.84 under pressure; 41 wickets at 10.54 average; 5.93 rpo in international pressure overs.",
                    "auction_note": "Marquee auction target if not retained by DC; highest-impact clutch spinner in world cricket."
                },
                {
                    "name": "Noor Ahmad", "category": "Other IPL Franchise", "role": "Left-Arm Mystery Wrist Spin", "team": "Gujarat Titans",
                    "score": 90.50, "press_econ": 7.36, "ipl_econ": 7.23, "t20i_econ": 7.81, "wickets": 27, "balls": 283,
                    "strengths": "7.36 pressure economy; 12.85 bowling average; sharp trajectory variations that deceive both RHB and LHB.",
                    "auction_note": "Young overseas spinner with high upside; ideal fit for Sawai Mansingh Stadium's larger dimensions."
                },
                {
                    "name": "Wanindu Hasaranga", "category": "Historical Rajasthan Royals", "role": "Leg-Spin All-Rounder", "team": "Rajasthan Royals",
                    "score": 85.28, "press_econ": 7.63, "ipl_econ": 7.41, "t20i_econ": 7.76, "wickets": 36, "balls": 361,
                    "strengths": "36 high-pressure wickets at 12.75 average; strike rate of 10.0 balls per wicket under match pressure.",
                    "auction_note": "Previous RR squad member; proven middle-overs wicket-taker and lower-order batting resource."
                },
                {
                    "name": "Abrar Ahmed", "category": "International-Only", "role": "Mystery Leg-Spinner", "team": "Pakistan",
                    "score": 91.56, "press_econ": 4.86, "ipl_econ": 0.0, "t20i_econ": 4.86, "wickets": 16, "balls": 215,
                    "strengths": "Lowest pressure economy in the dataset (4.86 rpo); 51.4% dot ball density; takes a wicket every 13.4 balls.",
                    "auction_note": "International-only performer; monitor participation eligibility for future global franchise deployment."
                }
            ]
            
            for p in target_bowlers:
                st.markdown(f"""
                <div class="recruitment-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <div>
                            <span style="font-size: 1.25rem; font-weight: 800; color: #f8fafc;">{p['name']}</span>
                            <span style="margin-left: 8px;" class="badge-cat-rr" if "{p['category']}" == "Historical Rajasthan Royals" else "badge-cat-ipl">{p['category']}</span>
                            <div style="font-size: 0.82rem; color: #38bdf8; font-weight: 600; margin-top: 3px;">{p['role']} • {p['team']}</div>
                        </div>
                        <div style="text-align: right;">
                            <span class="badge-rec">Reliability Score: {p['score']:.2f}</span>
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px; margin: 10px 0; flex-wrap: wrap;">
                        <span class="badge-stat">Overall Press Econ: {p['press_econ']:.2f} rpo</span>
                        <span class="badge-stat">IPL Press Econ: {p['ipl_econ']:.2f} rpo</span>
                        <span class="badge-stat">T20I Press Econ: {p['t20i_econ']:.2f} rpo</span>
                        <span class="badge-stat">Wickets: {p['wickets']}</span>
                        <span class="badge-stat">Volume: {p['balls']} Balls</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #cbd5e1; margin-top: 4px;">
                        <b>📊 Empirical Strengths:</b> {p['strengths']}
                    </div>
                    <div style="font-size: 0.82rem; color: #38bdf8; margin-top: 4px;">
                        <b>🎯 Auction Availability & Strategy:</b> {p['auction_note']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ==================== MODULE 5: PROPRIETARY TRACKING MECHANICS ====================
elif nav == "⚡ Proprietary Ball Mechanics (Pace/Spin & Variations)":
    st.markdown("### ⚡ Rajasthan Royals Proprietary Ball Mechanics Analysis")
    st.markdown("Deep dive into ball speed, variations (yorkers, cutters, bouncers), and batter pace/spin matchups under pressure.")
    
    tab1, tab2, tab3 = st.tabs(["🏏 Batter Matchup: Pace vs Spin", "🎯 Bowler Delivery Variations", "🚀 Bowling Speed Impact"])
    
    with tab1:
        st.markdown("#### Batter Pressure Performance Split by Bowling Type")
        selected_batter = st.selectbox(
            "Select Batter to Inspect Matchup:",
            sorted(bat_split['striker_name'].unique()),
            index=sorted(bat_split['striker_name'].unique()).index("Virat Kohli") if "Virat Kohli" in bat_split['striker_name'].unique() else 0
        )
        b_data = bat_split[bat_split['striker_name'] == selected_batter].copy()
        
        b_disp = b_data[['pace_or_spin', 'runs', 'balls', 'sr', 'average', 'boundary_pct', 'dot_pct', 'dismissals']].copy()
        b_disp.columns = ['Bowling Type Faced', 'Runs Scored', 'Balls Faced', 'Strike Rate', 'Average', 'Boundary %', 'Dot %', 'Dismissals']
        
        st.dataframe(
            b_disp.style.format({
                'Strike Rate': '{:.1f}',
                'Average': '{:.1f}',
                'Boundary %': '{:.1f}%',
                'Dot %': '{:.1f}%'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        fig_b_split = px.bar(
            b_data, x='pace_or_spin', y='sr', color='pace_or_spin',
            text='sr', title=f"{selected_batter}: Strike Rate Under Pressure vs Pace and Spin",
            color_discrete_map={'Pace': '#ea1a7f', 'Spin': '#0ea5e9'}
        )
        fig_b_split.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Outfit'),
            xaxis=dict(title="Bowling Type Faced"),
            yaxis=dict(title="Strike Rate")
        )
        st.plotly_chart(fig_b_split, use_container_width=True)
        
    with tab2:
        st.markdown("#### Bowler Variation Breakdown in High Pressure Situations")
        selected_bowler = st.selectbox(
            "Select Bowler to Inspect Delivery Styles:",
            sorted(bowl_style['bowler_name'].unique()),
            index=sorted(bowl_style['bowler_name'].unique()).index("Kuldeep Yadav") if "Kuldeep Yadav" in bowl_style['bowler_name'].unique() else 0
        )
        bowler_vars = bowl_style[bowl_style['bowler_name'] == selected_bowler].sort_values(by='legal_balls', ascending=False).copy()
        
        bv_disp = bowler_vars[['delivery_style', 'legal_balls', 'runs', 'wickets', 'economy', 'dot_pct', 'strike_rate']].copy()
        bv_disp.columns = ['Delivery Style', 'Legal Balls', 'Runs Conceded', 'Wickets', 'Economy (Runs/Over)', 'Dot %', 'Strike Rate']
        
        st.dataframe(
            bv_disp.style.format({
                'Economy (Runs/Over)': '{:.2f}',
                'Dot %': '{:.1f}%',
                'Strike Rate': '{:.1f}'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        fig_var = px.bar(
            bowler_vars.head(8), x='delivery_style', y='economy', color='wickets',
            title=f"{selected_bowler}: Economy by Delivery Variation",
            labels={'economy': 'Economy (Runs/Over)', 'delivery_style': 'Delivery Style', 'wickets': 'Wickets'},
            color_continuous_scale='Teal'
        )
        fig_var.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Outfit'),
            xaxis=dict(title="Delivery Variation"),
            yaxis=dict(title="Economy (Runs Per Over)")
        )
        st.plotly_chart(fig_var, use_container_width=True)
        
    with tab3:
        st.markdown("#### Pace Bowling Speed Tiers Under Pressure")
        spd_disp = speed_summary.copy()
        spd_disp.columns = ['Speed Tier', 'Legal Balls', 'Runs Conceded', 'Wickets Taken', 'Boundaries Conceded', 'Dot Deliveries', 'Economy (Runs/Over)', 'Strike Rate', 'Dot %']
        
        st.dataframe(
            spd_disp.style.format({
                'Economy (Runs/Over)': '{:.2f}',
                'Strike Rate': '{:.1f}',
                'Dot %': '{:.1f}%'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        fig_spd = px.bar(
            speed_summary, x='speed_bin', y='economy', text='economy',
            color='strike_rate', title="Speed Tiers: Economy vs Wicket Strike Rate",
            color_continuous_scale='Sunset'
        )
        fig_spd.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', family='Outfit'),
            xaxis=dict(title="Pace Speed Tiers"),
            yaxis=dict(title="Economy (Runs Per Over)")
        )
        st.plotly_chart(fig_spd, use_container_width=True)
        st.info("💡 **War Room Finding:** Cutters and slower balls (<120 kph) yield lower economy (9.2 rpo) than express pace (145+ kph), which gets punished at 10.4 rpo in high-pressure death overs.")

# ==================== MODULE 6: PLAYER COMPARISON ====================
elif nav == "🔬 Head-to-Head Player Comparison":
    st.markdown("### 🔬 Head-to-Head Player Comparison Matrix")
    role = st.radio("Select Player Role", ["Batters", "Bowlers"], horizontal=True)
    
    if role == "Batters":
        p_list = sorted(all_bat['player_name'].unique())
        c1, c2 = st.columns(2)
        with c1:
            p1 = st.selectbox("Player 1", p_list, index=p_list.index("Virat Kohli") if "Virat Kohli" in p_list else 0)
        with c2:
            p2 = st.selectbox("Player 2", p_list, index=p_list.index("Suryakumar Yadav") if "Suryakumar Yadav" in p_list else 1)
            
        r1 = all_bat[all_bat['player_name'] == p1].iloc[0]
        r2 = all_bat[all_bat['player_name'] == p2].iloc[0]
        
        comp_df = pd.DataFrame({
            "Metric": ["Reliability Score", "Pressure SR", "Normal SR", "SR Lift (Δ)", "Pressure Avg", "Normal Avg", "Pressure Boundary %", "Dot Ball %", "Pressure Balls Faced"],
            p1: [f"{r1['reliability_score']:.2f}", f"{r1['press_strike_rate']:.1f}", f"{r1['norm_strike_rate']:.1f}", f"{r1['sr_lift']:+.1f}", f"{r1['press_average']:.1f}", f"{r1['norm_average']:.1f}", f"{r1['press_boundary_pct']:.1f}%", f"{r1['press_dot_pct']:.1f}%", f"{int(r1['press_balls_faced']):,}"],
            p2: [f"{r2['reliability_score']:.2f}", f"{r2['press_strike_rate']:.1f}", f"{r2['norm_strike_rate']:.1f}", f"{r2['sr_lift']:+.1f}", f"{r2['press_average']:.1f}", f"{r2['norm_average']:.1f}", f"{r2['press_boundary_pct']:.1f}%", f"{r2['press_dot_pct']:.1f}%", f"{int(r2['press_balls_faced']):,}"],
        })
        st.dataframe(comp_df, use_container_width=True, hide_index=True)
    else:
        p_list = sorted(all_bowl['player_name'].unique())
        c1, c2 = st.columns(2)
        with c1:
            p1 = st.selectbox("Player 1", p_list, index=p_list.index("Kuldeep Yadav") if "Kuldeep Yadav" in p_list else 0)
        with c2:
            p2 = st.selectbox("Player 2", p_list, index=p_list.index("Sunil Narine") if "Sunil Narine" in p_list else 1)
            
        r1 = all_bowl[all_bowl['player_name'] == p1].iloc[0]
        r2 = all_bowl[all_bowl['player_name'] == p2].iloc[0]
        
        comp_df = pd.DataFrame({
            "Metric": ["Reliability Score", "Pressure Economy", "Normal Economy", "Economy Suppression (Δ)", "Pressure Bowling Avg", "Normal Bowling Avg", "Pressure Dot %", "Boundary Conceded %", "Pressure Wickets", "Pressure Balls"],
            p1: [f"{r1['reliability_score']:.2f}", f"{r1['press_economy']:.2f}", f"{r1['norm_economy']:.2f}", f"{r1['econ_suppression']:+.2f}", f"{r1['press_average']:.1f}", f"{r1['norm_average']:.1f}", f"{r1['press_dot_pct']:.1f}%", f"{r1['press_boundary_conceded_pct']:.1f}%", f"{int(r1['press_wickets'])}", f"{int(r1['press_legal_balls']):,}"],
            p2: [f"{r2['reliability_score']:.2f}", f"{r2['press_economy']:.2f}", f"{r2['norm_economy']:.2f}", f"{r2['econ_suppression']:+.2f}", f"{r2['press_average']:.1f}", f"{r2['norm_average']:.1f}", f"{r2['press_dot_pct']:.1f}%", f"{r2['press_boundary_conceded_pct']:.1f}%", f"{int(r2['press_wickets'])}", f"{int(r2['press_legal_balls']):,}"],
        })
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

# ==================== MODULE 7: METHODOLOGY & MATHEMATICAL ENGINE ====================
elif nav == "⚙️ Mathematical Engine & Pressure Formulation":
    st.markdown("### ⚙️ Mathematical Engine & Pressure Formulation")
    st.markdown("""
    #### 1. Two-Layer Analytical Architecture
    - **Layer 1 (Official Overall Rankings):** Follows the official competition requirements. Ranks all qualified batters and bowlers across the entire 200,999 delivery dataset without bias toward franchise ownership.
    - **Layer 2 (Rajasthan Royals Recruitment Intelligence):** Connects performance metrics with verified appearance records from `playing_eleven.csv`, categorizing players into Historical RR, Other IPL Franchises, and International-Only players to inform auction shortlist decisions.
    
    #### 2. Pre-Delivery Match State Architecture
    In cricket analytics, pressure must be evaluated at the **instant before each delivery is bowled**:
    - **Current Team Score ($S$)** and **Wickets Lost ($W$)** represent the situation prior to the ball.
    - **Legal Balls Bowled ($B_{\\text{bowled}}$)** strictly increments on legal balls (excluding wides and no-balls).
    - **Required Run Rate (RRR)** in chases is calculated dynamically:
      $$\\text{RRR} = \\frac{\\text{Target} - S}{(120 - B_{\\text{bowled}})/6}$$
      
    #### 3. Innings-Specific Dynamic Match Pressure ($P \\in [0, 1]$)
    
    **Second-Innings Chasing:**
    $$P_{\\text{chase}} = \\left[ 0.55 \\cdot f_{\\text{RRR}} + 0.35 \\cdot f_{\\text{wkt}} + 0.10 \\cdot f_{\\text{death}} \\right] \\times \\tau(B_{\\text{rem}})$$
    - $f_{\\text{RRR}} = \\text{clip}\\left(\\frac{\\text{RRR} - 7.0}{7.0}, 0, 1.5\\right)$
    - $f_{\\text{wkt}} = \\text{clip}\\left(\\frac{10 - \\text{WIH}}{6.0}, 0, 1.5\\right)$
    - Urgency Multiplier: $\\tau(B_{\\text{rem}}) = 1.3\\times$ if $B_{\\text{rem}} \\le 30$; $1.1\\times$ if $B_{\\text{rem}} \\le 60$.
    
    **First-Innings Setting:**
    - **Early Collapse Pressure:** $\\ge 3$ wickets lost in the Powerplay (Overs 1–6).
    - **Middle Crisis Pressure:** $\\ge 5$ wickets lost before Over 15.
    - **Death Overs Boundary Acceleration:** Overs 16–20 boundary demand ($0.75\\text{--}0.95$).
    
    #### 4. Bayesian Sample-Size Confidence Shrinkage
    To prevent unproven players with small sample sizes from dominating the rankings, raw scores are shrunk toward the population baseline (50.0):
    $$S_{\\text{final}} = (S_{\\text{raw}} \\times C) + (50.0 \\times (1 - C))$$
    where:
    $$C = 0.60 + 0.40\\sqrt{\\text{clip}\\left(\\frac{N - N_{\\min}}{N_{\\text{target}} - N_{\\min}}, 0, 1\\right)}$$
    - Batters: $N_{\\min} = 60$ pressure balls, $N_{\\text{target}} = 250$ balls.
    - Bowlers: $N_{\\min} = 60$ pressure balls, $N_{\\text{target}} = 250$ balls.
    """)
