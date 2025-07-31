import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Modern Mercantilism: Decoding the New Global Order",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f4037, #99f2c8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">Modern Mercantilism: Decoding the New Global Order</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7f8c8d;">A Data-Driven Analysis of the Four-Cycle Machine Shaping Global Economics</p>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_forecast_data():
    forecasts = [
        {
            "id": 1,
            "statement": "US effective tariff rate on imports will average over 10% from 2026–2028",
            "probability": 70,
            "timeframe": "2026-2028",
            "resolution_criteria": "U.S. Treasury data; weighted average tariff",
            "cycle_link": "Internal Political / Geopolitical",
            "category": "Trade Policy"
        },
        {
            "id": 2,
            "statement": "China's industrial subsidies as a share of global subsidies will exceed 50% by 2027",
            "probability": 75,
            "timeframe": "2027",
            "resolution_criteria": "WTO/OECD global subsidy reporting",
            "cycle_link": "Geopolitical / Technology",
            "category": "Industrial Policy"
        },
        {
            "id": 3,
            "statement": "EU will impose new tariffs on green tech imports from the US and China by 2026",
            "probability": 68,
            "timeframe": "2026",
            "resolution_criteria": "EU Official Journal tariff schedule update",
            "cycle_link": "Geopolitical / Technology",
            "category": "Trade Policy"
        },
        {
            "id": 4,
            "statement": "Global average tariff rate will increase compared to 2024 levels by 2028",
            "probability": 80,
            "timeframe": "2028",
            "resolution_criteria": "WTO world tariff database",
            "cycle_link": "Geopolitical",
            "category": "Trade Policy"
        },
        {
            "id": 5,
            "statement": "US annual trade deficit will be lower (2026–2028 avg.) than the 2018–2024 avg.",
            "probability": 72,
            "timeframe": "2026-2028",
            "resolution_criteria": "Bureau of Economic Analysis trade balance",
            "cycle_link": "Internal Political",
            "category": "Trade Balance"
        },
        {
            "id": 6,
            "statement": "More than three G20 countries will mandate critical mineral stockpiles by 2028",
            "probability": 65,
            "timeframe": "2028",
            "resolution_criteria": "National critical minerals legislation",
            "cycle_link": "Geopolitical / Technology",
            "category": "Resource Security"
        },
        {
            "id": 7,
            "statement": "At least 80% of G20 nations will escalate subsidies in strategic sectors from 2025–2029",
            "probability": 85,
            "timeframe": "2025-2029",
            "resolution_criteria": "OECD, IMF annual fiscal reviews",
            "cycle_link": "Internal Political / Geopolitical",
            "category": "Industrial Policy"
        },
        {
            "id": 8,
            "statement": "US dollar share in international reserves will decline by at least 20% by 2028",
            "probability": 60,
            "timeframe": "2028",
            "resolution_criteria": "IMF COFER reports",
            "cycle_link": "Debt/Monetary",
            "category": "Monetary System"
        },
        {
            "id": 9,
            "statement": "US and allied tech export controls expand to include quantum and AI chips by 2027",
            "probability": 90,
            "timeframe": "2027",
            "resolution_criteria": "BIS/EU/China official policy docs",
            "cycle_link": "Technology / Geopolitical",
            "category": "Tech Controls"
        },
        {
            "id": 10,
            "statement": "WTO dispute over digital and AI trade rules by 2026",
            "probability": 70,
            "timeframe": "2026",
            "resolution_criteria": "WTO dispute settlement documentation",
            "cycle_link": "Geopolitical / Technology",
            "category": "Digital Trade"
        },
        {
            "id": 11,
            "statement": "G7 countries will institute formal stockpile mandates for rare earth minerals by 2028",
            "probability": 62,
            "timeframe": "2028",
            "resolution_criteria": "G7 official records",
            "cycle_link": "Geopolitical",
            "category": "Resource Security"
        },
        {
            "id": 12,
            "statement": "Public investment surge in renewables among the top 5 economies by 2027",
            "probability": 95,
            "timeframe": "2027",
            "resolution_criteria": "IEA, national investment reports",
            "cycle_link": "Technology / Nature",
            "category": "Green Investment"
        },
        {
            "id": 13,
            "statement": "India will raise tariffs on at least three strategic subsectors by 2026",
            "probability": 72,
            "timeframe": "2026",
            "resolution_criteria": "Indian Ministry of Commerce data",
            "cycle_link": "Internal Political / Geopolitical",
            "category": "Trade Policy"
        },
        {
            "id": 14,
            "statement": "BRICS+ bloc pilots a dollar-alternative digital trade settlement system by 2029",
            "probability": 90,
            "timeframe": "2029",
            "resolution_criteria": "BRICS, IMF, central bank announcements",
            "cycle_link": "Debt/Monetary / Geopolitical",
            "category": "Monetary System"
        },
        {
            "id": 15,
            "statement": "US will formally restrict outbound investment in key tech sectors by 2026",
            "probability": 75,
            "timeframe": "2026",
            "resolution_criteria": "U.S. Treasury/Commerce rulings",
            "cycle_link": "Internal Political / Technology",
            "category": "Investment Controls"
        },
        {
            "id": 16,
            "statement": "At least five SSA countries declare digital payments as sovereign backing for currency by 2032",
            "probability": 62,
            "timeframe": "2032",
            "resolution_criteria": "National policy documents, IMF reports",
            "cycle_link": "Debt/Monetary / Technology",
            "category": "SSA Digital Currency"
        },
        {
            "id": 17,
            "statement": "EU will expand carbon border taxes to at least two new categories by 2029",
            "probability": 65,
            "timeframe": "2029",
            "resolution_criteria": "EU Commission regulations",
            "cycle_link": "Geopolitical / Nature",
            "category": "Climate Policy"
        },
        {
            "id": 18,
            "statement": "Chinese export controls on strategic minerals will persist through 2028",
            "probability": 75,
            "timeframe": "2028",
            "resolution_criteria": "China Ministry of Commerce",
            "cycle_link": "Geopolitical / Technology",
            "category": "Resource Controls"
        },
        {
            "id": 19,
            "statement": "SSA's share of global strategic mineral exports exceeds 10% by 2028",
            "probability": 72,
            "timeframe": "2028",
            "resolution_criteria": "UN Comtrade, ITC statistics",
            "cycle_link": "Geopolitical",
            "category": "SSA Resource Power"
        },
        {
            "id": 20,
            "statement": "Western firms will lose at least 30% market share in SSA digital payments by 2029",
            "probability": 70,
            "timeframe": "2029",
            "resolution_criteria": "Central Bank/country market reports",
            "cycle_link": "Geopolitical / Technology",
            "category": "SSA Digital Markets"
        }
    ]
    return pd.DataFrame(forecasts)

