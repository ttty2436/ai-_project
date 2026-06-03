import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="수행평가 데이터 분석", layout="wide")

    # 1. 웹페이지 대제목 (필요 없는 서론 빼고 핵심만 깔끔하게!)
    st.title("📊 술 소비량과 행복지수의 상관관계 분석")
    st.write("세계 각국의 알코올 소비 데이터와 세계 행복 보고서 데이터를 연동한 대시보드입니다.")
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

        # 2. 사이드바 필터 설정 (한국어 변환)
        st.sidebar.subheader("⚙️ 데이터 필터 설정")
        if alc_year_col != "":
            df_alc[alc_year_col] = pd.to_numeric(df_alc[alc_year_col], errors='coerce')
            df_alc = df_alc.dropna(subset=[alc_year_col])
            
            all_years = sorted(list(df_alc[alc_year_col].unique()))
            min_y = int(min(all_years))
            max_y = int(max(all_years))
            
            selected_year = st.sidebar.slider("📅 분석할 연도를 선택하세요", min_value=min_y, max_value=max_y, value=max_y)
            df_alc_filtered = df_alc[df_alc[alc_year_col] == selected_year]
        else:
            df_alc_filtered = df_alc.groupby("country")[alc_col].mean().reset_index()

        df_hap_filtered = df_hap.groupby("country")[hap_col].mean().reset_index()

        # 📊 1번 그래프: 알코올 소비 상위 20개국 (1위 나라 강조!)
        st.header("📈 1. 국가별 알코올 소비량 Top 20")
        st.write("선택한 연도에 1인당 연간 알코올 소비량이 가장 많았던 상위 20개국입니다.")
        
        df_top20 = df_alc_filtered.sort_values(by=alc_col, ascending=False).head(20)
        
        if not df_top20.empty:
            # 1위 국가 찾아서 색상 채우기 로직 (1위는 노란색, 나머지는 차분한 네이비)
            top_alc_country = df_top20.iloc[0]["country"]
            
            bar_colors = []
            for c in df_top20["country"]:
                if c == top_alc_country:
                    bar_colors.append("#F1C40F")  # 1위는 노란색! 💛
                elif "korea" in str(c):
                    bar_colors.append("#E74C3C")  # 한국은 빨간색! ❤️
                else:
                    bar_colors.append("#34495E")
                    
            fig_bar = px.bar(df_top20, x="country", y=alc_col, title=f"[{selected_year}년] 알코올 소비 상위 20개국 (1위 노란색 💛 / 한국 포함시 빨간색 ❤️)")
            fig_bar.update_traces(marker_color=bar_colors)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # 그래프 설명 추가
            st.info(f"💡 **분석 내용:** {selected_year}년 기준, 전 세계에서 술을 가장 많이 마신 나라는 **'{top_alc_country.upper()}'**입니다. 주로 유럽권 국가들이 상위권에 많이 포진해 있는 경향을 보입니다.")
        else:
            st.warning("선택한 연도에 해당하는 알코올 데이터가 없습니다.")
            
        st.write("---")

        # 🎯 2번 그래프: 알코올 vs 행복지수 상관관계 산점도 (행복 1위, 술 1위 강조!)
        st.header("🎯 2. 알코올 소비량과 행복지수의 상관관계 분석")
        st.write("X축은 술 소비량, Y축은 행복 점수입니다. 두 지표가 어떤 연관성이 있는지 한눈에 보여줍니다.")
        
        df_merged = pd.merge(df_alc_filtered, df_hap_filtered, on="country", how="inner")
        df_merged = df_merged.dropna(subset=[alc_col, hap_col])

        if not df_merged.empty:
            max_alc_idx = df_merged[alc_col].idxmax()
            max_hap_idx = df_merged[hap_col].idxmax()
            
            df_group = []
            df_size = []
            for idx, row in df_merged.iterrows():
                if idx == max_alc_idx:
                    df_group.append("술 소비 1위 국가 💛")
                    df_size.append(18)
                elif idx == max_hap_idx:
                    df_group.append("행복지수 1위 국가 ❤️")
                    df_size.append(18)
                elif "korea" in str(row["country"]):
                    df_group.append("대한민국 💙")
                    df_size.append(15)
                else:
                    df_group.append("일반 국가들")
                    df_size.append(8)
                    
            df_merged["구분"] = df_group
            
            fig_scatter = px.scatter(
                df_merged, x=alc_col, y=hap_col, color="구분",
                color_discrete_map={
                    "술 소비 1위 국가 💛": "#F1C40F",
                    "행복지수 1위 국가 ❤️": "#E74C3C",
                    "대한민국 💙": "#3498DB",
                    "일반 국가들": "#AED6F1"
                },
                hover_name="country", title="알코올 소비량과 행복지수 분산 차트",
                size=df_size, size_max=18
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # 💡 통계적 수치에 기반한 수행평가 최종 결론 및 데이터 설명
            corr_value = df_merged[alc_col].corr(df_merged[hap_col])
            st.subheader("📝 수행평가 최종 분석 결론")
            st.write(f"두 데이터셋을 매칭하여 계산한 통계적 상관계수는 **{corr_value:.2f}** 입니다.")
            
            if corr_value > 0.3:
                st.success(f"상관계수가 양수({corr_value:.2f})로 나타납니다. 즉, **술을 많이 마시는 나라일수록 행복지수도 높은 경향**이 있습니다. 이는 사교적인 파티 문화나 축제가 활성화된 국가에서 두 지표가 동시에 높게 나타나기 때문으로 해석할 수 있습니다.")
            elif corr_value < -0.3:
                st.warning(f"상관계수가 음수({corr_value:.2f})로 나타납니다. 즉, **술을 많이 마시는 나라일수록 오히려 행복지수는 낮아지는 경향**이 있습니다. 과도한 알코올 소비가 사회적 스트레스나 삶의 질 저하와 연관이 있을 가능성을 시사합니다.")
            else:
                st.info(f"상관계수가 0에 가깝습니다({corr_value:.2f}). 결론적으로 **술 소비량과 국민의 행복지수 사이에는 통계적으로 뚜렷한 인과관계가 없다**고 볼 수 있습니다. 행복은 술이 아닌 경제력, 복지, 자유 등 다른 복합적인 사회적 요인에 의해 결정됩니다.")
        else:
            st.error("두 데이터의 국가명을 매칭하는 데 실패했거나 데이터가 비어있습니다.")

    except FileNotFoundError:
        st.error("파일 에러: 깃허브 최상위 폴더에 CSV 데이터 파일이 제대로 있는지 확인해 주세요.")

if __name__ == "__main__":
    main()
