import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="Alcohol & Happiness Analysis", layout="wide")

    # 대시보드 본연의 주제에 집중한 타이틀
    st.title("📊 글로벌 알코올 소비량과 행복지수의 상관관계 분석")
    st.write("세계 각국의 1인당 연간 알코올 소비 데이터와 글로벌 행복 점수를 융합하여 두 지표 간의 통계적 연관성을 추적합니다.")
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

        if alc_col != "":
            df_alc[alc_col] = pd.to_numeric(df_alc[alc_col], errors='coerce')
        if hap_col != "":
            df_hap[hap_col] = pd.to_numeric(df_hap[hap_col], errors='coerce')

        df_alc = df_alc.dropna(subset=["country", alc_col])
        df_hap = df_hap.dropna(subset=["country", hap_col])

        df_alc_fixed = df_alc.groupby("country")[alc_col].mean().reset_index()
        df_hap_fixed = df_hap.groupby("country")[hap_col].mean().reset_index()

        df_merged = pd.merge(df_alc_fixed, df_hap_fixed, on="country", how="inner")
        df_merged = df_merged.dropna(subset=[alc_col, hap_col])

        if not df_merged.empty:
            # 상단 통계 요약 브리핑
            st.subheader("📌 핵심 데이터 브리핑")
            col1, col2, col3 = st.columns(3)
            
            top_alc_row = df_merged.sort_values(by=alc_col, ascending=False).iloc[0]
            top_hap_row = df_merged.sort_values(by=hap_col, ascending=False).iloc[0]
            
            with col1:
                st.metric(label="분석 대상 국가지표", value=f"{len
