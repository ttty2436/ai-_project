import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정 및 이모지 제목 🎉
st.set_page_config(page_title="알코올 & 행복지수 분석", layout="wide", page_icon="📊")

st.title("🍻 술을 많이 마시는 나라가 더 행복할까?")
st.subheader("나라별 알코올 소비량과 행복지수 상관관계 분석 (수행평가)")
st.markdown("---")

# 2. 데이터 불러오기 (최상위 폴더에 있는 CSV 파일 이름 그대로 입력!) ⭐
try:
    # 스트림릿 클라우드는 기본적으로 최상위 폴더에서 실행되므로, 파일명만 적으면 됩니다.
    df_alc = pd.read_csv("alcohol_consumption_around_the_world.csv")
    df_hap = pd.read_csv("world-happiness-report-2024.csv")
    
    # 영어 컬럼명들을 다루기 쉽게 모두 소문자로 변환
    df_alc.columns = df_alc.columns.str.strip().str.lower()
    df_hap.columns = df_hap.columns.str.strip().str.lower()
    
    # 행복지수의 'country name' 컬럼을 알코올의 'country'와 이름 맞추기
    if 'country name' in df_hap.columns:
        df_hap = df_hap.rename(columns={'country name': 'country'})

    # 국가 이름 소문자로 통일 (매칭 잘 되도록!)
    df_alc['country'] = df_alc['country'].str.strip().str.lower()
    df_hap['country'] = df_hap['country'].str.strip().str.lower()

    # 3. 사이드바 연도 선택 슬라이더 🎛️
    st.sidebar.header("⚙️ 연도 선택")
    # 두 데이터에 공통으로 있는 연도 추출
    common_years = sorted(list(set(df_alc['year'].unique()).intersection(set(df_hap['year'].unique()))))
    
    if common_years:
        selected_year = st.sidebar.slider("📅 분석할 연도를 골라보세요", min_value=min(common_years), max_value=max(common_years), value=max(common_years))
        
        # 선택한 연도로 데이터 필터링
        df_alc_filtered = df_alc[df_alc['year'] == selected_year]
        df_hap_filtered = df_hap[df_hap['year'] == selected_year]
    else:
        st.sidebar.warning("공통 연도가 없어 전체 평균으로 분석합니다.")
        df_alc_filtered = df_alc
        df_hap_filtered = df_hap

    # 알코올 소비량 컬럼과 행복 점수 컬럼 자동 찾기
    alc_col = [col for col in df_alc.columns if 'consumption' in col or 'total' in col or 'liter' in col][0]
    hap_col = [col for col in df_hap.columns if 'score' in col or 'happiness' in col][0]

    # 4. 그래프 ①: 연도별 전 세계 평균 알코올 소비량 추이 (꺾은선) 📈
    st.header("📈 1. 전 세계 알코올 소비량 추이")
    df_trend = df_alc.groupby('year')[alc_col].mean().reset_index()
    fig_line = px.line(df_trend, x='year', y=alc_col, title="연도별 전 세계 평균 알코올 소비량 변화", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("---")

    # 5. 그래프 ②: 나라별 알코올 소비량 Top 20 (막대그래프 & 한국 강조) 📊
    st.header("📊 2. 술을 가장 많이 마시는 나라 Top 20")
    df_top20 = df_alc_filtered.sort_values(by=alc_col, ascending=False).head(20)
    
    # 한국(south korea 등)은 빨간색, 나머지는 회색빛 파란색으로 색상 지정
    colors = ['#E74C3C' if 'korea' in str(c) else '#34495E' for c in df_top20['country']]
    fig_bar = px.bar(df_top20, x='country', y=alc_col, title=f"알코올 소비량 상위 20개국 (대한민국은 빨간색 🔴)")
    fig_bar.update_traces(marker_color=colors)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("---")

    # 6. 그래프 ③ & ④: 알코올 소비량 vs 행복지수 산점도 🎯
    st.header("🎯 3. 알코올 소비량과 행복지수의 관계")
    df_merged = pd.merge(df_alc_filtered, df_hap_filtered, on='country', how='inner')

    if not df_merged.empty:
        # 한국 강조용 컬럼 만들기
        df_merged['구분'] = df_merged['country'].apply(lambda x: '대한민국 🔴' if 'korea' in str(x) else '다른 나라들 🔵')
        
        fig_scatter = px.scatter(
            df_merged, x=alc_col, y=hap_col, color='구분',
            color_discrete_map={'대한민국 🔴': '#E74C3C', '다른 나라들 🔵': '#AED6
