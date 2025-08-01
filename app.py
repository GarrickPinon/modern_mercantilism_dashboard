import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import math

# Page configuration
st.set_page_config(
    page_title="Modern Mercantilism: Decoding the New Global Order",
    page_icon="📈", # Changed Icon
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- THEME AND STYLING ---
# Define the primary color palette
COMPANY_COLORS = {
    "red_primary": "#B80000",
    "red_accent": "#FF4136",
    "black_bg": "#0E0E0E",
    "dark_grey_bg": "#1C1C1C",
    "medium_grey": "#444444",
    "light_grey": "#AAAAAA",
    "light_grey_text": "#DDDDDD"
}

# Custom CSS for the black and red theme
st.markdown(f"""
<style>
    /* Main app background */
    .stApp {{
        background-color: {COMPANY_COLORS['black_bg']};
        color: {COMPANY_COLORS['light_grey_text']};
    }}

    /* Main header styling */
    .main-header {{
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, {COMPANY_COLORS['red_primary']}, {COMPANY_COLORS['medium_grey']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }}
    
    /* Sub-header styling */
    .sub-header {{
        font-size: 1.75rem;
        color: {COMPANY_COLORS['red_primary']};
        margin-bottom: 1rem;
        padding-bottom: 10px;
        border-bottom: 2px solid {COMPANY_COLORS['medium_grey']};
    }}

    /* Metric card styling */
    .metric-card {{
        background-color: {COMPANY_COLORS['dark_grey_bg']};
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        border: 1px solid {COMPANY_COLORS['medium_grey']};
        border-top: 4px solid {COMPANY_COLORS['red_primary']};
    }}
    .metric-card h3 {{
        color: {COMPANY_COLORS['red_accent']};
        font-size: 2.5rem;
    }}

    /* Custom card for cycle descriptions */
    .cycle-card {{
        background-color: {COMPANY_COLORS['dark_grey_bg']};
        padding: 1rem;
        border-radius: 10px;
        color: white;
        height: 180px;
        border: 1px solid {COMPANY_COLORS['medium_grey']};
    }}
    .cycle-card h4 {{
        color: {COMPANY_COLORS['red_primary']};
    }}

    /* Stationary Tab Navigation Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 5px;
        background-color: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background-color: {COMPANY_COLORS['dark_grey_bg']};
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        color: {COMPANY_COLORS['light_grey_text']};
        border-bottom: 3px solid {COMPANY_COLORS['medium_grey']};
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {COMPANY_COLORS['dark_grey_bg']};
        color: white;
        font-weight: bold;
        border-bottom: 3px solid {COMPANY_COLORS['red_primary']};
    }}
</style>
""", unsafe_allow_html=True)


# --- DATA LOADING ---
@st.cache_data
def load_forecast_data():
    # Data remains the same
    forecasts = [
        {"id": 1, "statement": "US effective tariff rate on imports will average over 15% from 2026–2028", "probability": 82, "timeframe": "2026-2028", "resolution_criteria": "U.S. Treasury data; weighted average tariff", "cycle_link": "Internal Political / Geopolitical", "category": "Trade Policy"},
        {"id": 2, "statement": "China's industrial subsidies as a share of global subsidies will exceed 50% by 2027", "probability": 75, "timeframe": "2027", "resolution_criteria": "WTO/OECD global subsidy reporting", "cycle_link": "Geopolitical / Technology", "category": "Industrial Policy"},
        {"id": 3, "statement": "EU will impose new tariffs on green tech imports from the US and China by 2026", "probability": 68, "timeframe": "2026", "resolution_criteria": "EU Official Journal tariff schedule update", "cycle_link": "Geopolitical / Technology", "category": "Trade Policy"},
        {"id": 4, "statement": "Global average tariff rate will increase compared to 2024 levels by 2028", "probability": 80, "timeframe": "2028", "resolution_criteria": "WTO world tariff database", "cycle_link": "Geopolitical", "category": "Trade Policy"},
        {"id": 5, "statement": "US annual trade deficit will be lower (2026–2028 avg.) than the 2018–2024 avg.", "probability": 72, "timeframe": "2026-2028", "resolution_criteria": "Bureau of Economic Analysis trade balance", "cycle_link": "Internal Political", "category": "Trade Balance"},
        {"id": 6, "statement": "More than three G20 countries will mandate critical mineral stockpiles by 2028", "probability": 65, "timeframe": "2028", "resolution_criteria": "National critical minerals legislation", "cycle_link": "Geopolitical / Technology", "category": "Resource Security"},
        {"id": 7, "statement": "At least 80% of G20 nations will escalate subsidies in strategic sectors from 2025–2029", "probability": 85, "timeframe": "2025-2029", "resolution_criteria": "OECD, IMF annual fiscal reviews", "cycle_link": "Internal Political / Geopolitical", "category": "Industrial Policy"},
        {"id": 8, "statement": "US dollar share in international reserves will decline by at least 20% by 2028", "probability": 60, "timeframe": "2028", "resolution_criteria": "IMF COFER reports", "cycle_link": "Debt/Monetary", "category": "Monetary System"},
        {"id": 9, "statement": "US and allied tech export controls expand to include quantum and AI chips by 2027", "probability": 90, "timeframe": "2027", "resolution_criteria": "BIS/EU/China official policy docs", "cycle_link": "Technology / Geopolitical", "category": "Tech Controls"},
        {"id": 10, "statement": "WTO dispute over digital and AI trade rules by 2026", "probability": 70, "timeframe": "2026", "resolution_criteria": "WTO dispute settlement documentation", "cycle_link": "Geopolitical / Technology", "category": "Digital Trade"},
        {"id": 11, "statement": "G7 countries will institute formal stockpile mandates for rare earth minerals by 2028", "probability": 62, "timeframe": "2028", "resolution_criteria": "G7 official records", "cycle_link": "Geopolitical", "category": "Resource Security"},
        {"id": 12, "statement": "Public investment surge in renewables among the top 5 economies by 2027", "probability": 95, "timeframe": "2027", "resolution_criteria": "IEA, national investment reports", "cycle_link": "Technology / Nature", "category": "Green Investment"},
        {"id": 13, "statement": "India will raise tariffs on at least three strategic subsectors by 2026", "probability": 72, "timeframe": "2026", "resolution_criteria": "Indian Ministry of Commerce data", "cycle_link": "Internal Political / Geopolitical", "category": "Trade Policy"},
        {"id": 14, "statement": "BRICS+ bloc pilots a dollar-alternative digital trade settlement system by 2029", "probability": 90, "timeframe": "2029", "resolution_criteria": "BRICS, IMF, central bank announcements", "cycle_link": "Debt/Monetary / Geopolitical", "category": "Monetary System"},
        {"id": 15, "statement": "US will formally restrict outbound investment in key tech sectors by 2026", "probability": 75, "timeframe": "2026", "resolution_criteria": "U.S. Treasury/Commerce rulings", "cycle_link": "Internal Political / Technology", "category": "Investment Controls"},
        {"id": 16, "statement": "At least five SSA countries declare digital payments as sovereign backing for currency by 2032", "probability": 62, "timeframe": "2032", "resolution_criteria": "National policy documents, IMF reports", "cycle_link": "Debt/Monetary / Technology", "category": "SSA Digital Currency"},
        {"id": 17, "statement": "EU will expand carbon border taxes to at least two new categories by 2029", "probability": 65, "timeframe": "2029", "resolution_criteria": "EU Commission regulations", "cycle_link": "Geopolitical / Nature", "category": "Climate Policy"},
        {"id": 18, "statement": "Chinese export controls on strategic minerals will persist through 2028", "probability": 75, "timeframe": "2028", "resolution_criteria": "China Ministry of Commerce", "cycle_link": "Geopolitical / Technology", "category": "Resource Controls"},
        {"id": 19, "statement": "SSA's share of global strategic mineral exports exceeds 10% by 2028", "probability": 72, "timeframe": "2028", "resolution_criteria": "UN Comtrade, ITC statistics", "cycle_link": "Geopolitical", "category": "SSA Resource Power"},
        {"id": 20, "statement": "Western firms will lose at least 30% market share in SSA digital payments by 2029", "probability": 70, "timeframe": "2029", "resolution_criteria": "Central Bank/country market reports", "cycle_link": "Geopolitical / Technology", "category": "SSA Digital Markets"}
    ]
    return pd.DataFrame(forecasts)

@st.cache_data
def load_trade_data():
    trade_data = [
        {"year": 2001, "China": 10, "US": 40, "EU": 80}, {"year": 2005, "China": 25, "US": 45, "EU": 75},
        {"year": 2010, "China": 90, "US": 50, "EU": 60}, {"year": 2015, "China": 180, "US": 35, "EU": 62},
        {"year": 2020, "China": 245, "US": 30, "EU": 60}, {"year": 2024, "China": 255, "US": 32, "EU": 68}
    ]
    df = pd.DataFrame(trade_data)
    
    # --- NEW: Forecasting Logic ---
    forecast_years = list(range(2025, 2035))
    forecast_data = []
    
    # Calculate historical CAGR (Compound Annual Growth Rate)
    start_year = df['year'].min()
    end_year = df['year'].max()
    num_years = end_year - start_year
    
    cagr_china = (df[df['year'] == end_year]['China'].iloc[0] / df[df['year'] == start_year]['China'].iloc[0])**(1/num_years) - 1
    cagr_us = (df[df['year'] == end_year]['US'].iloc[0] / df[df['year'] == start_year]['US'].iloc[0])**(1/num_years) - 1
    cagr_eu = (df[df['year'] == end_year]['EU'].iloc[0] / df[df['year'] == start_year]['EU'].iloc[0])**(1/num_years) - 1

    # Adjust CAGR based on qualitative forecasts (protectionism vs. strategic investment)
    # China's BRI and strategic focus suggest continued strong growth.
    # US/EU tariffs and friendshoring suggest slower, more deliberate growth.
    forecast_cagr = {'China': cagr_china * 1.05, 'US': cagr_us * 0.8, 'EU': cagr_eu * 0.9}

    last_values = df[df['year'] == end_year].iloc[0]
    
    for year in forecast_years:
        new_row = {'year': year}
        for country in ['China', 'US', 'EU']:
            last_value = last_values[country]
            new_row[country] = last_value * (1 + forecast_cagr[country])
            last_values[country] = new_row[country]
        forecast_data.append(new_row)
        
    df_forecast = pd.DataFrame(forecast_data)
    return pd.concat([df, df_forecast]).reset_index(drop=True)

@st.cache_data
def load_power_index_data():
    power_data, countries = [], ["USA", "China", "Nigeria", "EU"]
    years = [2000, 2010, 2020, 2024]
    scores = {"USA": [0.95, 0.90, 0.85, 0.82], "China": [0.25, 0.45, 0.75, 0.78],
              "Nigeria": [0.51, 0.507, 0.495, 0.495], "EU": [0.70, 0.68, 0.65, 0.63]}
    
    df_list = []
    for country in countries:
        for i, year in enumerate(years):
            df_list.append({"Country": country, "Year": year, "Power_Index": scores[country][i]})
    df = pd.DataFrame(df_list)

    # --- NEW: Forecasting Logic ---
    forecast_years = list(range(2025, 2035))
    
    # Calculate annualized rate of change from the last period (2020-2024)
    last_period = df[df['Year'].isin([2020, 2024])]
    annual_changes = {}
    for country in countries:
        start_val = last_period[(last_period['Country'] == country) & (last_period['Year'] == 2020)]['Power_Index'].iloc[0]
        end_val = last_period[(last_period['Country'] == country) & (last_period['Year'] == 2024)]['Power_Index'].iloc[0]
        annual_changes[country] = (end_val - start_val) / 4

    # Adjust rates based on qualitative forecasts (dollar decline, BRICS+, SSA mineral power)
    annual_changes['USA'] *= 1.5  # Accelerate decline based on monetary forecasts
    annual_changes['China'] *= 1.1 # Maintain strong growth
    annual_changes['Nigeria'] += 0.001 # Slight increase based on resource power forecasts
    
    forecast_data = []
    last_values = df[df['Year'] == 2024].set_index('Country')['Power_Index']
    
    for year in forecast_years:
        for country in countries:
            new_val = last_values[country] + annual_changes[country]
            # Add caps to prevent scores from going above 1 or below 0
            new_val = min(max(new_val, 0), 1)
            forecast_data.append({'Country': country, 'Year': year, 'Power_Index': new_val})
            last_values[country] = new_val

    df_forecast = pd.DataFrame(forecast_data)
    return pd.concat([df, df_forecast]).reset_index(drop=True)

# Load all dataframes
df_forecasts = load_forecast_data()
df_trade = load_trade_data()
df_power = load_power_index_data()

# Plotting color map -- KEY FIX: Changed 'US' to 'USA' to prevent KeyError
PLOT_COLORS = {'China': COMPANY_COLORS['red_primary'], 'USA': COMPANY_COLORS['medium_grey'], 'EU': COMPANY_COLORS['light_grey'], 'Nigeria': '#D3D3D3'}

# --- UI LAYOUT ---
st.markdown('<h1 class="main-header">Modern Mercantilism: Decoding the New Global Order</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7f8c8d;">A Data-Driven Analysis of the Four-Cycle Machine Shaping Global Economics</p>', unsafe_allow_html=True)

# Stationary Tab Navigation
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Executive Dashboard", "📈 Forecast Analysis", "📈 Trade Dynamics", 
    "⚡ Power Index Trends", "🌍 Sub-Saharan Focus", "🔄 Causal Loops"
])


