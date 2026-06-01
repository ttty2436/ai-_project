import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Alcohol & Happiness", layout="wide")

# 2. Main Title (Korean is safe here)
st.title("🍻 술을 많이 마시는 나라는 정말 더 행복할까?")
st.subheader("나라별 알코올 소비량과 행복지수 상관관계 분석 (수행평가)")
st.markdown("---")

try:
    # 3. Load CSV Files from root directory
    df_alc = pd.read_csv("alcohol-consumption.csv")
    df_hap = pd.read_csv("world-happiness-report-2024.csv")
    
    # Column preprocessing
    df_alc.columns = df_alc.columns.str.strip().str.lower()
    df_hap.columns = df_hap.columns.str.strip().str.lower()
    
    if "country name" in df_hap.columns:
        df_hap = df_hap.rename(columns={"country name": "country"})
    if "entity" in df_alc.columns:
        df_alc = df_alc.rename(columns={"entity": "country"})

    df_alc["country"] = df_alc["country"].str.strip().str.lower()
    df_hap["country"] = df_hap["country"].str.strip().str.lower()

    # Find columns
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

    # 4. Sidebar Filter
    st.sidebar.header("⚙️ 분석 조건 설정")
    if alc_year_col != "":
        all_years = sorted(list(df_alc[alc_year_col].unique()))
        min_y = int(min(all_years))
        max_y = int(max(all_years))
        
        selected_year = st.sidebar.slider("📅 어떤 연도의 데이터를 볼까요?", min_value=min_y, max_value=max_y, value=max_y)
        df_alc_filtered = df_alc[df_alc[alc_year_col] == selected_year]
        st.sidebar.success(f"알코올 데이터: {selected_year}년 기준 반영!")
    else:
        df_alc_filtered = df_alc.groupby("country")[alc_col].mean().reset_index()

    df_hap_filtered = df_hap.groupby("country")[hap_col].mean().reset_index()

    # 📈 Chart 1: Line Chart (Global Trend)
    st.header("📈 1. 전 세계 알코올 소비량은 어떻게 변했을까?")
    if alc_year_col != "":
        df_trend = df_alc.groupby(alc_year_col)[alc_col].mean().reset_index()
        fig_line = px.line(df_trend, x=alc_year_col, y=alc_col, title="연도별 전 세계 평균 알코올 소비량 변화 추이", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("💡 데이터에 연도 정보가 없어 추이 그래프는 생략합니다.")
    st.markdown("---")

    # 📊 Chart 2: Bar Chart (Top 20)
    st.header("📊 2. 술을 가장 많이 마시는 나라 Top 20")
    df_top20 = df_alc_filtered.sort_values(by=alc_col, ascending=False).head(20)
    
    bar_colors = []
    for c in df_top20["country"]:
        if "korea" in str(c):
            bar_colors.append("#E74C3C")  # 한국은 빨간색! 🔴
        else:
            bar_colors.append("#34495E")
            
    fig_bar = px.bar(df_top20, x="country", y=alc_col, title="국가별 알코올 소비량 상위 20개국 (대한민국은 빨간색 🔴)")
    fig_bar.update_traces(marker_color=bar_colors)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("---")

    # 🎯 Chart 3 & 4: Scatter Plot
    st.header("🎯 3. 알코올 소비량과 행복지수의 관계")
    df_merged = pd.merge(df_alc_filtered, df_hap_filtered, on="country", how="inner")

    if not df_merged.empty:
        df_group = []
        df_size = []
        for c in df_merged["country"]:
            if "korea" in str(c):
                df_group.append("대한민국 🔴")
                df_size.append(18)
            else:
                df_group.append("다른 국가들 🔵")
                df_size.append(8)
                
        df_merged["group"] = df_group
        
        fig_scatter = px.scatter(
            df_merged, x=alc_col, y=hap_col, color="group",
            color_discrete_map={"대한민국 🔴": "#E74C3C", "다른 국가들 🔵": "#AED6F1"},
            hover_name="country", title="알코올 소비량(X축)과 행복지수(Y축)의 분포 (마우스를 올려 나라 이름을 확인하세요!)",
            size=df_size, size_max=18
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # 💡 Conclusion
        corr_value = df_merged[alc_col].corr(df_merged[hap_col])
        st.subheader("💡 대시보드가 도출한 최종 결론")
        st.write(f"두 데이터의 상관계수는 현재 **{corr_value:.2f}** 입니다.")
        
        if corr_value > 0.3:
            st.success(f"✨ **결론:** 상관계수가 양수({corr_value:.2f})로 나타납니다! 술을 많이 마시는 나라가 더 행복한 경향이 있네요! 축제나 사교 문화가 발달한 국가일 수 있습니다.")
        elif corr_value < -0.3:
            st.warning(f"✨ **결론:** 상관계수가 음수({corr_value:.2f})로 나타납니다! 술을 많이 마시는 나라일수록 덜 행복한 경향이 있네요!")
        else:
            st.info(f"✨ **결론:** 상관계수가 0에 가깝습니다({corr_value:.2f}). 술 소비량과 행복지수 사이에는 뚜렷한 관계가 없어요. 행복은 술이 아닌 다른 요소가 결정하나 봐요! 🎉")
    else:
        st.error("😭 국가 이름을 매칭하는 데 실패했습니다.")

except FileNotFoundError:
    st.error("⚠️ [파일 에러] 깃허브 최상위 폴더에 'alcohol-consumption.csv'와 'world-happiness-report-2024.csv' 파일이 있는지 꼭 확인해 주세요!")
