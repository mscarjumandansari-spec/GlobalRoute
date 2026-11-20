import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="GlobalRoute | 3D Geopolitical & Trade Command", layout="wide")

st.markdown("""
<style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    .exec-header { border-bottom: 1px solid #2D333B; padding-bottom: 1rem; margin-bottom: 1.4rem; }
    .exec-badge {
        display: inline-block; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.08em;
        text-transform: uppercase; color: #00CC96; background-color: rgba(0, 204, 150, 0.1);
        border: 1px solid rgba(0, 204, 150, 0.3); padding: 3px 10px; border-radius: 4px; margin-bottom: 0.5rem;
    }
    .exec-title { font-size: 1.8rem; font-weight: 700; color: #F0F6FC; letter-spacing: -0.02em; margin: 0; line-height: 1.25; }
    .exec-subtitle { font-size: 0.9rem; color: #8B949E; margin-top: 0.35rem; }
    .kpi-card {
        background-color: #161B22; border: 1px solid #30363D; border-top: 3px solid #00CC96;
        border-radius: 6px; padding: 14px 16px; margin-bottom: 1rem;
    }
    .kpi-label { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #8B949E; margin-bottom: 6px; }
    .kpi-value { font-size: 1.42rem; font-weight: 700; color: #F0F6FC; letter-spacing: -0.01em; }
    .kpi-sub { font-size: 0.75rem; color: #00CC96; margin-top: 4px; }
</style>

<div class="exec-header">
    <div class="exec-badge">Global Supply Chain &amp; Trade Intelligence •</div>
    <h1 class="exec-title">GLOBALROUTE: Cross-Border Multi-Modal &amp; Tariff Optimization System</h1>
    <div class="exec-subtitle">
        Quantitative Decision-Support Platform for Geopolitical Corridor Routing, EU CBAM Carbon Valuation &amp; Working Capital Efficiency
    </div>
</div>
""", unsafe_allow_html=True)


# --- SIDEBAR: MANAGER CONTROLS ---
st.sidebar.header("📦 Shipment & Capital Parameters")
origin_city = st.sidebar.selectbox("Origin Manufacturing Hub", ["Shenzhen, China", "Ningbo, China", "Chongqing, China"])
dest_city = st.sidebar.selectbox("Destination Market", ["Hamburg, Germany", "Rotterdam, Netherlands", "Warsaw, Poland"])
units = st.sidebar.number_input("Shipment Volume (Units)", min_value=1000, max_value=500000, value=50000, step=5000)
unit_value = st.sidebar.number_input("Manufacturing Value per Unit ($)", min_value=10, max_value=1000, value=60)
cost_of_capital = st.sidebar.slider("Annual Cost of Working Capital (%)", 2.0, 15.0, 8.0, step=0.5)
total_cargo_value = units * unit_value

st.sidebar.header("⚡ Geopolitical & Carbon Shock Simulator")
tariff_hike = st.sidebar.slider("Surprise Direct-Route Tariff Hike (%)", 0, 50, 25)
carbon_tax_per_ton = st.sidebar.slider("EU CBAM Carbon Price ($ / Metric Ton CO₂)", 0, 150, 85)
red_sea_crisis = st.sidebar.checkbox("Simulate Red Sea Disruption (+14d & Cape Detour)", value=True)
rail_congestion = st.sidebar.checkbox("Simulate Border Rail Congestion (+4d Rail)", value=False)

st.sidebar.header("🎯 Executive Priority Weights")
w_cost = st.sidebar.slider("Total Landed Cost Sensitivity (%)", 0, 100, 45)
w_speed = st.sidebar.slider("Lead-Time Speed Sensitivity (%)", 0, 100, 25)
w_risk = st.sidebar.slider("Geopolitical Safety Sensitivity (%)", 0, 100, 20)
w_esg = st.sidebar.slider("Low-Carbon / ESG Sensitivity (%)", 0, 100, 10)

st.sidebar.markdown("---")
uploaded_rates = st.sidebar.file_uploader(
    "📂 Upload Custom Carrier Rates (CSV)",
    type=["csv"],
    help="Upload custom routes to override the default simulator data."
)