# --- PAGE 1: EXECUTIVE DASHBOARD ---
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>{len(df_forecasts)}</h3><p>Strategic Forecasts</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>{df_forecasts["probability"].mean():.1f}%</h3><p>Average Probability</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>{len(df_forecasts[df_forecasts["probability"] >= 80])}</h3><p>High Confidence (≥80%)</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h3>{len(df_forecasts[df_forecasts["category"].str.contains("SSA")])}</h3><p>Sub-Saharan Focused</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2]) # Adjusted column ratio
    with col1:
        st.markdown('<h2 class="sub-header">📈 SSA Trade Volume by Major Power (with Forecast)</h2>', unsafe_allow_html=True)
        fig_trade = go.Figure()
        
        # --- MODIFIED: Split data for historical and forecast plotting ---
        hist_trade = df_trade[df_trade['year'] <= 2024]
        fcst_trade = df_trade[df_trade['year'] >= 2024] # Overlap one year for continuous line

        # Plot historical data with solid lines
        fig_trade.add_trace(go.Scatter(x=hist_trade['year'], y=hist_trade['China'], mode='lines+markers', name='China (Hist.)', line=dict(color=PLOT_COLORS['China'], width=4)))
        fig_trade.add_trace(go.Scatter(x=hist_trade['year'], y=hist_trade['US'], mode='lines+markers', name='USA (Hist.)', line=dict(color=PLOT_COLORS['USA'], width=4)))
        fig_trade.add_trace(go.Scatter(x=hist_trade['year'], y=hist_trade['EU'], mode='lines+markers', name='EU (Hist.)', line=dict(color=PLOT_COLORS['EU'], width=4)))

        # Plot forecast data with dashed lines
        fig_trade.add_trace(go.Scatter(x=fcst_trade['year'], y=fcst_trade['China'], mode='lines', name='China (Fcst.)', line=dict(color=PLOT_COLORS['China'], width=3, dash='dash')))
        fig_trade.add_trace(go.Scatter(x=fcst_trade['year'], y=fcst_trade['US'], mode='lines', name='USA (Fcst.)', line=dict(color=PLOT_COLORS['USA'], width=3, dash='dash')))
        fig_trade.add_trace(go.Scatter(x=fcst_trade['year'], y=fcst_trade['EU'], mode='lines', name='EU (Fcst.)', line=dict(color=PLOT_COLORS['EU'], width=3, dash='dash')))

        fig_trade.update_layout(title="Trade Volume (Billions USD) - Historical & Forecast to 2034", xaxis_title="Year", yaxis_title="Volume ($B)", template="plotly_dark", height=400, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_trade, use_container_width=True)
    
    with col2:
        st.markdown('<h2 class="sub-header">Average Forecast Probability Per Category</h2>', unsafe_allow_html=True)
        avg_prob_by_cat = df_forecasts.groupby('category')['probability'].mean().sort_values(ascending=True)
        fig_prob = px.bar(
            avg_prob_by_cat,
            x=avg_prob_by_cat.values,
            y=avg_prob_by_cat.index,
            orientation='h',
            labels={'x': 'Average Probability (%)', 'y': 'Category'},
            text_auto='.2s'
        )
        fig_prob.update_traces(marker_color=COMPANY_COLORS['red_primary'], textposition='outside')
        fig_prob.update_layout(height=400, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_prob, use_container_width=True)

    st.markdown('<h2 class="sub-header">🔄 The Four-Cycle Machine of Modern Mercantilism</h2>', unsafe_allow_html=True)
    cycle_cols = st.columns(4)
    cycles = [
        ("💰 Debt & Monetary", "States weaponize payment systems, debt-diplomacy, and digital currency races."),
        ("🏛️ Protectionism & Nationalism", "Tariffs and subsidies serve domestic stabilization and regime legitimacy."),
        ("🌍 Geopolitical Bloc & Friendshoring", "Globalization becomes a contest between economic blocs & alliances (i.e.: G7, BRICS+)."),
        ("🔬 Green Tech & Natural Disasters", "Tech and climate become primary arenas for state-backed competition.")
    ]
    for i, (title, desc) in enumerate(cycles):
        with cycle_cols[i]:
            st.markdown(f'<div class="cycle-card"><h4>{title}</h4><p style="font-size: 0.9rem;">{desc}</p></div>', unsafe_allow_html=True)

