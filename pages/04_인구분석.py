import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 페이지 세팅 (안전한 영문/한글 텍스트 구성)
st.set_page_config(
    page_title="Population Analysis Dashboard", 
    layout="wide"
)

# 2. 타이틀 및 헤더 (특수문자 및 이모지 전면 제거)
st.title("주민등록 인구 분석 하이라이트")
st.markdown("다크모드 환경에 최적화된 지역별 인구 통계 대시보드입니다.")
st.markdown("---")

# 기본 파일명 설정
DEFAULT_FILE = "202604_202604_주민등록인구및세대현황_월간.csv"
df_source = None

# 3. 데이터 자동 로드 검사
if os.path.exists(DEFAULT_FILE):
    try:
        df_source = pd.read_csv(DEFAULT_FILE, encoding='utf-8')
    except Exception:
        df_source = pd.read_csv(DEFAULT_FILE, encoding='cp949')
    st.success("데이터 파일을 자동으로 불러왔습니다.")
else:
    st.subheader("STEP 1. CSV 파일을 업로드해주세요.")
    uploaded_file = st.file_uploader(
        "주민등록인구및세대현황 CSV 파일을 선택해주세요.", 
        type=["csv"]
    )
    if uploaded_file is not None:
        try:
            df_source = pd.read_csv(uploaded_file, encoding='utf-8')
        except Exception:
            uploaded_file.seek(0)
            df_source = pd.read_csv(uploaded_file, encoding='cp949')

# 4. 데이터 전처리 및 시각화
if df_source is not None:
    df = df_source.copy()
    df.columns = df.columns.str.strip()
    
    cols_to_convert = [
        '2026년04월_총인구수', '2026년04월_세대수', 
        '2026년04월_남자 인구수', '2026년04월_여자 인구수', 
        '2026년04월_세대당 인구', '2026년04월_남여 비율'
    ]
    
    for col in cols_to_convert:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df_total = df[df['행정구역'].str.contains('전국', na=False)]
    df_regions = df[~df['행정구역'].str.contains('전국', na=False)].copy()
    df_regions['지역명'] = df_regions['행정구역'].apply(lambda x: x.split('(')[0].strip())

    # 5. 핵심 지표 요약
    if not df_total.empty:
        st.markdown("### 대한민국 요약 현황")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric(label="총 인구수 (명)", value=f"{int(df_total['2026년04월_총인구수'].values[0]):,}")
        with c2:
            st.metric(label="총 세대수 (가구)", value=f"{int(df_total['2026년04월_세대수'].values[0]):,}")
        with c3:
            st.metric(label="세대당 인구", value=f"{df_total['2026년04월_세대당 인구'].values[0]:.2f}명")
        with c4:
            st.metric(label="남여 비율", value=f"{df_total['2026년04월_남여 비율'].values[0]:.2f}")
    
    st.markdown("---")

    # 6. 그래프 선택 및 시각화 구역
    st.markdown("### STEP 2. 데이터 지표 선택")
    
    topic = st.radio(
        "분석할 지표를 선택하세요:",
        ["총인구수 현황", "세대수 현황", "남녀 인구 비율 밸런스"],
        horizontal=True
    )

    # 다크모드 유저를 위한 어두운 테마 강제 고정 (글씨 가독성 100% 보장)
    plotly_theme = "plotly_dark"

    if topic == "총인구수 현황":
        fig = px.bar(df_regions, x='지역명', y='2026년04월_총인구수', 
                     title="지역별 총 인구수 차트", 
                     color_discrete_sequence=["#ff007f"],
                     template=plotly_theme)
        
    elif topic == "세대수 현황":
        fig = px.bar(df_regions, x='지역명', y='2026년04월_세대수', 
                     title="지역별 세대수 차트", 
                     color_discrete_sequence=["#9b5de5"],
                     template=plotly_theme)
        
    elif topic == "남녀 인구 비율 밸런스":
        df_melted = pd.melt(df_regions, id_vars=['지역명'], 
                            value_vars=['2026년04월_남자 인구수', '2026년04월_여자 인구수'],
                            var_name='성별', value_name='인구수')
        df_melted['성별'] = df_melted['성별'].str.replace('2026년04월_', '')
        
        # barmode='group'으로 다크모드에서도 남자(블루) 여자(핑크) 안 겹치고 나란히 배치
        fig = px.bar(df_melted, x='지역명', y='인구수', color='성별', 
                     title="지역별 남녀 인구 구성 비교 (나란히 보기)", 
                     barmode='group',
                     color_discrete_map={'남자 인구수': '#00bbf9', '여자 인구수': '#ff007f'},
                     template=plotly_theme)

    # 배경 투명화 및 레이아웃 정리
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.1)', tickfont=dict(size=12, bold=True)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)

    # 7. 데이터 상세 선택 필터
    st.markdown("---")
    st.markdown("### STEP 3. 상세 데이터 조회")
    
    chosen = st.multiselect("조회할 특정 지역을 선택하세요 (비워두면 전체 지역 조회):", df_regions['지역명'].unique())
    
    final_df = df_regions[df_regions['지역명'].isin(chosen)] if chosen else df_regions
    
    st.dataframe(
        final_df