sample_csv = (
    "Route,Mode,Freight_Per_Unit,Days,Tariff_Pct,Risk,CO2_Kg_Per_Unit\n"
    "Maersk Express Sea (Shenzhen -> Hamburg),Ocean Express,3.90,32,12.0,4.5,0.42\n"
    "DHL Priority Air Charter (Shenzhen -> Hamburg),Air Charter,16.50,2,25.0,1.2,9.50\n"
    "Jebel Ali Sea-Air Bridge (Shenzhen -> Dubai -> Hamburg),Hybrid Sea-Air,7.80,13,2.5,2.0,2.10\n"
    "Eurasia Northern Rail Corridor (Chongqing -> Hamburg),Block Train,6.20,17,14.5,3.8,1.10\n"
).encode("utf-8")

st.sidebar.download_button(
    label="📄 Download Sample CSV Template",
    data=sample_csv,
    file_name="sample_carrier_rates.csv",
    mime="text/csv"
)

# --- COORDINATES FOR DYNAMIC HUBS ---
hub_coords = {
    "Shenzhen": (22.54, 114.05),
    "Ningbo": (29.86, 121.54),
    "Chongqing": (29.56, 106.55),
    "Hamburg": (53.55, 9.99),
    "Rotterdam": (51.92, 4.47),
    "Warsaw": (52.23, 21.01)
}

origin_name = origin_city.partition(",")[0]
dest_name = dest_city.partition(",")[0]
orig_lat, orig_lon = hub_coords[origin_name]
dest_lat, dest_lon = hub_coords[dest_name]

# --- ROUTE DATA MODEL ---
if uploaded_rates is not None:
    custom_df = pd.read_csv(uploaded_rates)
    routes = []
    for _, r in custom_df.iterrows():
        routes.append({
            "Route": r["Route"],
            "Mode": r["Mode"],
            "Base_Freight_Per_Unit": float(r["Freight_Per_Unit"]),
            "Transit_Days": int(r["Days"]),
            "Base_Tariff_Pct": float(r["Tariff_Pct"]),
            "Risk_Score": float(r["Risk"]),
            "CO2_Kg_Per_Unit": float(r["CO2_Kg_Per_Unit"]),
            "Path_Lats": [orig_lat, 25.20, dest_lat],
            "Path_Lons": [orig_lon, 55.27, dest_lon]
        })
else:
    routes = [
        {
            "Route": f"Direct Sea Freight ({origin_name} → {dest_name})",
            "Mode": "Direct Sea",
            "Base_Freight_Per_Unit": 2.20 + (1.50 if red_sea_crisis else 0.0),
            "Transit_Days": 35 + (14 if red_sea_crisis else 0),
            "Base_Tariff_Pct": 4.0 + tariff_hike,
            "Risk_Score": 8.5 if red_sea_crisis else 3.5,
            "CO2_Kg_Per_Unit": 0.48 if red_sea_crisis else 0.35,
            "Path_Lats": [orig_lat, 1.29, -34.35, 14.71, 36.14, dest_lat] if red_sea_crisis else [orig_lat, 1.29, 12.60, 29.96, 36.14, dest_lat],
            "Path_Lons": [orig_lon, 103.85, 18.47, -17.46, -5.35, dest_lon] if red_sea_crisis else [orig_lon, 103.85, 43.33, 32.55, -5.35, dest_lon]
        },
        {
            "Route": f"China-Europe Railway Express (Chongqing → {dest_name})",
            "Mode": "China-Europe Rail",
            "Base_Freight_Per_Unit": 6.80,
            "Transit_Days": 16 + (4 if rail_congestion else 0),
            "Base_Tariff_Pct": 4.0 + (tariff_hike * 0.5),
            "Risk_Score": 4.5 if rail_congestion else 3.0,
            "CO2_Kg_Per_Unit": 1.15,
            "Path_Lats": [29.56, 43.82, 45.17, 51.16, 52.23, dest_lat],
            "Path_Lons": [106.55, 87.61, 82.58, 71.47, 21.01, dest_lon]
        },
        {
            "Route": f"Multi-Modal Re-Export Hub ({origin_name} → Dubai Hub → {dest_name})",
            "Mode": "Sea + Air Hub",
            "Base_Freight_Per_Unit": 8.50,
            "Transit_Days": 14,
            "Base_Tariff_Pct": 2.5,
            "Risk_Score": 2.2,
            "CO2_Kg_Per_Unit": 2.40,
            "Path_Lats": [orig_lat, 1.29, 18.92, 25.20, 41.01, dest_lat],
            "Path_Lons": [orig_lon, 103.85, 72.83, 55.27, 28.97, dest_lon]
        },
        {
            "Route": f"Direct Air Cargo ({origin_name} → {dest_name})",
            "Mode": "Direct Air",
            "Base_Freight_Per_Unit": 18.00,
            "Transit_Days": 3,
            "Base_Tariff_Pct": 4.0 + tariff_hike,
            "Risk_Score": 1.5,
            "CO2_Kg_Per_Unit": 9.80,
            "Path_Lats": [orig_lat, 39.90, 55.75, dest_lat],
            "Path_Lons": [orig_lon, 116.40, 37.61, dest_lon]
        }
    ]

