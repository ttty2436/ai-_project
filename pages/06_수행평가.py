import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="수행평가 데이터 분석", layout="wide")

    # 1. 깔끔한 대제목 및 개요
    st.title("📊 전 세계 알코올 소비량과 행복지수의 상관관계 분석")
    st.write("본 대시보드는 국가별 전체 기간의 평균 데이터를 융합하여 데이터의 공백을 없애고 분석의 신뢰성을 높인 수행평가 자료입니다.")
    st.write("---")

    try:
        # 데이터 읽기
        df_alc = pd.read_csv("alcohol-consumption.csv")
        df_hap = pd.read_csv("world-happiness-report-2024.csv")
        
        # 컬럼명 전처리
        df_alc.columns = df_alc.columns.str.strip().str.lower()
        df_hap.columns = df_hap.columns.str.strip().str.lower()
        
        if "country name" in df_hap.columns:
            df_hap = df_hap.rename(columns={"country name": "country"})
        if "entity" in df_alc.columns:
            df_alc = df_alc.rename(columns={"entity": "country"})

        df_alc["country"] = df_alc["country"].str.strip().str.lower()
        df_hap["country"] = df_hap["country"].str.strip().str.lower()

        # 필요한 컬럼 자동 매칭
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

        # 데이터 정제 (결측치 제거)
        df_alc = df_alc.dropna(subset=[country, alc_col])
        df_hap = df_hap.dropna(subset=[country, hap_col])

        # ✨ [핵심 수정] 연도별로 쪼개지 않고, 국가별 '전체 평균값'을 내서 데이터 전원 매칭!
        df_alc_fixed = df_alc.groupby("country")[alc_col].mean().reset_index()
        df_hap_fixed = df_hap.groupby("country")[hap_col].mean().reset_index()

        # 데이터 병합
        df_merged = pd.merge(df_alc_fixed, df_hap_fixed, on="country", how="inner")
        df_merged = df_merged.dropna(subset=[alc_col, hap_col])

        if not df_merged.empty:
            # 2. 화면 상단에 완성도를 높여주는 '데이터 요약 상자(Metric)' 배치
            st.subheader("📌 데이터 분석 요약 정보")
            col1, col2, col3 = st.columns(3)
            
            top_alc_row = df_merged.sort_values(by=alc_col, ascending=False).iloc[0]
            top_hap_row = df_merged.sort_values(by=hap_col, ascending=False).iloc[0]
            
            with col1:
                st.metric(label="분석된 총 국가 수", value=f"{len(df_merged)}개국")
            with col2:
                st.metric(label="최고 알코올 소비국", value=top_alc_row["country"].upper(), delta=f"{top_alc_row[alc_col]:.2f} L")
            with col3:
                st.metric(label="최고 행복지수 국가", value=top_hap_row["country"].upper(), delta=f"{top_hap_row[hap_col]:.2f} 점")
                
            st.write("---")

            # 📊 1번 그래프: 알코올 소비 상위 20개국
            st.header("📈 1. 전 세계 알코올 소비량 상위 20개국")
            st.write("전체 조사 기간 동안 1인당 평균 알코올 소비량이 가장 많았던 20개 나라입니다.")
            
            df_top20 = df_merged.sort_values(by=alc_col, ascending=False).head(20)
            top_alc_country = df_top20.iloc[0]["country"]
            
            bar_colors = []
            for c in df_top20["country"]:
                if c == top_alc_country:
                    bar_colors.append("#F1C40F")  # 술 소비 1위 노란색 💛
                elif "korea" in str(c):
                    bar_colors.append("#E74C3C")  # 대한민국 포함 시 빨간색 ❤️
                else:
                    bar_colors.append("#34495E")   # 기본 네이비
                    
            fig_bar = px.bar(df_top20, x="