# --- PAGE 2: FORECAST ANALYSIS ---
with tab2:
    st.markdown('<h2 class="sub-header">📈 Strategic Forecasts Analysis</h2>', unsafe_allow_html=True)

    # Initialize session state for filters and widgets if not already done
    # This dictionary now defines our streamlined category groups
    category_mapping = {
        "Trade": ["Trade Policy", "Digital Trade", "Trade Balance"],
        "Policy": ["Industrial Policy", "Climate Policy"],
        "Controls": ["Investment Controls", "Resource Controls", "Tech Controls"],
        "Resources": ["Resource Security", "SSA Resource Power", "Green Investment"],
        "Monetary/Finance": ["Monetary System", "SSA Digital Currency", "SSA Digital Markets"],
    }
    
    # Initialize session state using the new streamlined categories
    if 'streamlined_cat_initialized' not in st.session_state:
        st.session_state.streamlined_cat_initialized = True
        for cat_group in category_mapping.keys():
            st.session_state[f'cat_group_{cat_group}'] = True

    if 'data_editor_key' not in st.session_state:
        st.session_state.data_editor_key = 0

    # --- REVISED FILTERS ---
    with st.expander("Show Filters", expanded=True):
        
        # --- 1. Driving Cycle Filter ---
        st.markdown("#### 1. Filter by Core Driving Cycle")
        st.markdown("<p style='font-size: 0.9rem; color: #AAAAAA;'>Select core cycles. The table will show any forecast linked to <b>at least one</b> of your selections.</p>", unsafe_allow_html=True)
        core_cycles = ["Debt/Monetary", "Internal Political", "Geopolitical", "Technology", "Nature"]
        cycle_cols = st.columns(len(core_cycles))
        selected_core_cycles = []
        for i, cycle in enumerate(core_cycles):
            if cycle_cols[i].checkbox(cycle, value=True, key=f"core_cyc_{cycle}"):
                selected_core_cycles.append(cycle)

        st.markdown("---")
        
        # --- 2. Category Filter (NOW STREAMLINED) ---
        st.markdown("#### 2. Filter by Category")
        
        def select_all_streamlined_cats():
            for cat_group in category_mapping.keys(): st.session_state[f'cat_group_{cat_group}'] = True
        def deselect_all_streamlined_cats():
            for cat_group in category_mapping.keys(): st.session_state[f'cat_group_{cat_group}'] = False

        b1, b2, _ = st.columns([0.15, 0.15, 0.7]) 
        b1.button("Select All", on_click=select_all_streamlined_cats, use_container_width=True)
        b2.button("Deselect All", on_click=deselect_all_streamlined_cats, use_container_width=True)

        cat_cols = st.columns(len(category_mapping))
        selected_categories = []
        # Loop through the streamlined groups to create the UI
        for i, cat_group in enumerate(category_mapping.keys()):
            with cat_cols[i]:
                if st.checkbox(cat_group, key=f'cat_group_{cat_group}'):
                    # If checked, add all corresponding sub-categories to our filter list
                    selected_categories.extend(category_mapping[cat_group])

        st.markdown("---")

        # --- 3. Probability Filter ---
        st.markdown("#### 3. Filter by Minimum Probability")
        min_p = int(df_forecasts['probability'].min())
        max_p = 100
        min_prob_selection = st.slider(
            "Minimum Probability", min_value=min_p, max_value=max_p, value=min_p,
            label_visibility="collapsed"
        )

    # --- FILTERING LOGIC ---
    if not selected_core_cycles:
        cycle_filtered_df = df_forecasts[df_forecasts['cycle_link'].isnull()]
    else:
        pattern = '|'.join(selected_core_cycles)
        cycle_filtered_df = df_forecasts[df_forecasts['cycle_link'].str.contains(pattern, case=False, na=False)]

    # The rest of the logic remains the same, as `selected_categories` now contains the correct detailed list
    final_filtered_df = cycle_filtered_df[
        (cycle_filtered_df['category'].isin(selected_categories)) &
        (cycle_filtered_df['probability'] >= min_prob_selection)
    ].copy()
    
    # --- INTERACTIVE FORECAST TABLE & COMPARISON FEATURE ---
    if not final_filtered_df.empty:
        final_filtered_df.insert(0, "Compare", False)
        st.markdown("### 📋 Detailed Forecasts")
        st.info("💡 **Tip:** Check the 'Compare' box next to any forecast to analyze it side-by-side in the 'Comparison View' below.", icon="ℹ️")
        
        edited_df = st.data_editor(
            final_filtered_df,
            key=f"editor_{st.session_state.data_editor_key}",
            column_config={
                "Compare": st.column_config.CheckboxColumn(required=True),
                "category": None, # Hiding the category column from the table as it's now redundant visually
                "id": None, 
                "statement": st.column_config.TextColumn("Forecast Statement", width="large"),
                "probability": st.column_config.ProgressColumn("Probability (%)", format="%d%%", min_value=0, max_value=100),
                "resolution_criteria": None,
                "cycle_link": "Driving Cycle(s)"
            },
            use_container_width=True, hide_index=True,
            disabled=df_forecasts.columns.tolist()
        )
        
        comparison_df = edited_df[edited_df["Compare"]]
        if not comparison_df.empty:
            st.markdown('<h2 class="sub-header">⚖️ Comparison View</h2>', unsafe_allow_html=True)
            compare_cols = st.columns(len(comparison_df))
            for i, col in enumerate(compare_cols):
                forecast = comparison_df.iloc[i]
                with col:
                    st.markdown(f"##### {forecast['statement']}")
                    st.metric("Probability", f"{forecast['probability']}%")
                    # We can still show the specific category here if we want
                    st.markdown(f"**Specific Category:** `{forecast['category']}`")
                    st.markdown(f"**Cycle(s):** `{forecast['cycle_link']}`")
                    st.markdown(f"**Timeframe:** `{forecast['timeframe']}`")
            
            def clear_comparison_selection():
                st.session_state.data_editor_key += 1
            
            st.button("Clear Comparison Selection", on_click=clear_comparison_selection, use_container_width=True)
        else:
            st.info("Select forecasts above to see their detailed comparison here.")
                
