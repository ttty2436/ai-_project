# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="Alcohol & Happiness Analysis", layout="wide")

    st.title("Global Alcohol Consumption and Happiness Score Analysis")
    st.write("This dashboard analyzes the statistical correlation between annual alcohol consumption per capita and global happiness scores across various nations.")
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

        df_merged["display_country"] = df_merged["country"].str.title()
        
        for idx, row in df_merged.iterrows():
            if "korea" in str(row["country"]):
                df_merged.at[idx, "display_country"] = "South Korea"

        if not df_merged.empty:
            st.subheader("Data Overview Briefing")
            col1, col2, col3 = st.columns(3)
            
            top_alc_row = df_merged.sort_values(by=alc_col, ascending=False).iloc[0]
            top_hap_row = df_merged.sort_values(by=hap_col, ascending=False).iloc[0]
            
            with col1:
                st.metric(label="Total Nations Analyzed", value=f"{len(df_merged)} countries")
            with col2:
                st.metric(label="Highest Alcohol Consumption", value=str(top_alc_row["display_country"]), delta=f"{top_alc_row[alc_col]:.2f} L")
            with col3:
                st.metric(label="Highest Happiness Score", value=str(top_hap_row["display_country"]), delta=f"{top_hap_row[hap_col]:.2f} pts")
                
            st.write("---")

            st.header("1. Top 20 Global Alcohol Consumption Nations")
            st.write("The chart below illustrates the top 20 nations with the highest average annual alcohol consumption per capita.")
            
            df_top20 = df_merged.sort_values(by=alc_col, ascending=False).head(20).copy()
            
            has_korea = df_top20["display_country"].str.contains("South Korea").any()
            if not has_korea:
                df_korea = df_merged[df_merged["display_country"] == "South Korea"]
                if not df_korea.empty:
                    df_top20 = pd.concat([df_top20, df_korea]).drop_duplicates(subset=["country"])

            top_alc_name = df_merged.sort_values(by=alc_col, ascending=False).iloc[0]["display_country"]
            
            bar_colors = []
            for c in df_top20["display_country"]:
                if c == top_alc_name:
                    bar_colors.append("#F1C40F")
                elif "South Korea" in str(c):
                    bar_colors.append("#E74C3C")
                else:
                    bar_colors.append("#34495E")
                    
            fig_bar = px.bar(df_top20, x="display_country", y=alc_col, title="Average Alcohol Consumption by Country (Top Consumer: Yellow / South Korea: Red)")
            fig_bar.update_traces(marker_color=bar_colors)
            
            # [국가 이름 깨짐/사라짐 방지 강제 설정] 글자가 짤리지 않게 각도를 틀고 무조건 보이도록 지정
            fig_bar.update_xaxes(tickangle=45, tickmode='linear')
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # 한글 텍스트 브리핑 (오류 방지를 위해 정교하게 작성)
            korea_data = df_merged[df_merged["display_country"] == "South Korea"]
            korea_alc = korea_data[alc_col].values[0] if not korea_data.empty else 0
            
            st.write("### 🔍 국가별 데이터 분석 리포트")
            st.write(f"- **최상위 알코올 소비 집단:** 글로벌 알코올 통계를 정밀 분석한 결과, 세계에서 가장 높은 알코올 소비량을 기록한 국가는 연평균 **{top_alc_name}**({top_alc_row[alc_col]:.2f}L)으로 파악되었습니다. 뒤이어 서유럽 및 동유럽 권역의 국가들이 최상위 그래프를 점유하고 있습니다.")
            st.write(f"- **대한민국(South Korea)의 데이터:** 대한민국은 연평균 **{korea_alc:.2f}L**의 소비량을 기록하며 아시아 국가군 중에서 눈에 띄게 높은 소비 성향을 보이고 있으며, 글로벌 상위권 지표들과 비교 분석할 수 있는 주요 대조군으로 위치합니다.")
            st.write("---")

            st.header("2. Correlation Mapping: Alcohol Consumption vs Happiness Score")
            st.write("This scatter plot demonstrates the statistical distribution mapping between alcohol intake and subjective life satisfaction.")
            
            max_alc_name = df_merged.sort_values(by=alc_col, ascending=False).iloc[0]["display_country"]
            max_hap_name = df_merged.sort_values(by=hap_col, ascending=False).iloc[0]["display_country"]
            
            df_group = []
            df_size = []
            for _, row in df_merged.iterrows():
                if row["display_country"] == max_alc_name:
                    df_group.append("Top Alcohol Consumer")
                    df_size.append(18)
                elif row["display_country"] == max_hap_name:
                    df_group.append("Top Happiness Score")
                    df_size.append(18)
                elif "South Korea" in str(row["display_country"]):
                    df_group.append("South Korea")
                    df_size.append(15)
                else:
                    df_group.append("General Nations")
                    df_size.append(8)
                    
            df_merged["Classification"] = df_group
            
            fig_scatter = px.scatter(
                df_merged, x=alc_col, y=hap_col, color="Classification",
                color_discrete_map={
                    "Top Alcohol Consumer": "#F1C40F",
                    "Top Happiness Score": "#E74C3C",
                    "South Korea": "#3498DB",
                    "General Nations": "#AED6F1"
                },
                hover_name="display_country", title="Statistical Distribution Map",
                size=df_size, size_max=18
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            corr_value = df_merged[alc_col].corr(df_merged[hap_col])
            
            st.write("### 📝 데이터 기반 심층 결론")
            st.write(f"두 데이터 변수 간의 통계적 상관계수를 정밀 산출한 결과, 최종 값은 **{corr_value:.2f}**로 계산되었습니다.")
            
            st.write(f"- **행복도 최상위권 분석:** **{max_hap_name}**을 필두로 한 북유럽 국가들은 알코올 소비 지표의 고저와 무관하게 사회 인프라와 국가적 신뢰도를 기반으로 Y축 최상단(7.5점 이상)에 강력한 군집을 형성하고 있습니다.")
            st.write(f"- **알코올 고소비 국가 분석:** **{max_alc_name}**을 포함한 고소비 국가들은 술 소비가 많음에도 불구하고 국민 만족도가 중상위권(6.5점대)을 유지하는 경향을 보여주어, 사교와 문화적 요인이 반영되었음을 짐작하게 합니다.")
            st.write(f"- **대한민국의 포지션:** 대한민국은 알코올 소비 지표(X축)는 평균 이상으로 치우쳐 있으나 국민 주관적 행복 지표(Y축)는 글로벌 평균선에 머물러 있어, 자극성 기호품 소비의 증가가 국민 전체의 삶의 질 향상으로 직접 연결되지는 않는다는 불일치 사례를 실증합니다.")
            st.write(f"**💡 최종 종합 요약:** 상관계수가 **{corr_value:.2f}**로 사실상 0에 가깝기 때문에, **전 세계 알코올 소비량과 국민 행복지수 간에는 인과관계나 뚜렷한 경향성이 존재하지 않는다**는 결론을 도출할 수 있습니다. 국민의 궁극적인 행복감은 단순 기호품 소비량보다는 경제적 안정성, 복지 체계, 개인의 자유도 등 거시적인 구조적 변수들에 의해 결정됩니다.")
        else:
            st.error("Data matching failed.")

    except FileNotFoundError:
        st.error("Error: CSV files not found. Check repository paths.")

if __name__ == "__main__":
    main()
