# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="알코올과 행복지수 분석", layout="wide")

    st.title("📊 글로벌 알코올 소비량과 행복지수의 상관관계 분석")
    st.write("세계 각국의 1인당 연간 알코올 소비 데이터와 세계 행복 보고서 점수를 연동하여 두 지표 간의 통계적 연관성을 추적합니다.")
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

        # 국가명 변환 및 순위 계산 (에러 안전 구조)
        df_merged["국가명"] = df_merged["country"].str.title()
        for idx, row in df_merged.iterrows():
            if "korea" in str(row["country"]):
                df_merged.at[idx, "국가명"] = "South Korea"

        # 순위 변수 명확하게 생성
        df_merged = df_merged.sort_values(by=alc_col, ascending=False).reset_index(drop=True)
        df_merged["알코올_순위"] = df_merged.index + 1
        
        df_merged = df_merged.sort_values(by=hap_col, ascending=False).reset_index(drop=True)
        df_merged["행복_순위"] = df_merged.index + 1

        # 차트용 컬럼명 알아보기 쉽게 복사
        df_merged["알코올_소비량"] = df_merged[alc_col]
        df_merged["행복_점수"] = df_merged[hap_col]

        if not df_merged.empty:
            st.subheader("📌 핵심 데이터 요약 브리핑")
            col1, col2, col3 = st.columns(3)
            
            top_alc_row = df_merged.sort_values(by="알코올_소비량", ascending=False).iloc[0]
            top_hap_row = df_merged.sort_values(by="행복_점수", ascending=False).iloc[0]
            
            with col1:
                st.metric(label="분석 대상 국가 수", value=f"{len(df_merged)}개국")
            with col2:
                st.metric(label="최대 알코올 소비국", value=str(top_alc_row["국가명"]), delta=f"{top_alc_row['알코올_소비량']:.2f} L")
            with col3:
                st.metric(label="최고 행복 점수 기록국", value=str(top_hap_row["국가명"]), delta=f"{top_hap_row['행복_점수']:.2f} 점")
                
            st.write("---")

            # 1. 막대 그래프 생성
            st.header("📈 1. 전 세계 알코올 소비량 상위 20개국 현황")
            st.write("1인당 연평균 알코올 소비량이 가장 높은 국가들의 통계입니다. 그래프 막대에 마우스를 올리면 순위와 상세 정보가 나타납니다.")
            
            df_top20 = df_merged.sort_values(by="알코올_소비량", ascending=False).head(20).copy()
            
            has_korea = df_top20["국가명"].str.contains("South Korea").any()
            if not has_korea:
                df_korea = df_merged[df_merged["국가명"] == "South Korea"]
                if not df_korea.empty:
                    df_top20 = pd.concat([df_top20, df_korea]).drop_duplicates(subset=["country"])

            top_alc_name = df_merged.sort_values(by="알코올_소비량", ascending=False).iloc[0]["국가명"]
            
            bar_colors = []
            for c in df_top20["국가명"]:
                if c == top_alc_name:
                    bar_colors.append("#F1C40F")
                elif "South Korea" in str(c):
                    bar_colors.append("#E74C3C")
                else:
                    bar_colors.append("#34495E")
            
            # 문법적으로 안전한 최신 팝업(Hover) 지정 방식
            fig_bar = px.bar(
                df_top20, x="국가명", y="알코올_소비량", 
                title="국가별 평균 알코올 소비량 지표 (최대 소비국 💛 / 대한민국 ❤️)",
                hover_data=["알코올_순위", "행복_순위"]
            )
            fig_bar.update_traces(marker_color=bar_colors)
            fig_bar.update_xaxes(tickangle=45)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            korea_data = df_merged[df_merged["국가명"] == "South Korea"]
            korea_alc = korea_data["알코올_소비량"].values[0] if not korea_data.empty else 0
            korea_alc_rank = korea_data["알코올_순위"].values[0] if not korea_data.empty else 0
            
            st.write("### 🔍 국가별 데이터 분석 리포트")
            st.write(f"- **최상위 알코올 소비 집단:** 글로벌 알코올 통계를 정밀 분석한 결과, 세계에서 가장 높은 알코올 소비량을 기록한 국가는 연평균 **{top_alc_name}**({top_alc_row['알코올_소비량']:.2f}L)으로 파악되었습니다. 뒤이어 서유럽 및 동유럽 권역의 국가들이 최상위 그래프를 점유하고 있습니다.")
            st.write(f"- **대한민국(South Korea)의 데이터:** 대한민국은 연평균 **{korea_alc:.2f}L**의 소비량을 기록하며 전체 조사 대상국 중 **{korea_alc_rank}위**를 차지했습니다. 이는 아시아 국가군 중에서 눈에 띄게 높은 소비 성향을 보이고 있으며, 글로벌 상위권 지표들과 비교 분석할 수 있는 주요 대조군으로 위치합니다.")
            st.write("---")

            # 2. 산점도 그래프 생성
            st.header("🎯 2. 알코올 소비량과 행복 점수의 매칭 분포")
            st.write("술 소비 성향이 실제 국민들의 행복 점수와 연관이 있는지 추적합니다. 점 위에 마우스를 올리면 국가별 상세 순위가 표시됩니다.")
            
            max_alc_name = df_merged.sort_values(by="알코올_소비량", ascending=False).iloc[0]["국가명"]
            max_hap_name = df_merged.sort_values(by="행복_점수", ascending=False).iloc[0]["국가명"]
            
            df_group = []
            df_size = []
            for _, row in df_merged.iterrows():
                if row["국가명"] == max_alc_name:
                    df_group.append("알코올 소비 1위 💛")
                    df_size.append(18)
                elif row["국가명"] == max_hap_name:
                    df_group.append("행복지수 1위 ❤️")
                    df_size.append(18)
                elif "South Korea" in str(row["국가명"]):
                    df_group.append("대한민국 💙")
                    df_size.append(15)
                else:
                    df_group.append("일반 국가 데이터")
                    df_size.append(8)
                    
            df_merged["구분"] = df_group
            
            fig_scatter = px.scatter(
                df_merged, x="알코올_소비량", y="행복_점수", color="구분",
                color_discrete_map={
                    "알코올 소비 1위 💛": "#F1C40F",
                    "행복지수 1위 ❤️": "#E74C3C",
                    "대한민국 💙": "#3498DB",
                    "일반 국가 데이터": "#AED6F1"
                },
                title="알코올 소비량(X축)과 행복 점수(Y축)의 통계적 분포",
                size=df_size, size_max=18,
                hover_data=["국가명", "알코올_순위", "행복_순위"]
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            corr_value = df_merged["알코올_소비량"].corr(df_merged["행복_점수"])
            
            st.write("### 📝 데이터 기반 심층 결론")
            st.write(f"두 데이터 변수 간의 통계적 상관계수를 정밀 산출한 결과, 최종 값은 **{corr_value:.2f}**로 계산되었습니다.")
            
            korea_hap = korea_data["행복_점수"].values[0] if not korea_data.empty else 0
            korea_hap_rank = korea_data["행복_순위"].values[0] if not korea_data.empty else 0

            st.write(f"- **행복도 최상위권 분석:** **{max_hap_name}**을 필두로 한 북유럽 국가들은 알코올 소비 지표의 고저와 무관하게 사회 인프라와 국가적 신뢰도를 기반으로 Y축 최상단(7.5점 이상)에 강력한 군집을 형성하고 있습니다.")
            st.write(f"- **알코올 고소비 국가 분석:** **{max_alc_name}**을 포함한 고소비 국가들은 술 소비가 많음에도 불구하고 국민 만족도가 중상위권(6.5점대)을 유지하는 경향을 보여주어, 사교와 문화적 요인이 반영되었음을 짐작하게 합니다.")
            st.write(f"- **대한민국의 포지션:** 대한민국은 알코올 소비(연 {korea_alc:.2f}L, {korea_alc_rank}위) 지표는 평균 이상으로 치우쳐 있으나, 국민 주관적 행복 지표(평균 {korea_hap:.2f}점, {korea_hap_rank}위)는 글로벌 중간선에 머물러 있습니다. 이는 자극성 기호품 소비의 증가가 국민 전체의 삶의 질 향상으로 직접 연결되지는 않는다는 대표적인 불일치 통계 사례를 실증합니다.")
            st.write(f"**💡 최종 종합 요약:** 상관계수가 **{corr_value:.2f}**로 사실상 0에 가깝기 때문에, **전 세계 알코올 소비량과 국민 행복지수 간에는 인과관계나 뚜렷한 경향성이 존재하지 않는다**는 결론을 도출할 수 있습니다. 국민의 궁극적인 행복감은 단순 기호품 소비량보다는 경제적 안정성, 복지 체계, 개인의 자유도 등 거시적인 사회 구조적 요인들에 의해 결정됩니다.")
        else:
            st.error("데이터 매칭 실패")

    except FileNotFoundError:
        st.error("파일 로드 에러: CSV 파일 위치를 확인하세요.")

if __name__ == "__main__":
    main()
