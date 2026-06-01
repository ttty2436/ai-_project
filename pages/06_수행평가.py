import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(page_title="Alcohol and Happiness", layout="wide")

st.title("🍻 술을 많이 마시는 나라는 정말 더 행복할까?")
st.subheader("나라별 알코올 소비량과 행복지수 상관관계 분석 (수행평가)")
st.markdown("---")

try:
    # 2. 데이터 파일 로드
    df_alc = pd.read_csv("alcohol-consumption.csv")
    df_hap = pd.read_csv("world-happiness-report-2024.csv")
    
    # 컬럼명 소문자 및 공백 제거
    df_alc.columns = df_alc.columns.str.strip().str.lower()
    df_hap.columns = df_hap.columns.str.strip().str.lower()
    
    # 국가 컬럼명 통일 (entity나 country name을 모두 country로)
    if "country name" in df_hap.columns:
        df_hap = df_hap.rename(columns={"country name": "country"})
    if "entity" in df_alc.columns:
        df_alc = df_alc.rename(columns={"entity": "country"})

    df_alc["country"] = df_alc["country"].str.strip().str.lower()
    df_hap["country"] = df_hap["country"].str.strip().str.lower()

    # 3. 알코올 소비량 수치 컬럼과 행복 점수 컬럼 매칭
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

    # 알코올 데이터에 연도 컬럼이 있는지 확인
    alc_year_col = ""
    for col in df_alc.columns:
        if "year" in col or "yr" in col or "date" in col:
            alc_year_col = col
            break

    # 4. 연도 선택 슬라이더 (알코올 데이터에 연도가 있을 때만 활성화)
    st.sidebar.header("⚙️ 분석 조건 설정")
    if alc_year_col != "":
        all_years = sorted(list(df_alc[alc_year_col].unique()))
        min_y = int(min(all_years))
        max_y = int(max(all_years))
        
        selected_year = st.sidebar.slider("📅 어떤 연도의 알코올 데이터를 볼까요?", min_value=min_y, max_value=max_y, value=max_y)
        df_alc_filtered = df_alc[df_alc[alc_year_col] == selected_year]
        st.sidebar.success(f"알코올 데이터: {selected_year}년 기준 반영!")
    else:
        st.sidebar.info("💡 알코올 데이터에 연도 정보가 없어 전체 평균으로 분석합니다.")
        df_alc_filtered = df_alc.groupby("country")[alc_col].mean().reset_index()

    # 행복지수 데이터는 단일 연도(2024)라고 가정하고 국가별 최신 데이터로 고정
    df_hap_filtered = df_hap.groupby("country")[hap_col].mean().reset_index()

    # 📈 1. 전 세계 알코올 소비량 추이 (꺾은선)
    st.header("📈 1. 전 세계 알코올 소비량은 어떻게 변했을까?")
    if alc_year_col != "":
        df_trend = df_alc.groupby(alc_year_col)[alc_col].mean().reset_index()
        fig_line = px.line(df_trend, x=alc_year_col, y=alc_col, title="연도별 전 세계 평균 알코올 소비량 변화 추이", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("💡 데이터에 연도 트렌드가 없어 추이 그래프는 생략합니다.")
    st.markdown("---")

    # 📊 2. 술을 가장 많이 마시는 나라 Top 20 (막대그래프)
    st.header("📊 2. 술을 가장 많이 마시는 나라 Top 20")
    df_top20 = df_alc_filtered.sort_values(by=alc_col, ascending=False).head(20)
    
    bar_colors = []
    for c in df_top20["country"]:
        if "korea" in str(c):
            bar_colors.append("#E74C3C")  # 한국은 빨간색 🔴
        else:
            bar_colors.append("#34