df = pd.DataFrame(routes)

# --- TRUE LANDED COST ENGINE (FREIGHT + TARIFF + CARBON + WORKING CAPITAL) ---
df["Total_Freight ($)"] = df["Base_Freight_Per_Unit"] * units
df["Total_Tariff ($)"] = total_cargo_value * (df["Base_Tariff_Pct"] / 100.0)
df["CO2_Tons"] = ((df["CO2_Kg_Per_Unit"] * units) / 1000.0).round(1)
df["Carbon_CBAM_Cost ($)"] = df["CO2_Tons"] * carbon_tax_per_ton
df["Capital_Holding_Cost ($)"] = total_cargo_value * (cost_of_capital / 100.0) * (df["Transit_Days"] / 365.0)
df["True_Landed_Cost ($)"] = (
    df["Total_Freight ($)"] +
    df["Total_Tariff ($)"] +
    df["Carbon_CBAM_Cost ($)"] +
    df["Capital_Holding_Cost ($)"]
)

# Normalize metrics (0 to 1, lower is better)
norm_cost = df["True_Landed_Cost ($)"] / df["True_Landed_Cost ($)"].max()
norm_speed = df["Transit_Days"] / df["Transit_Days"].max()
norm_risk = df["Risk_Score"] / 10.0
norm_esg = df["CO2_Tons"] / df["CO2_Tons"].max()

total_w = max(w_cost + w_speed + w_risk + w_esg, 1)
df["Penalty_Index"] = (
    (w_cost * norm_cost) +
    (w_speed * norm_speed) +
    (w_risk * norm_risk) +
    (w_esg * norm_esg)
) / total_w
df["Optimization_Score"] = ((1 - df["Penalty_Index"]) * 100).round(1)

df = df.sort_values(by="Optimization_Score", ascending=False).reset_index(drop=True)
best_route = df.head(1).squeeze()
worst_route = df.tail(1).squeeze()
savings = worst_route["True_Landed_Cost ($)"] - best_route["True_Landed_Cost ($)"]