@st.cache_data
def load_trade_data():
    trade_data = [
        {"year": 2001, "China": 10, "US": 40, "EU": 80},
        {"year": 2005, "China": 25, "US": 45, "EU": 75},
        {"year": 2010, "China": 90, "US": 50, "EU": 60},
        {"year": 2015, "China": 180, "US": 35, "EU": 62},
        {"year": 2020, "China": 245, "US": 30, "EU": 60},
        {"year": 2024, "China": 255, "US": 32, "EU": 68}
    ]
    return pd.DataFrame(trade_data)

@st.cache_data
def load_power_index_data():
    power_data = []
    countries = ["USA", "China", "Nigeria", "EU"]
    years = [2000, 2010, 2020, 2024]
    scores = {
        "USA": [0.95, 0.90, 0.85, 0.82],
        "China": [0.25, 0.45, 0.75, 0.78],
        "Nigeria": [0.51, 0.507, 0.495, 0.495],
        "EU": [0.70, 0.68, 0.65, 0.63]
    }
    
    for country in countries:
        for i, year in enumerate(years):
            power_data.append({"Country": country, "Year": year, "Power_Index": scores[country][i]})
    
    return pd.DataFrame(power_data)

# Load all data
df_forecasts = load_forecast_data()
df_trade = load_trade_data()
df_power = load_power_index_data()

# Sidebar
st.sidebar.markdown("## 🎛️ Dashboard Controls")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.selectbox(
    "Navigate to:",
    ["📊 Executive Dashboard", "🔮 Forecast Analysis", "📈 Trade Dynamics", "⚡ Power Index Trends", "🌍 SSA Focus", "🔄 Causal Loops"]
)

