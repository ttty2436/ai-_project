import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dataset Analysis", layout="wide")

st.title("Alcohol and Happiness Analysis")
st.write("Correlation analysis between alcohol consumption and happiness score.")
st.write("---")

try:
    df_alc = pd.read_csv("alcohol-consumption.csv")
    df_hap = pd.read_csv("world-happiness-report-2024.csv")
    
    df_alc.columns = df_alc.columns.str.strip().str.lower()
    df_hap.columns = df_hap.columns.str.strip().str.lower()
    
    if "country name" in df_hap.columns:
        df_hap = df_hap.rename(columns={"country name": "country"})
    if "entity" in df_alc.columns:
        df_alc = df_alc.rename(columns={"entity": "country"})

    df_alc["country"] = df_alc["country"].str.strip().str.lower()
    df_hap["country"] = df_hap["country"].str.strip().str.lower()

    alc_col = ""
    for col in df_alc.columns:
        if "consumption" in col or "total" in col or "liter" in col or "alcohol" in col:
            alc_col = col
            break
            
    hap_col = ""
    for col in df_hap.columns:
        if "score" in col or "happiness" in col or "ladder" in col:
            hap_col = col
            break

    alc_year_col = ""
    for col in df_alc.columns:
        if "year" in col or "yr" in col or "date" in col:
            alc_year_col = col
            break

    if alc_col != "":
        df_alc[alc_col] = pd.to_numeric(df_alc[alc_col], errors='coerce')
    if hap_col != "":
        df_hap[hap_col] = pd.to_numeric(df_hap[hap_col], errors='coerce')

    st.sidebar.subheader("Filter Setting")
    if alc_year_col != "":
        df_alc[alc_year_col] = pd.to_numeric(df_alc[alc_year_col], errors='coerce')
        df_alc = df_alc.dropna(subset=[alc_year_col])
        
        all_years = sorted(list(df_alc[alc_year_col].unique()))
        min_y = int(min(all_years))
        max_y = int(max(all_years))
        
        selected_year = st.sidebar.slider("Select Year", min_value=min_y, max_value=max_y, value=max_y)
        df_alc_filtered = df_alc[df_alc[alc_year_col] == selected_year]
    else:
        df_alc_filtered = df_alc.groupby("country")[alc_col].mean().reset_index()

    df_hap_filtered = df_hap.groupby("country")[hap_col].mean().reset_index()

    st.subheader("1. Global Alcohol Consumption Trend")
    if alc_year_col != "":
        df_trend = df_alc.groupby(alc_year_col)[alc_col].mean().reset_index()
        fig_line = px.line(df_trend, x=alc_year_col, y=alc_col, title="Trend", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    st.write("---")

    st.subheader("2. Top 20 Alcohol Consumption Countries")
    df_top20 = df_alc_filtered.sort_values(by=alc_col, ascending=False).head(20)
    
    bar_colors = []
    for c in df_top20["country"]:
        if "korea" in str(c):
            bar_colors.append("#E74C3C")
        else:
            bar_colors.append("#34495E")
            
    fig_bar = px.bar(df_top20, x="country", y=alc_col, title="Top 20")
    fig_bar.update_traces(marker_color=bar_colors)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.write("---")

    st.subheader("3. Alcohol vs Happiness Scatter Plot")
    df_merged = pd.merge(df_alc_filtered, df_hap_filtered, on="country", how="inner")
    df_merged = df_merged.dropna(subset=[alc_col, hap_col])

    if not df_merged.empty:
        df_group = []
        df_size = []
        for c in df_merged["country"]:
            if "korea" in str(c):
                df_group.append("Korea")
                df_size.append(18)
            else:
                df_group.append("Others")
                df_size.append(8)
                
        df_merged["group"] = df_group
        
        fig_scatter
