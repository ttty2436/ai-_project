import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(page_title="Alcohol & Happiness", layout="wide")

# 2. 한글 제목 및 서론 (출력부 한글은 100% 안전)
st.title("🍻 술을 많이 마시는 나라는 정말 더 행복할까?")
st.subheader("나라별 알코올 소비량과 행복지수 상관관계 분석 (수행평가)")
st.markdown("---")

try:
    # 3. 데이터 로드 (새로 받은 파일명 기준)
    df_alc = pd.read_csv("alcohol-consumption.csv")
    df_hap = pd.read_csv("world-happiness-report-2024.csv")
    
    # 컬럼명 대소문자 소문자로 통일 및 공백 제거
    df_alc.columns = df_alc.columns.str.strip().str.lower()
    df_hap.columns = df_hap.columns.str.strip().str.lower()
    
    # 국가 컬럼명 강제 통일
    if "country name" in df_hap.columns:
        df_hap = df_hap.rename(columns={"country name": "country"})
    if "entity" in df_alc.columns:
        df_alc = df_alc.rename(columns={"entity": "country"})

    df_alc["country"] = df_alc["country"].str.strip().str.lower()
    df_hap["country"] = df_hap["country"].str.strip().str.lower()

    # 데이터 컬럼 자동 매칭
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

    # [중요] 글자로 되어있을지 모르는 데이터를 강제로 숫자형으로 변환 (TypeError 방지)
    if alc_col != "":
        df_alc[alc_col] = pd.to_numeric(df_alc[alc_col], errors='coerce')
    if hap_col != "":
        df_hap[hap_col] = pd.to_numeric(df_hap[hap_col], errors='coerce')

    # 4. 사이드바 연도 필터 구현
    st.sidebar.header("⚙️ 분석 조건 설정")
    if alc_year_col != "":
        df_alc[alc_year_col] = pd.to_numeric(df_alc[alc_year_col], errors='coerce')
        df_alc = df_alc.dropna(subset=[alc_year_col])
        
        all_years = sorted(list(df_alc[alc_year_col].unique()))
        min_y = int(min(all_years))
        max_y = int(max(all_years))
        
        selected_year = st.sidebar.slider("📅 어떤 연도의 데이터를 볼까요?", min_value=min_y, max_value=max_y, value=max_y)
        df_alc_filtered = df_alc[df_alc[alc_year_col] == selected_year]
        st.sidebar.success(f"알코올 데이터: {selected_year}년 기준 반영!")
    else:
        df_alc_filtered = df_alc.groupby("country")[alc_col].mean().reset_index()

    df_hap_filtered = df_hap.groupby("country")[hap_col].mean().reset_index()

    # 📈 Chart 1: 연도별 전 세계 추이 (꺾은선)
    st.header("📈 1. 전 세계 알코올 소비량은 어떻게 변했을까?")
    if alc_year_col != "":
        df_trend = df_alc.groupby(alc_year_col)[alc_col].mean().reset_index()
        fig_line = px.line(df_trend, x=alc_year_col, y=alc_col, title="연도별 전 세계 평균 알코올 소비량 변화 추이", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("💡 데이터에 연도 정보가 없어 추이 그래프는 생략합니다.")
    st.markdown("---")

    # 📊 Chart 2: 알코올 소비 상위 20개국 (막대)
    st.header("📊 2. 술을 가장 많이 마시는 나라 Top 20")