# --- PAGE 3: TRADE DYNAMICS ---
with tab3:
    st.markdown('<h2 class="sub-header">📈 SSA Trade Dynamics: The New Great Game</h2>', unsafe_allow_html=True)
    
    st.markdown("#### 2024 SSA Trade Share")
    trade_2024 = df_trade[df_trade['year'] == 2024].iloc[0]
    total_2024 = trade_2024['China'] + trade_2024['US'] + trade_2024['EU']
    shares_2024 = {'China': (trade_2024['China'] / total_2024) * 100, 'USA': (trade_2024['US'] / total_2024) * 100, 'EU': (trade_2024['EU'] / total_2024) * 100}
    
    pie_colors = [PLOT_COLORS[name] for name in shares_2024.keys()]
    fig_share = px.pie(
        values=list(shares_2024.values()), 
        names=list(shares_2024.keys()), 
        color_discrete_sequence=pie_colors
    )
    fig_share.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#000000', width=2)))
    fig_share.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
    st.plotly_chart(fig_share, use_container_width=True)
    
    st.markdown("#### Trade Growth Rate (2001-2024)")
    start_trade = df_trade[df_trade['year'] == 2001].iloc[0]
    china_growth = ((trade_2024['China'] - start_trade['China']) / start_trade['China']) * 100
    us_growth = ((trade_2024['US'] - start_trade['US']) / start_trade['US']) * 100
    eu_growth = ((trade_2024['EU'] - start_trade['EU']) / start_trade['EU']) * 100
    growth_data = pd.DataFrame({'Country': ['China', 'USA', 'EU'], 'Growth_Rate (%)': [china_growth, us_growth, eu_growth]})
    fig_growth = px.bar(growth_data, x='Country', y='Growth_Rate (%)', color='Country', color_discrete_map=PLOT_COLORS)
    fig_growth.update_layout(showlegend=False, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_growth, use_container_width=True)

