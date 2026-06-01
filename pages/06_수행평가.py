import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Alcohol and Happiness", layout="wide")

st.title("🍻 술을 많이 마시는 나라가 더 행복할까?")
st.subheader("나라별 알코올 소비량과 행복지수 상관관계 분석 (수행평가)")
st.markdown("---")

try:
    df_alc = pd.read_csv("alcohol_consumption_around_the_world.csv")
    df_hap = pd.read_csv("world-happiness-report-2024.csv")
    
    df_alc.columns = df_alc.columns.str.strip().str.lower()
    df_hap.columns = df_hap.columns.str.strip().str.lower()
    
    if "country name" in df_hap.columns:
        df_hap = df_hap.rename(columns={"country name": "country"})

    df_alc["country"] = df_alc["country"].str.strip().str.lower()
    df_hap["country"] = df_hap["country"].str.strip().str.lower()

    alc_year_col = ""
    for col in df_alc.columns:
        if "year" in col or "yr" in col or "date" in col:
            alc_year_col = col
            break

    hap_year_col = ""
    for col in df_hap.columns:
        if "year" in col or "yr" in col or "date" in col:
            hap_year_col = col
            break

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

    use_year_filter = False
    if alc_year_col != "" and hap_year_col != "":
        common_years = sorted(list(set(df_alc[alc_year_col].unique()).intersection(set(df_hap[hap_year_col].unique()))))
        if len(common_years) > 0:
            st.sidebar.header("⚙️ 연도 선택")
            min_y = int(min(common_years))
            max_y = int(max(common_years))
            selected_year = st.sidebar.slider("📅 분석할 연도를 골라보세요", min_value=min_y, max_value=max_y, value=max_y)
            
            df_alc_filtered = df_alc[df_alc[alc_year_col] == selected_year]
            df_hap_filtered = df_hap[df_hap[hap_year_col] == selected_year]
            use_year_filter = True
            st.success(f"현재 {selected_year}년 데이터를 분석 중입니다!")

    if not use_year_filter:
        st.sidebar.info("💡 데이터 특성에 맞춰 전체 평균 데이터로 분석을 진행합니다.")
        df_alc_filtered = df_alc.groupby("country")[alc_col].mean().reset_index()
        df_hap_filtered = df_hap.groupby("country")[hap_col].mean().reset_index()

    st.header("📈 1. 전 세계 알코올 소비량 추이")
    if alc_year_col != "":
        df_trend = df_alc.groupby(alc_year_col)[alc_col].mean().reset_index()
        fig_line = px.line(df_trend, x=alc_year_col, y=alc_col, title="연도별 전 세계 평균 알코올 소비량 변화", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("💡 데이터에 연도 정보가 없어 추이 그래프는 생략합니다.")
    st.markdown("---")

    st.header("📊 2. 술을 가장 많이 마시는 나라 Top 20")
    df_top20 = df_alc_filtered.sort_values(by=alc_col, ascending=False).head(20)
    
    bar_colors = []
    for c in df_top20["country"]:
        if "korea" in str(c):
            bar_colors.append("#E74C3C")
        else:
            bar_colors.append("#34495E")
            
    fig_bar = px.bar(df_top20, x="country", y=alc_col, title="알코올 소비량 상위 20개국 (대한민국은 빨간색 🔴)")
    fig_bar.update_traces(marker_color=bar_colors)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("---")

    st.header("🎯 3. 알코올 소비량과 행복지수의 관계")
    df_merged = pd.merge(df_alc_filtered, df_hap_filtered, on="country", how="inner")

    if not df_merged.empty:
        df_group = []
        df_size = []
        for c in df_merged["country"]:
            if "korea" in str(c):
                df_group.append("Korea")
                df_size.append(16)
            else:
                df_group.append("Others")
                df_size.append(8)
                
        df_merged["group"] = df_group
        
        fig_scatter = px.scatter(
            df_merged, x=alc_col, y=hap_col, color="group",
            color_discrete_map={"Korea": "#E74C3C", "Others": "#AED6F1"},
            hover_name="country", title="알코올 소비량과 행복지수 산점도 (국가 이름은 마우스를 대보세요!)",
            size=df_size, size_max=16
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        corr_value = df_merged[alc_col].corr(df_merged[hap_col])
        st.subheader("💡 데이터 분석 결론")
        st.write(f"두 데이터의 상관계수는 **{corr_value:.2f}** 입니다.")
        
        if corr_value > 0.2:
            st.info("✨ 결론: 술을 많이 마시는 나라가 더 행복한 경향이 있네요!")
        elif corr_value < -0.2:
            st.info("✨ 결론: 술을 많이 마시는 나라일수록 덜 행복한 경향이 있네요!")
        else:
            st.info("✨ 결론: 술 소비량과 행복지수 사이에는 뚜렷한 관계가 없어요. 행복은 술이 아닌 다른 게 결정하나 봐요! 🎉")
    else:
        st.error("데이터 매칭에 실패했습니다. 파일 안의 국가 이름을 확인해 주세요.")

except FileNotFoundError:
    st.error("⚠️ [파일 에러] CSV 파일 이름을 찾을 수 없어요! 깃허브 최상위 폴더에 파일이 제대로 있는지 꼭 확인해 주세요.")
