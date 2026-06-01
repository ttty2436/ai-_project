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

    # [🔥 핵심 보완 1] 연도(Year) 컬럼 자동으로 매칭하기
    alc_year_col = [col for col in df_alc.columns if 'year' in col or 'yr' in col or 'date' in col]
    hap_year_col = [col for col in df_hap.columns if 'year' in col or 'yr' in col or 'date' in col]

    # [🔥 핵심 보완 2] 알코올 소비량 및 행복 점수 컬럼 매칭
    alc_col = [col for col in df_alc.columns if 'consumption' in col or 'total' in col or 'liter' in col or 'alcohol' in col][0]
    hap_col = [col for col in df_hap.columns if 'score' in col or 'happiness' in col or 'ladder' in col][0]

    # 3. Sidebar - Year Filter (연도 컬럼이 양쪽 다 진짜 있을 때만 실행)
    use_year_filter = False
    if alc_year_col and hap_year_col:
        a_yr = alc_year_col[0]
        h_yr = hap_year_col[0]
        
        common_years = sorted(list(set(df_alc[a_yr].unique()).intersection(set(df_hap[h_yr].unique()))))
        if common_years:
            st.sidebar.header("⚙️ 연도 선택")
            selected_year = st.sidebar.slider("📅 분석할 연도를 골라보세요", min_value=int(min(common_years)), max_value=int(max(common_years)), value=int(max(common_years)))
            
            df_alc_filtered = df_alc[df_alc[a_yr] == selected_year]
            df_hap_filtered = df_hap[df_hap[h_yr] == selected_year]
            use_year_filter = True
            st.success(f" 현재 **{selected_year}년** 데이터를 분석 중입니다!")

    # 만약 연도 컬럼이 없거나 매칭 실패 시 -> 국가별 평균값(Mean)으로 안전하게 진행!
    if not use_year_filter:
        st.sidebar.info("💡 데이터 특성에 맞춰 전체 평균 데이터로 분석을 진행합니다.")
        df_alc_filtered = df_alc.groupby('country')[alc_col].mean().reset_index()
        df_hap_filtered = df_hap.groupby('country')[hap_col].mean().reset_index()

    # 4. Chart 1: Line Chart (Global Trend)
    st.header("📈 1. 전 세계 알코올 소비량 추이")
    if alc_year_col:
        df_trend = df_alc.groupby(alc_year_col[0])[alc_col].mean().reset_index()
        fig_line = px.line(df_trend, x=alc_year_col[0], y=alc_col, title="연도별 전 세계 평균 알코올 소비량 변화", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("💡 데이터에 연도 정보가 없어 추
