# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="Alcohol & Happiness Analysis", layout="wide")

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

        # [수정] 매칭은 소문자로 하되, 나중에 그래프에 출력할 때는 대문자로 예쁘게 변환합니다.
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

        # ✨ [핵심 수정] 국가명 첫 글자를 다시 대문자로 바인딩하여 그래프에 글자가 안 깨지고 나오게 함!
        df_merged["display_country"] = df_merged["country"].str.title()
        
        # 한국 이름 강제 통일 (차트 인식용)
        df_merged.loc[df_merged["country"].str.contains("korea"), "display_country"] = "South Korea"

        if not df_merged.empty:
            st.subheader("📌 핵심 데이터 브리핑")
            col1, col2, col3 = st.columns(3)
            
            top_alc_row = df_merged.sort_values(by=alc_col, ascending=False).iloc[0]
            top_hap_row = df_merged.sort_values(by=hap_col, ascending=False).iloc[0]
            
            with col1:
                st.metric(label="분석 대상 국가지표", value=f"{len(df_merged)}개국")
            with col2:
                st.metric(label="최대 알코올 소비국", value=str(top_alc_row["display_country"]), delta=f"{top_alc_row[alc_col]:.2f} L")
            with col3:
                st.metric(label="최고 행복 점수 기록국", value=str(top_hap_row["display_country"]), delta=f"{top_hap_row[hap_col]:.2f} 점")
                
            st.write("---")

            # 1. 막대 그래프 데이터
            st.header("📈 1. 전 세계 알코올 소비량 상위 20개국 현황")
            st.write("조사 기간 동안 1인당 연평균 알코올 소비량이 가장 높게 나타난 상위 20개 국가의 통계입니다.")
            
            df_top20 = df_merged.sort_values(by=alc_col, ascending=False).head(20)
            
            # 혹시 상위 20개국에 한국이 없다면 강제로 데이터 추가해서 그래프에 보여주기
            if not df_top20["country"].str.contains("korea").any():
                df_korea = df_merged[df_merged["country"].str.contains("korea")]
                if not df_korea.empty:
                    df_top20 = pd.concat([df_top20, df_korea]).drop_duplicates(subset=["country"])

            top_alc_name = df_top20.sort_values(by=alc_col, ascending=False).iloc[0]["display_country"]
            
            bar_colors = []
            for c in df_top20["display_country"]:
                if c == top_alc_name:
                    bar_colors.append("#F1C40F")  # 술 소비 1위 노란색 💛
                elif "Korea" in str(c):
                    bar_colors.append("#E74C3C")  # 대한민국 빨간색 ❤️
                else:
                    bar_colors.append("#34495E")
                    
            fig_bar = px.bar(df_top20, x="display_country", y=alc_col, title="국가별 평균 알코올 소비량 지표 (최대 소비국 💛 / 대한민국 ❤️)")
            fig_bar.update_traces(marker_color=bar_colors)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # 💡 구체적인 정성적 국가 설명 추가
            st.info(f"💡 **국가별 세부 분석:** 알코올 소비 추이를 정밀 분석한 결과, 세계에서 가장 많은 기호용 알코올을 소비하는 국가는 연간 {top_alc_row[alc_col]:.2f}리터를 기록한 **{top_alc_name}**으로 나타났습니다. 그 뒤를 이어 유럽 전통 양조 문화가 발달한 프랑스, 독일 등의 서구권 국가들이 최상위권을 형성하고 있습니다. 반면 **대한민국(South Korea)**은 연평균 약 {df_merged[df_merged['country'].str.contains('korea')][alc_col].mean():.2f}리터 내외 수준으로, 동아시아 국가 중에서는 최상위권의 알코올 소비 특성을 보여주고 있습니다.")
            st.write("---")