# --- EXECUTIVE KPI CARDS ---
# --- EXECUTIVE KPI CARDS ---
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Optimal Corridor Mode</div>
        <div class="kpi-value">{best_route['Mode']}</div>
        <div class="kpi-sub">Score: {best_route['Optimization_Score']}/100</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">True Landed Cost</div>
        <div class="kpi-value">${best_route['True_Landed_Cost ($)']:,.0f}</div>
        <div class="kpi-sub">${best_route['True_Landed_Cost ($)'] / units:,.2f} / unit</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Lead Time</div>
        <div class="kpi-value">{best_route['Transit_Days']} Days</div>
        <div class="kpi-sub">Door-to-Port Transit</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Scope 3 Carbon Footprint</div>
        <div class="kpi-value">{best_route['CO2_Tons']:,.1f} tCO₂</div>
        <div class="kpi-sub">CBAM: ${best_route['Carbon_CBAM_Cost ($)']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Net Strategy Savings</div>
        <div class="kpi-value">${savings:,.0f}</div>
        <div class="kpi-sub">vs. Highest-Penalty Route</div>
    </div>
    """, unsafe_allow_html=True)


st.success(
    f"**Executive Strategy Brief:** Deploy **{best_route['Route']}** "
    f"(Command Score: **{best_route['Optimization_Score']}/100**). "
    f"Factoring in customs tariffs, EU CBAM carbon pricing (**${best_route['Carbon_CBAM_Cost ($)']:,.0f}**), "
    f"and inventory capital lockup (**${best_route['Capital_Holding_Cost ($)']:,.0f}**), this corridor saves **${savings:,.0f}** over the worst alternative."
)

# --- 360° INTERACTIVE 3D GLOBE & RADAR INTELLIGENCE ---
map_col, radar_col = st.columns([1.65, 1])

with map_col:
    st.subheader("🌍 360° Interactive Global Corridor Globe (Drag to Rotate)")
    fig_globe = go.Figure()

    for idx, row in df.iterrows():
        is_best = (idx == 0)
        fig_globe.add_trace(go.Scattergeo(
            lat=row["Path_Lats"],
            lon=row["Path_Lons"],
            mode="lines+markers",
            name=f"{'★ ' if is_best else ''}{row['Mode']} (${row['True_Landed_Cost ($)']:,.0f})",
            line=dict(
                width=5 if is_best else 2.2,
                color="#00CC96" if is_best else "#EF553B",
                dash="solid" if is_best else "dot"
            ),
            marker=dict(size=7 if is_best else 4),
            hoverinfo="text",
            text=(
                f"<b>{row['Route']}</b><br>"
                f"True Landed Cost: ${row['True_Landed_Cost ($)']:,.0f}<br>"
                f"Transit Time: {row['Transit_Days']} Days<br>"
                f"Carbon Footprint: {row['CO2_Tons']} tCO₂<br>"
                f"Score: {row['Optimization_Score']}/100"
            )
        ))

    hubs = pd.DataFrame([
        {"Name": f"{origin_name} (Origin)", "Lat": orig_lat, "Lon": orig_lon},
        {"Name": "Chongqing Hub", "Lat": 29.56, "Lon": 106.55},
        {"Name": "Dubai Free-Zone", "Lat": 25.20, "Lon": 55.27},
        {"Name": f"{dest_name} (Market)", "Lat": dest_lat, "Lon": dest_lon},
    ])

    fig_globe.add_trace(go.Scattergeo(
        lat=hubs["Lat"],
        lon=hubs["Lon"],
        mode="markers+text",
        name="Strategic Hubs",
        text=hubs["Name"],
        textposition="top center",
        marker=dict(size=9, color="#FFA15A", symbol="diamond"),
        textfont=dict(size=10, color="white")
    ))

    if red_sea_crisis:
        fig_globe.add_trace(go.Scattergeo(
            lat=[12.60],
            lon=[43.33],
            mode="markers+text",
            name="⚠️ Chokepoint Alert",
            text=["⚠️ RED SEA CRISIS"],
            textposition="bottom right",
            marker=dict(size=13, color="#EF553B", symbol="x"),
            textfont=dict(size=10, color="#EF553B")
    ))

    fig_globe.update_geos(
        projection_type="orthographic",
        projection_rotation=dict(lon=62, lat=22, roll=0),
        showland=True,
        landcolor="rgb(32, 37, 46)",
        showocean=True,
        oceancolor="rgb(13, 17, 23)",
        showcountries=True,
        countrycolor="rgb(70, 78, 92)",
        showcoastlines=True,
        coastlinecolor="rgb(85, 95, 112)",
        showlakes=True,
        lakecolor="rgb(13, 17, 23)",
        bgcolor="rgba(0,0,0,0)"
    )
    fig_globe.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.05, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_globe, use_container_width=True)

with radar_col:
    st.subheader("🧭 Multi-Dimensional Strategy Radar")
    categories = ["Cost<br>Efficiency", "Delivery<br>Speed", "Geopolitical<br>Safety", "Low-Carbon<br>ESG"]
    fig_radar = go.Figure()

    for idx, row in df.iterrows():
        is_best = (idx == 0)
        r_vals = [
            round((1 - (row["True_Landed_Cost ($)"] / df["True_Landed_Cost ($)"].max())) * 100 + 20, 1),
            round((1 - (row["Transit_Days"] / df["Transit_Days"].max())) * 100 + 20, 1),
            round((1 - (row["Risk_Score"] / 10.0)) * 100, 1),
            round((1 - (row["CO2_Tons"] / df["CO2_Tons"].max())) * 100 + 20, 1),
        ]
        r_vals = [min(v, 100) for v in r_vals]

        fig_radar.add_trace(go.Scatterpolar(
            r=r_vals + [next(iter(r_vals))],
            theta=categories + [next(iter(categories))],
            fill="toself" if is_best else "none",
            name=row["Mode"],
            line=dict(width=3 if is_best else 1.5, color="#00CC96" if is_best else None)
        ))

    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(25, 29, 36, 0.6)",
            radialaxis=dict(visible=True, range=(0, 100), showticklabels=False, gridcolor="rgb(65, 72, 85)"),
            angularaxis=dict(gridcolor="rgb(65, 72, 85)", tickfont=dict(size=11))
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5),
        height=500,
        margin=dict(l=65, r=65, t=35, b=50),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# --- COST & TRADE-OFF CHARTS ---
c1, c2 = st.columns(2)
with c1:
    fig_cost = px.bar(
        df,
        x="Mode",
        y=["Total_Freight ($)", "Total_Tariff ($)", "Carbon_CBAM_Cost ($)", "Capital_Holding_Cost ($)"],
        title="Full Landed Cost Anatomy: Freight, Tariffs, Carbon & Working Capital",
        barmode="stack",
        text_auto=".2s"
    )
    st.plotly_chart(fig_cost, use_container_width=True)

with c2:
    fig_scatter = px.scatter(
        df,
        x="Transit_Days",
        y="True_Landed_Cost ($)",
        size="Optimization_Score",
        color="Mode",
        hover_name="Route",
        text="Mode",
        title="Pareto Frontier: Transit Speed vs. True Landed Cost"
    )
    fig_scatter.update_traces(textposition="top center")
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- DATA TABLE & CSV EXPORT ---
st.subheader("📊 Enterprise Multi-Criteria Decision Matrix")
display_cols = [
    "Route", "Mode", "Transit_Days", "Base_Tariff_Pct",
    "Total_Freight ($)", "Total_Tariff ($)", "Carbon_CBAM_Cost ($)",
    "Capital_Holding_Cost ($)", "True_Landed_Cost ($)", "CO2_Tons",
    "Risk_Score", "Optimization_Score"
]
st.dataframe(
    df[display_cols].style.format({
        "Base_Tariff_Pct": "{:.1f}%",
        "Total_Freight ($)": "${:,.0f}",
        "Total_Tariff ($)": "${:,.0f}",
        "Carbon_CBAM_Cost ($)": "${:,.0f}",
        "Capital_Holding_Cost ($)": "${:,.0f}",
        "True_Landed_Cost ($)": "${:,.0f}",
        "CO2_Tons": "{:,.1f}",
        "Risk_Score": "{:.1f}/10",
        "Optimization_Score": "{:.1f}"
    }),
    use_container_width=True
)

csv_data = df[display_cols].to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Full Boardroom Decision Report (CSV)",
    data=csv_data,
    file_name=f"GlobalRoute_v3_{origin_name}_to_{dest_name}_Report.csv",
    mime="text/csv"
)

# --- ACADEMIC & BELT-AND-ROAD (BRI) RESEARCH MODULE ---
st.markdown("---")
st.subheader("🎓 Academic Research & Belt-and-Road (BRI) Corridor Analysis")

tab_bri, tab_math = st.tabs([
    "🇨🇳 Belt & Road (BRI) CR Express & Break-Even Sensitivity",
    "📐 View Mathematical Formulation (MCDA Engine)"
])

with tab_bri:
    st.markdown("### China-Europe Railway Express (CR Express) Strategic Hedge Analysis")
    st.info(
        "**Research Context:** The China-Europe Railway Express (Chongqing → Almaty → Europe) serves as a "
        "vital overland stabilizer under the Belt & Road Initiative (BRI). When maritime chokepoints (Red Sea) "
        "or punitive direct-port tariffs disrupt ocean shipping, CR Express cuts transit time by **55–65%** vs. Cape-rerouted sea freight "
        "while emitting **~88% less CO₂** than direct air cargo."
    )

    # Dynamic Break-Even Curve across Tariff Hike Scenarios (0% to 50%)
    tariff_range = list(range(0, 55, 5))
    sim_records = []

    for t_sim in tariff_range:
        for _, r in df.iterrows():
            mode_name = r["Mode"]
            # Apply simulated tariff sensitivity matching the core engine
            if mode_name == "Sea + Air Hub":
                eff_tariff = 2.5
            elif mode_name == "China-Europe Rail":
                eff_tariff = 4.0 + (t_sim * 0.5)
            else:
                eff_tariff = 4.0 + t_sim

            sim_cost = (
                r["Total_Freight ($)"] +
                (total_cargo_value * (eff_tariff / 100.0)) +
                r["Carbon_CBAM_Cost ($)"] +
                r["Capital_Holding_Cost ($)"]
            )
            sim_records.append({
                "Tariff_Hike_Pct": t_sim,
                "Mode": mode_name,
                "Simulated_Landed_Cost ($)": sim_cost
            })

    sim_df = pd.DataFrame(sim_records)

    fig_breakeven = px.line(
        sim_df,
        x="Tariff_Hike_Pct",
        y="Simulated_Landed_Cost ($)",
        color="Mode",
        markers=True,
        title="Tariff Shock Break-Even Frontier: Where Overland Rail & Free-Zone Hubs Outperform Direct Sea",
        labels={
            "Tariff_Hike_Pct": "Direct-Route Tariff Hike (%)",
            "Simulated_Landed_Cost ($)": "True Landed Cost ($)"
        }
    )
    fig_breakeven.add_vline(
        x=tariff_hike,
        line_dash="dash",
        line_color="#00CC96",
        annotation_text=f"Current Tariff Setting ({tariff_hike}%)"
    )
    st.plotly_chart(fig_breakeven, use_container_width=True)

with tab_math:
    with st.expander("📐 Click to Expand Full Multi-Criteria Decision Analysis (MCDA) Equations", expanded=True):
        st.markdown("#### 1. True Landed Cost Function ($C_{\\text{total}}$)")
        st.latex(
            r"C_{\text{total}} = (F_{\text{unit}} \cdot Q) + \left(V_{\text{cargo}} \cdot \frac{\tau}{100}\right) + \left(\frac{E_{\text{unit}} \cdot Q}{1000} \cdot P_{\text{CBAM}}\right) + \left(V_{\text{cargo}} \cdot r_{\text{cap}} \cdot \frac{T}{365}\right)"
        )
        st.markdown(
            """
            * **$F_{\\text{unit}}$**: Base freight rate per unit ($) | **$Q$**: Shipment volume (units)
            * **$V_{\\text{cargo}}$**: Total cargo value ($Q \\times \\text{Unit Value}$) | **$\\tau$**: Effective customs tariff rate (%)
            * **$E_{\\text{unit}}$**: Scope 3 emissions per unit (kg CO₂) | **$P_{\\text{CBAM}}$**: EU Carbon Border Adjustment price ($/ton)
            * **$r_{\\text{cap}}$**: Annual cost of working capital (%) | **$T$**: Corridor lead time (days)
            """
        )

        st.markdown("#### 2. Dimensionless Max-Normalization & Weighted Penalty Index ($I_p$)")
        st.latex(
            r"I_p = \frac{w_c \left(\frac{C_{\text{total}}}{C_{\max}}\right) + w_t \left(\frac{T}{T_{\max}}\right) + w_r \left(\frac{R}{10}\right) + w_e \left(\frac{E_{\text{tons}}}{E_{\max}}\right)}{w_c + w_t + w_r + w_e}"
        )

        st.markdown("#### 3. Executive Optimization Score ($S_{\\text{opt}}$)")
        st.latex(
            r"S_{\text{opt}} = (1 - I_p) \times 100 \quad \in"
        )