if page == "📊 Executive Dashboard":
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>20</h3>
            <p>Strategic Forecasts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_prob = df_forecasts['probability'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{avg_prob:.1f}%</h3>
            <p>Average Probability</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        high_conf = len(df_forecasts[df_forecasts['probability'] >= 80])
        st.markdown(f"""
        <div class="metric-card">
            <h3>{high_conf}</h3>
            <p>High Confidence (≥80%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        ssa_forecasts = len(df_forecasts[df_forecasts['category'].str.contains('SSA')])
        st.markdown(f"""
        <div class="metric-card">
            <h3>{ssa_forecasts}</h3>
            <p>SSA-Focused</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Main dashboard content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="sub-header">📈 China's Rise in SSA Trade</h2>', unsafe_allow_html=True)
        
        fig_trade = go.Figure()
        fig_trade.add_trace(go.Scatter(x=df_trade['year'], y=df_trade['China'], 
                                     mode='lines+markers', name='China', 
                                     line=dict(color='#e74c3c', width=4)))
        fig_trade.add_trace(go.Scatter(x=df_trade['year'], y=df_trade['US'], 
                                     mode='lines+markers', name='US', 
                                     line=dict(color='#3498db', width=4)))
        fig_trade.add_trace(go.Scatter(x=df_trade['year'], y=df_trade['EU'], 
                                     mode='lines+markers', name='EU', 
                                     line=dict(color='#f39c12', width=4)))
        
        fig_trade.update_layout(
            title="SSA Trade Volume by Major Power (Billions USD)",
            xaxis_title="Year",
            yaxis_title="Trade Volume (Billions USD)",
            template="plotly_white",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_trade, use_container_width=True)
    
    with col2:
        st.markdown('<h2 class="sub-header">🎯 Forecast Categories</h2>', unsafe_allow_html=True)
        
        category_counts = df_forecasts['category'].value_counts()
        
        fig_pie = px.pie(values=category_counts.values, names=category_counts.index, 
                        color_discrete_sequence=px.colors.qualitative.Set3)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Four Cycles explanation
    st.markdown("---")
    st.markdown('<h2 class="sub-header">🔄 The Four-Cycle Machine of Modern Mercantilism</h2>', unsafe_allow_html=True)
    
    cycle_cols = st.columns(4)
    
    cycles = [
        ("💰 Debt/Monetary", "States weaponize payment systems, debt-diplomacy, and digital currency races"),
        ("🏛️ Internal Political", "Tariffs and subsidies serve domestic stabilization and regime legitimacy"),
        ("🌍 Geopolitical/Bloc", "Globalization becomes contest between economic blocs (G7, BRICS+)"),
        ("🔬 Technology & Nature", "Tech and climate become primary arenas for state-backed competition")
    ]
    
    for i, (title, desc) in enumerate(cycles):
        with cycle_cols[i]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #74b9ff, #0984e3); padding: 1rem; border-radius: 10px; color: white; height: 150px;">
                <h4>{title}</h4>
                <p style="font-size: 0.9rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "🔮 Forecast Analysis":
    st.markdown('<h2 class="sub-header">🔮 Strategic Forecasts Analysis</h2>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_categories = st.multiselect("Filter by Category:", 
                                           df_forecasts['category'].unique(), 
                                           default=df_forecasts['category'].unique())
    with col2:
        min_prob = st.slider("Minimum Probability:", 0, 100, 0)
    with col3:
        selected_cycles = st.multiselect("Filter by Cycle:", 
                                       df_forecasts['cycle_link'].unique(),
                                       default=df_forecasts['cycle_link'].unique())
    
    # Filter data
    filtered_df = df_forecasts[
        (df_forecasts['category'].isin(selected_categories)) &
        (df_forecasts['probability'] >= min_prob) &
        (df_forecasts['cycle_link'].isin(selected_cycles))
    ]
    
    # Probability distribution
    fig_hist = px.histogram(filtered_df, x='probability', nbins=10,
                           title="Distribution of Forecast Probabilities",
                           color_discrete_sequence=['#e17055'])
    fig_hist.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Detailed forecast table
    st.markdown("### 📋 Detailed Forecasts")
    
    # Create a more readable dataframe for display
    display_df = filtered_df[['id', 'statement', 'probability', 'timeframe', 'category', 'cycle_link']].copy()
    display_df['probability'] = display_df['probability'].apply(lambda x: f"{x}%")
    
    st.dataframe(
        display_df,
        column_config={
            "id": "ID",
            "statement": st.column_config.TextColumn("Forecast Statement", width="large"),
            "probability": "Probability",
            "timeframe": "Timeframe",
            "category": "Category",
            "cycle_link": "Dalio Cycle"
        },
        hide_index=True,
        use_container_width=True
    )

elif page == "📈 Trade Dynamics":
    st.markdown('<h2 class="sub-header">📈 SSA Trade Dynamics: The New Great Game</h2>', unsafe_allow_html=True)
    
    # Trade evolution chart
    fig_trade_detailed = go.Figure()
    
    colors = {'China': '#e74c3c', 'US': '#3498db', 'EU': '#f39c12'}
    
    for country in ['China', 'US', 'EU']:
        fig_trade_detailed.add_trace(go.Scatter(
            x=df_trade['year'], 
            y=df_trade[country],
            mode='lines+markers+text',
            name=country,
            line=dict(color=colors[country], width=4),
            marker=dict(size=8),
            text=df_trade[country],
            textposition="top center",
            textfont=dict(size=12, color=colors[country])
        ))
    
    fig_trade_detailed.update_layout(
        title="SSA Trade Evolution: The Rise of China (2001-2024)",
        xaxis_title="Year",
        yaxis_title="Trade Volume (Billions USD)",
        template="plotly_white",
        height=500,
        showlegend=True,
        annotations=[
            dict(x=2010, y=90, text="China's BRI Launch", showarrow=True, arrowhead=2),
            dict(x=2020, y=245, text="COVID-19 Impact", showarrow=True, arrowhead=2)
        ]
    )
    st.plotly_chart(fig_trade_detailed, use_container_width=True)
    
    # Trade share analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Calculate trade shares for 2024
        total_2024 = df_trade.iloc[-1]['China'] + df_trade.iloc[-1]['US'] + df_trade.iloc[-1]['EU']
        shares_2024 = {
            'China': (df_trade.iloc[-1]['China'] / total_2024) * 100,
            'US': (df_trade.iloc[-1]['US'] / total_2024) * 100,
            'EU': (df_trade.iloc[-1]['EU'] / total_2024) * 100
        }
        
        fig_share = px.pie(values=list(shares_2024.values()), names=list(shares_2024.keys()),
                          title="2024 SSA Trade Share",
                          color_discrete_map=colors)
        fig_share.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_share, use_container_width=True)
    
    with col2:
        # Growth rates
        china_growth = ((df_trade.iloc[-1]['China'] - df_trade.iloc[0]['China']) / df_trade.iloc[0]['China']) * 100
        us_growth = ((df_trade.iloc[-1]['US'] - df_trade.iloc[0]['US']) / df_trade.iloc[0]['US']) * 100
        eu_growth = ((df_trade.iloc[-1]['EU'] - df_trade.iloc[0]['EU']) / df_trade.iloc[0]['EU']) * 100
        
        growth_data = pd.DataFrame({
            'Country': ['China', 'US', 'EU'],
            'Growth_Rate': [china_growth, us_growth, eu_growth]
        })
        
        fig_growth = px.bar(growth_data, x='Country', y='Growth_Rate',
                           title="Trade Growth Rate (2001-2024)",
                           color='Country', color_discrete_map=colors)
        fig_growth.update_layout(showlegend=False)
        st.plotly_chart(fig_growth, use_container_width=True)
    
    # Key insights
    st.markdown("### 🔍 Key Trade Insights")
    insights_col1, insights_col2, insights_col3 = st.columns(3)
    
    with insights_col1:
        st.info(f"**China's Meteoric Rise**: {china_growth:.0f}% growth since 2001, now dominant player")
    
    with insights_col2:
        st.warning(f"**US Decline**: {abs(us_growth):.0f}% decrease, losing ground to China")
    
    with insights_col3:
        st.success(f"**EU Stability**: {eu_growth:.0f}% growth, maintaining steady presence")

