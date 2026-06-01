import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & Korean Title
st.set_page_config(page_title="Alcohol & Happiness", layout="wide", page_icon="📊")

st.title("🍻 술을 많이 마시는 나라가 더 행복할까?")
st.subheader("나라별 알코올 소비량과 행복지수 상관관계 분석 (수행평가)")
st.markdown("---")

# 2. Load CSV Files
try:
    df_alc = pd.read_csv("alcohol_consumption_around_the_world.csv")
    df_hap = pd.read_csv("world-happiness-report-2024.csv")
    
    # Standardize column names to lowercase
    df_alc.columns = df_alc.columns.str.strip().str.lower()
    df_hap.columns = df_hap.columns.str.strip().str.lower()
    
    # Rename country name column for merging
    if 'country name' in df_hap.columns:
        df_hap = df_hap.rename(columns={'country name': 'country'})

    df_alc['country'] = df_alc['country'].str.strip().str.lower()
    df_hap['country'] = df_hap['country'].str.strip().str.lower()

    # [💡 파이썬 3.14 대응] 컬럼 매칭 로직을 가장 단순한 반복문으로 변경 (SyntaxError 방지)
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

    # 3. Sidebar - Year Filter
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
            st.success(f" 현재 **{selected_year}년** 데이터를 분석 중입니다!")

    # 연도 매칭 안될 때 예외 처리
    if not use_year_filter:
        st.sidebar.info("💡 데이터 특성에 맞춰 전체 평균 데이터로 분석을 진행합니다.")
        df_alc_filtered = df_alc.groupby('country')[alc_col].mean().reset_index()
        df_hap_filtered = df_hap.groupby('country')[hap_col].mean().reset_index()

    # 4. Chart 1: Line Chart (Global Trend)
    st.header("📈 1. 전 세계 알코올 소비량 추이")
    if alc_year_col != "":
        df_trend = df_alc.groupby(alc_year_col)[alc_col].mean().reset_index()
        fig_line = px.line(df_trend, x=alc_year_col, y=alc_col, title="연도별 전 세계 평균 알코올 소비량 변화", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("