# --- PAGE 4: POWER INDEX TRENDS ---
with tab4:
    st.markdown('<h2 class="sub-header">⚡ Power Index: The Great Transition (with Forecast)</h2>', unsafe_allow_html=True)
    
    # --- MODIFIED: Split data for historical and forecast plotting ---
    hist_power = df_power[df_power['Year'] <= 2024]
    fcst_power = df_power[df_power['Year'] >= 2024]

    fig_power = go.Figure()

    for country in df_power['Country'].unique():
        # Plot historical data
        country_hist = hist_power[hist_power['Country'] == country]
        fig_power.add_trace(go.Scatter(x=country_hist['Year'], y=country_hist['Power_Index'], name=f'{country} (Hist.)', mode='lines+markers', line=dict(color=PLOT_COLORS[country], width=4, shape='spline')))
        # Plot forecast data
        country_fcst = fcst_power[fcst_power['Country'] == country]
        fig_power.add_trace(go.Scatter(x=country_fcst['Year'], y=country_fcst['Power_Index'], name=f'{country} (Fcst.)', mode='lines', line=dict(color=PLOT_COLORS[country], width=3, dash='dash', shape='spline')))
    
    fig_power.update_layout(title="Power Index Trends - Historical & Forecast to 2034", template="plotly_dark", height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_power, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Power Index: 2000 vs 2024")
        power_2000 = df_power[df_power['Year'] == 2000].set_index('Country')['Power_Index']
        power_2024 = df_power[df_power['Year'] == 2024].set_index('Country')['Power_Index']
        comparison_df = pd.DataFrame({'2000': power_2000, '2024': power_2024}).reset_index()
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(name='2000', x=comparison_df['Country'], y=comparison_df['2000'], marker_color=COMPANY_COLORS['light_grey']))
        fig_comp.add_trace(go.Bar(name='2024', x=comparison_df['Country'], y=comparison_df['2024'], marker_color=COMPANY_COLORS['medium_grey']))
        fig_comp.update_layout(barmode='group', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_comp, use_container_width=True)

    with col2:
        st.markdown("#### Power Index Components (2024, Simulated)")
        components = ['Education', 'Innovation', 'Competitiveness', 'Military', 'Trade Share', 'Reserve Currency', 'Financial Center']
        component_scores = {'USA': [0.85, 0.95, 0.80, 0.95, 0.70, 0.90, 0.95], 'China': [0.75, 0.85, 0.90, 0.80, 0.85, 0.20, 0.60], 'EU': [0.80, 0.75, 0.75, 0.60, 0.70, 0.30, 0.80], 'Nigeria': [0.40, 0.35, 0.45, 0.40, 0.30, 0.10, 0.25]}
        fig_radar = go.Figure()
        for country in component_scores.keys():
            fig_radar.add_trace(go.Scatterpolar(r=component_scores[country], theta=components, fill='toself', name=country, line_color=PLOT_COLORS[country]))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_radar, use_container_width=True)