elif page == "⚡ Power Index Trends":
    st.markdown('<h2 class="sub-header">⚡ Dalio Power Index: The Great Transition</h2>', unsafe_allow_html=True)
    
    # Power index over time
    fig_power = px.line(df_power, x='Year', y='Power_Index', color='Country',
                       title="Dalio Power Index Trends (2000-2024)",
                       markers=True, line_shape='spline')
    
    color_map = {'USA': '#3498db', 'China': '#e74c3c', 'Nigeria': '#2ecc71', 'EU': '#f39c12'}
    for i, country in enumerate(['USA', 'China', 'Nigeria', 'EU']):
        fig_power.data[i].line.color = color_map[country]
        fig_power.data[i].line.width = 4
    
    fig_power.update_layout(
        template="plotly_white",
        height=500,
        annotations=[
            dict(x=2008, y=0.5, text="Financial Crisis", showarrow=True),
            dict(x=2020, y=0.7, text="COVID-19 & Trade Wars", showarrow=True)
        ]
    )
    st.plotly_chart(fig_power, use_container_width=True)
    
    # Power index comparison
    col1, col2 = st.columns(2)
    
    with col1:
        # 2000 vs 2024 comparison
        power_2000 = df_power[df_power['Year'] == 2000].set_index('Country')['Power_Index']
        power_2024 = df_power[df_power['Year'] == 2024].set_index('Country')['Power_Index']
        
        comparison_df = pd.DataFrame({
            '2000': power_2000,
            '2024': power_2024,
            'Change': power_2024 - power_2000
        }).reset_index()
        
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Bar(name='2000', x=comparison_df['Country'], y=comparison_df['2000'],
                                      marker_color='lightblue'))
        fig_comparison.add_trace(go.Bar(name='2024', x=comparison_df['Country'], y=comparison_df['2024'],
                                      marker_color='darkblue'))
        
        fig_comparison.update_layout(title="Power Index: 2000 vs 2024", barmode='group')
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    with col2:
        # Change analysis
        fig_change = px.bar(comparison_df, x='Country', y='Change',
                           title="Power Index Change (2000-2024)",
                           color='Change', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_change, use_container_width=True)
    
    # Power index breakdown (simulated data for visualization)
    st.markdown("### 📊 Power Index Components (2024)")
    
    components = ['Education', 'Innovation', 'Competitiveness', 'Military', 'Trade Share', 'Reserve Currency', 'Financial Center']
    
    # Simulated component scores
    component_scores = {
        'USA': [0.85, 0.95, 0.80, 0.95, 0.70, 0.90, 0.95],
        'China': [0.75, 0.85, 0.90, 0.80, 0.85, 0.20, 0.60],
        'EU': [0.80, 0.75, 0.75, 0.60, 0.70, 0.30, 0.80],
        'Nigeria': [0.40, 0.35, 0.45, 0.40, 0.30, 0.10, 0.25]
    }
    
    fig_radar = go.Figure()
    
    for country in component_scores.keys():
        fig_radar.add_trace(go.Scatterpolar(
            r=component_scores[country],
            theta=components,
            fill='toself',
            name=country,
            line_color=color_map[country]
        ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        title="Power Index Components Breakdown (2024)"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

elif page == "🌍 SSA Focus":
    st.markdown('<h2 class="sub-header">🌍 Sub-Saharan Africa: The New Battleground</h2>', unsafe_allow_html=True)
    
    # SSA-specific forecasts
    ssa_forecasts = df_forecasts[df_forecasts['category'].str.contains('SSA')]
    
    if not ssa_forecasts.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_ssa = px.bar(ssa_forecasts, x='probability', y='statement',
                           orientation='h', title="SSA-Focused Forecasts",
                           color='probability', color_continuous_scale='viridis')
            fig_ssa.update_layout(height=400)
            st.plotly_chart(fig_ssa, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 SSA Strategic Importance")
            st.markdown("""
            - **Resource Wealth**: Critical minerals for energy transition
            - **Demographic Dividend**: Young, growing population
            - **Market Potential**: Emerging consumer class
            - **Strategic Location**: Gateway to global trade routes
            """)
    
    # SSA trade patterns
    st.markdown("### 📈 SSA Trade Evolution")
    
    # Create projected data for SSA
    projection_years = [2025, 2026, 2027, 2028, 2029, 2030]
    china_projected = [260, 265, 270, 280, 290, 300]
    us_projected = [35, 37, 38, 40, 42, 45]
    eu_projected = [70, 72, 74, 76, 78, 80]
    
    # Combine historical and projected
    extended_years = list(df_trade['year']) + projection_years
    extended_china = list(df_trade['China']) + china_projected
    extended_us = list(df_trade['US']) + us_projected
    extended_eu = list(df_trade['EU']) + eu_projected
    
    fig_projection = go.Figure()
    
    # Historical data (solid lines)
    fig_projection.add_trace(go.Scatter(x=df_trade['year'], y=df_trade['China'],
                                      mode='lines+markers', name='China (Historical)',
                                      line=dict(color='#e74c3c', width=4)))
    fig_projection.add_trace(go.Scatter(x=df_trade['year'], y=df_trade['US'],
                                      mode='lines+markers', name='US (Historical)',
                                      line=dict(color='#3498db', width=4)))
    fig_projection.add_trace(go.Scatter(x=df_trade['year'], y=df_trade['EU'],
                                      mode='lines+markers', name='EU (Historical)',
                                      line=dict(color='#f39c12', width=4)))
    
    # Projected data (dashed lines)
    fig_projection.add_trace(go.Scatter(x=projection_years, y=china_projected,
                                      mode='lines+markers', name='China (Projected)',
                                      line=dict(color='#e74c3c', width=3, dash='dash')))
    fig_projection.add_trace(go.Scatter(x=projection_years, y=us_projected,
                                      mode='lines+markers', name='US (Projected)',
                                      line=dict(color='#3498db', width=3, dash='dash')))
    fig_projection.add_trace(go.Scatter(x=projection_years, y=eu_projected,
                                      mode='lines+markers', name='EU (Projected)',
                                      line=dict(color='#f39c12', width=3, dash='dash')))
    
    fig_projection.update_layout(
        title="SSA Trade: Historical Trends and Projections",
        xaxis_title="Year",
        yaxis_title="Trade Volume (Billions USD)",
        template="plotly_white",
        height=500
    )
    st.plotly_chart(fig_projection, use_container_width=True)
    
    # SSA debt analysis
    st.markdown("### 💰 SSA Debt Dynamics")
    
    debt_data = pd.DataFrame({
        'Year': [2015, 2018, 2020, 2022, 2024],
        'China_Debt_Share': [15, 25, 36, 38, 40],
        'Total_Debt_GDP': [45, 52, 65, 70, 72]
    })
    
    fig_debt = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_debt.add_trace(
        go.Bar(x=debt_data['Year'], y=debt_data['China_Debt_Share'], name="China Debt Share (%)"),
        secondary_y=False
    )
    
    fig_debt.add_trace(
        go.Scatter(x=debt_data['Year'], y=debt_data['Total_Debt_GDP'], 
                  mode='lines+markers', name="Total Debt/GDP (%)", line=dict(color='red', width=3)),
        secondary_y=True
    )
    
    fig_debt.update_xaxes(title_text="Year")
    fig_debt.update_yaxes(title_text="China Debt Share (%)", secondary_y=False)
    fig_debt.update_yaxes(title_text="Total Debt/GDP (%)", secondary_y=True)
    fig_debt.update_layout(title="SSA Debt Dynamics: China's Growing Influence")
    
    st.plotly_chart(fig_debt, use_container_width=True)

elif page == "🔄 Causal Loops":
    st.markdown('<h2 class="sub-header">🔄 Causal Loop Analysis: The Machinery of Modern Mercantilism</h2>', unsafe_allow_html=True)
    
    # Interactive causal loop selection
    loop_type = st.selectbox("Select Causal Loop to Analyze:",
                           ["China's BRI Loop", "US Decline Loop", "SSA Development Loop", "Global Tariff Spiral"])
    
    if loop_type == "China's BRI Loop":
        st.markdown("### 🇨🇳 China's Belt & Road Infrastructure Loop")
        
        # Create a network-style visualization
        loop_data = {
            'Variable': ['Infrastructure Investment', 'Resource Exports', 'Chinese Imports', 
                        'Local Production Displacement', 'Debt Accumulation', 'Policy Leverage'],
            'Effect_Size': [0.8, 0.9, 0.7, -0.6, 0.85, 0.75],
            'Loop_Position': [1, 2, 3, 4, 5, 6]
        }
        
        fig_loop = px.scatter(pd.DataFrame(loop_data), x='Loop_Position', y='Effect_Size',
                            size=[abs(x)*20 for x in loop_data['Effect_Size']],
                            color='Effect_Size', color_continuous_scale='RdYlGn',
                            hover_name='Variable',
                            title="China's BRI Causal Loop - Variable Interactions")
        
        fig_loop.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, title="Loop Flow"),
            yaxis=dict(title="Effect Strength"),
            height=400
        )
        st.plotly_chart(fig_loop, use_container_width=True)
        
        st.markdown("""
        **Loop Dynamics:**
        1. 🏗️ **Infrastructure Investment** → Increases resource export capacity
        2. 📦 **Resource Exports** → Generate revenue for Chinese goods imports  
        3. 🛒 **Chinese Imports** → Displace local production
        4. 📉 **Production Displacement** → Increases economic dependency
        5. 💸 **Debt Accumulation** → Enhances Chinese policy leverage
        6. 🎯 **Policy Leverage** → Enables more infrastructure investment
        
        *This creates a **reinforcing loop** that can lead to debt-trap dynamics.*
        """)
    
    elif loop_type == "Global Tariff Spiral":
        st.markdown("### 🌪️ Global Tariff Escalation Loop")
        
        tariff_data = {
            'Year': list(range(2018, 2030)),
            'US_Tariffs': [7.4, 8.2, 9.1, 10.5, 11.2, 12.8, 13.5, 14.2, 15.0, 15.8, 16.5, 17.2],
            'Retaliatory_Tariffs': [5.2, 6.1, 7.3, 8.9, 9.7, 10.8, 11.5, 12.3, 13.1, 13.9, 14.7, 15.5],
            'Global_Average': [6.8, 7.2, 7.8, 8.5, 9.2, 10.1, 10.8, 11.5, 12.2, 12.9, 13.6, 14.3]
        }
        
        fig_spiral = go.Figure()
        
        colors_spiral = {'US_Tariffs': '#e74c3c', 'Retaliatory_Tariffs': '#3498db', 'Global_Average': '#2ecc71'}
        
        for key in ['US_Tariffs', 'Retaliatory_Tariffs', 'Global_Average']:
            fig_spiral.add_trace(go.Scatter(
                x=tariff_data['Year'], y=tariff_data[key],
                mode='lines+markers', name=key.replace('_', ' '),
                line=dict(color=colors_spiral[key], width=3)
            ))
        
        fig_spiral.update_layout(
            title="Global Tariff Escalation Spiral (2018-2029)",
            xaxis_title="Year",
            yaxis_title="Average Tariff Rate (%)",
            template="plotly_white",
            height=500
        )
        st.plotly_chart(fig_spiral, use_container_width=True)
    
    # Feedback loop strength analysis
    st.markdown("### 📊 Feedback Loop Strength Analysis")
    
    loop_strength = pd.DataFrame({
        'Loop_Type': ['BRI Infrastructure', 'Tariff Retaliation', 'Tech Export Controls', 'Digital Currency Race'],
        'Reinforcing_Strength': [0.85, 0.75, 0.90, 0.70],
        'Balancing_Forces': [0.30, 0.45, 0.25, 0.55],
        'Net_Effect': [0.55, 0.30, 0.65, 0.15]
    })
    
    fig_strength = px.bar(loop_strength, x='Loop_Type', y=['Reinforcing_Strength', 'Balancing_Forces'],
                         title="Causal Loop Strength Analysis",
                         barmode='group', color_discrete_sequence=['#e74c3c', '#27ae60'])
    st.plotly_chart(fig_strength, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 2rem;">
    <p><strong>Modern Mercantilism Dashboard</strong> | Built with Streamlit & Plotly</p>
    <p>Data sources: World Bank, IMF, WTO, OECD, and proprietary analysis</p>
</div>
""", unsafe_allow_html=True)