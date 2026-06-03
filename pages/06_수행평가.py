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
            st.subheader("📌 핵심 데이터 브리핑")
            col1, col2, col3 = st.columns(3)
            
            top_alc_row = df_merged.sort_values(by=alc_col, ascending=False).iloc[0]
            top_hap_row = df_merged.sort_values(by=hap_col, ascending=False).iloc[0]
            
            with col1:
                st.metric(label="분석 대상 국가지표", value=f"{len(df_merged)}개국")
            with col2:
                st.metric(label="최대 알코올 소비국", value=str(top_alc_row["country"]).upper(), delta=f"{top_alc_row[alc_col]:.2f} L")
            with col3:
                st.metric(label="최고 행복 점수 기록국", value=str(top_hap_row["country"]).upper(), delta=f"{top_hap_row[hap_col]:.2f} 점")
                
            st.write("---")

            st.header("📈 1. 전 세계 알코올 소비량 상위 20개국 현황")
            st.write("조사 기간 동안 1인당 연평균 알코올 소비량이 가장 높게 나타난 상위 20개 국가의 통계입니다.")
            
            df_top20 = df_merged.sort_values(by=alc_col, ascending=False).head(20)
            top_alc_country = df_top20.iloc[0]["country"]
            
            bar_colors = []
            for c in df_top20["country"]:
                if c == top_alc_country:
                    bar_colors.append("#F1C40F")
                elif "korea" in str(c):
                    bar_colors.append("#E74C3C")
                else:
                    bar_colors.append("#34495E")
                    
            fig_bar = px.bar(df_top20, x="country", y=alc_col, title="국가별 평균 알코올 소비량 지표 (최대 소비국 💛 / 대한민국 ❤️)")
            fig_bar.update_traces(marker_color=bar_colors)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            st.info(f"💡 **통계 해석:** 글로벌 알코올 소비 상위권은 주로 유럽 및 서구권 국가들이 차지하고 있으며, 최상위권의 경우 연간 10리터 이상의 압도적인 소비량을 보입니다.")
            st.write("---")

            st.header("🎯 2. 알코올 소비량과 행복 점수의 매칭 분포")
            st.write("기호품 소비 성향이 실제 국민들의 주관적 삶의 질(행복)과 연관이 있는지 추적합니다.")
            
            max_alc_country = df_merged.sort_values(by=alc_col, ascending=False).iloc[0]["country"]
            max_hap_country = df_merged.sort_values(by=hap_col, ascending=False).iloc[0]["country"]
            
            df_group = []
            df_size = []
            for _, row in df_merged.iterrows():
                if row["country"] == max_alc_country:
                    df_group.append("알코올 소비 1위 💛")
                    df_size.append(18)
                elif row["country"] == max_hap_country:
                    df_group.append("행복지수 1위 ❤️")
                    df_size.append(18)
                elif "korea" in str(row["country"]):
                    df_group.append("대한민국 💙")
                    df_size.append(15)
                else:
                    df_group.append("일반 데이터")
                    df_size.append(8)
                    
            df_merged["구분"] = df_group
            
            fig_scatter = px.scatter(
                df_merged, x=alc_col, y=hap_col, color="구분",
                color_discrete_map={
                    "알코올 소비 1위 💛": "#F1C40F",
                    "행복지수 1위 ❤️": "#E74C3C",
                    "대한민국 💙": "#3498DB",
                    "일반 데이터": "#AED6F1"
                },
                hover_name="country", title="알코올 소비량(X축)과 행복 점수(Y축)의 통계적 분포",
                size=df_size, size_max=18
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            corr_value = df_merged[alc_col].corr(df_merged[hap_col])
            st.subheader("📝 데이터 분석 최종 결론")
            st.write(f"두 지표 간의 피어슨 상관계수(Pearson Correlation Coefficient) 분석 결과: **{corr_value:.2f}**")
            
            if corr_value > 0.3:
                st.success(f"상관계수가 {corr_value:.2f}로 유의미한 양의 상관성을 보입니다. 즉, 알코올 소비가 높은 문화권일수록 국민들이 인지하는 행복 점수 또한 높은 경향을 띱니다. 이는 집단적 유대감을 강조하는 축제나 사교 문화의 발달이 삶의 만족도와 연관되어 있을 가능성을 시사합니다.")
            elif corr_value < -0.3:
                st.warning(f"상관계수가 {corr_value:.2f}로 유의미한 음의 상관성을 보입니다. 알코올 소비량 증가가 오히려 국민 행복도의 저하 및 사회적 피로도 심화와 결을 같이하고 있음을 나타냅니다.")
            else:
                st.info(f"상관계수가 {corr_value:.2f}로 0에 근접합니다. 즉, 알코올 소비량과 국민의 행복지수 사이에는 통계적인 인과관계나 뚜렷한 경향성이 존재하지 않습니다. 국민의 행복 수준은 기호품 소비라는 지표보다는 경제적 안정성, 복지 인프라, 개인의 자유 등 보다 거시적이고 본질적인 사회 구조적 요인들에 의해 결정됨을 의미합니다.")
        else:
            st.error("데이터 매칭 실패")

    except FileNotFoundError:
        st.error("파일 로드 에러: CSV 파일 위치를 확인하세요.")

if __name__ == "__main__":
    main()