# --- PAGE 5: SSA FOCUS ---
with tab5:
    st.markdown('<h2 class="sub-header">🌍 Sub-Saharan Africa: The New Modern Mercantilism Playground</h2>', unsafe_allow_html=True)
    ssa_forecasts = df_forecasts[df_forecasts['category'].str.contains('SSA')]
    if not ssa_forecasts.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            fig_ssa = px.bar(ssa_forecasts, x='probability', y='statement', orientation='h', title="SSA-Focused Forecasts", color='probability', color_continuous_scale='Reds')
            fig_ssa.update_layout(height=400, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_ssa, use_container_width=True)
        with col2:
            st.markdown("### 🎯 SSA Strategic Importance")
            st.markdown("- **Resource Wealth**: Critical minerals for energy transition\n- **Demographic Dividend**: Young, growing population\n- **Market Potential**: Emerging consumer class\n- **Strategic Location**: Gateway to global trade routes")

    # --- REVISED: Changed to a 100% Stacked Bar Chart for Debt Composition ---
    st.markdown("### 📊 Composition of SSA External Public Debt")
    debt_data = pd.DataFrame({'Year': [2015, 2018, 2020, 2022, 2024], 'China_Debt_Share': [15, 25, 36, 38, 40]})
    debt_data['Other_Lenders_Share'] = 100 - debt_data['China_Debt_Share']

    # Melt the dataframe to make it suitable for a stacked bar chart
    debt_melted = debt_data.melt(
        id_vars='Year', 
        value_vars=['China_Debt_Share', 'Other_Lenders_Share'],
        var_name='Lender',
        value_name='Share'
    )
    # Clean up the lender names
    debt_melted['Lender'] = debt_melted['Lender'].replace({'China_Debt_Share': 'China', 'Other_Lenders_Share': 'Other Lenders'})
    
    fig_debt_stacked = px.bar(
        debt_melted,
        x='Year',
        y='Share',
        color='Lender',
        title="China's Share of SSA External Debt vs. Other Lenders",
        barmode='stack',
        text_auto='.2s',
        color_discrete_map={
            'China': COMPANY_COLORS['red_primary'],
            'Other Lenders': COMPANY_COLORS['medium_grey']
        }
    )
    fig_debt_stacked.update_traces(textangle=0, textposition='inside')
    fig_debt_stacked.update_layout(
        xaxis_title="Year",
        yaxis_title="Share of External Debt (%)",
        yaxis_ticksuffix='%',
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        legend_title_text='Lender'
    )
    st.plotly_chart(fig_debt_stacked, use_container_width=True)


# --- PAGE 6: CAUSAL LOOPS ---
with tab6:
    st.markdown('<h2 class="sub-header">🔄 Causal Loop Analysis</h2>', unsafe_allow_html=True)
    loop_type = st.selectbox("Select Causal Loop to Analyze:", ["China's BRI Loop", "Global Tariff Spiral"])
    if loop_type == "China's BRI Loop":
        st.markdown("### China's Belt & Road Infrastructure Loop")
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
        # --- VISUALIZE THE REINFORCING LOOP AS A CIRCLE ---

        loop_steps = [
            "Infrastructure Investment",
            "Resource Exports",
            "Chinese Imports",
            "Production Displacement",
            "Debt Accumulation",
            "Policy Leverage"
        ]
        n = len(loop_steps)
        angle_step = 2 * math.pi / n
        radius = 1

        # Calculate (x, y) positions for each step
        points = [
            (radius * math.cos(i * angle_step - math.pi/2), radius * math.sin(i * angle_step - math.pi/2))
            for i in range(n)
        ]

        # Create the circular loop diagram
        fig_circle = go.Figure()

        # Draw the circle (for visual reference)
        circle_theta = [i * 2 * math.pi / 100 for i in range(101)]
        circle_x = [radius * math.cos(t) for t in circle_theta]
        circle_y = [radius * math.sin(t) for t in circle_theta]
        fig_circle.add_trace(go.Scatter(
            x=circle_x, y=circle_y, mode='lines',
            line=dict(color=COMPANY_COLORS['medium_grey'], width=2),
            hoverinfo='skip', showlegend=False
        ))

        # Add points and labels
        for i, (x, y) in enumerate(points):
            fig_circle.add_trace(go.Scatter(
            x=[x], y=[y], mode='markers+text',
            marker=dict(size=32, color=COMPANY_COLORS['red_primary']),
            text=[f"{i+1}"], textposition="middle center",
            hovertemplate=f"<b>Step {i+1}:</b> {loop_steps[i]}<extra></extra>",
            showlegend=False
            ))
            # Add step label slightly outside the circle
            label_x = 1.18 * x
            label_y = 1.18 * y
            fig_circle.add_annotation(
            x=label_x, y=label_y, text=loop_steps[i],
            showarrow=False, font=dict(size=14, color=COMPANY_COLORS['light_grey_text']),
            align='center', xanchor='center', yanchor='middle'
            )

        # Draw arrows between points to show the loop direction
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i+1)%n]
            # Shorten arrows so they don't overlap the markers
            shrink = 0.18
            dx = x1 - x0
            dy = y1 - y0
            length = math.sqrt(dx**2 + dy**2)
            x_start = x0 + dx * shrink / length
            y_start = y0 + dy * shrink / length
            x_end = x1 - dx * shrink / length
            y_end = y1 - dy * shrink / length
            fig_circle.add_annotation(
            x=x_end, y=y_end, ax=x_start, ay=y_start,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=2,
            arrowcolor=COMPANY_COLORS['red_accent'], opacity=0.85
            )

        fig_circle.update_layout(
            title="Reinforcing Loop: China's BRI Cycle",
            xaxis=dict(visible=False, range=[-1.5, 1.5]),
            yaxis=dict(visible=False, range=[-1.5, 1.5]),
            height=500, width=500,
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=60, b=20)
        )
        st.plotly_chart(fig_circle, use_container_width=False)

    elif loop_type == "Global Tariff Spiral":
        st.markdown("### 💸 Global Tariff Escalation Loop")
        # --- MODIFIED: Extended tariff forecast to 2034 ---
        tariff_data = {
            'Year': list(range(2018, 2035)),
            'US_Tariffs': [f"{7.4 + 0.8*i:.1f}%" for i in range(17)],
            'Retaliatory_Tariffs': [f"{5.2 + 0.9*i:.1f}%" for i in range(17)],
            'Global_Average': [f"{6.8 + 0.7*i:.1f}%" for i in range(17)]
        }
        fig_spiral = go.Figure()
        colors_spiral = {'US_Tariffs': COMPANY_COLORS['red_primary'], 'Retaliatory_Tariffs': COMPANY_COLORS['medium_grey'], 'Global_Average': COMPANY_COLORS['red_accent']}
        for key in ['US_Tariffs', 'Retaliatory_Tariffs', 'Global_Average']:
            # Convert percentage string to float for plotting
            y_values = [float(v.strip('%')) for v in tariff_data[key]]
            fig_spiral.add_trace(go.Scatter(x=tariff_data['Year'], y=y_values, mode='lines+markers', name=key.replace('_', ' '), line=dict(color=colors_spiral[key], width=3)))
        
        fig_spiral.update_layout(
            title="Projected Tariff Escalation Spiral (to 2034)", 
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Average Tariff Rate (%)"
        )
        st.plotly_chart(fig_spiral, use_container_width=True)
