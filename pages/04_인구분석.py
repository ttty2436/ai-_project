import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 페이지 설정
st.set_page_config(
    page_title='Population Dashboard',
    layout='wide'
)

# 2. 타이틀 구역 (특수문자 및 이모지 완전 제거)
st.title('주민등록 인구 통계 대시보드')
st.markdown('다크모드 화면에 최적화된 지역별 인구 분석 페이지입니다.')
st.markdown('---')

# 기본 파일 설정
DEFAULT_FILE = '202604_202604_주민등록인구및세대현황_월간.csv'
df_source = None

# 3. 데이터 로딩 구역
if os.path.exists(DEFAULT_FILE):
    try:
        df_source = pd.read_csv(DEFAULT_FILE, encoding='utf-8')
    except:
        df_source = pd.read_csv(DEFAULT_FILE, encoding='cp949')
else:
    st.subheader('STEP 1. CSV 파일 업로드')
    uploaded_file = st.file_uploader('인구현황 CSV 파일을 업로드해 주세요.', type=['csv'])
    if uploaded_file is not None:
        try:
            df_source = pd.read_csv(uploaded_file, encoding='utf-8')
        except:
            uploaded_file.seek(0)
            df_source = pd.read_csv(uploaded_file, encoding='cp949')

# 4. 데이터 전처리 및 시각화
if df_source is not None:
    df = df_source.copy()
    df.columns = df.columns.str.strip()
    
    # 변환할 컬럼 지정
    target_cols = ['2026년04월_총인구수', '2026년04월_세대수', '2026년04월_남자 인구수', '2026년04월_여자 인구수', '2026년04월_세대당 인구', '2026년04월_남여 비율']
    
    for col in target_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # 전국 데이터와 지역 데이터 분리
    df_total = df[df['행정구역'].str.contains('전국', na=False)]
    df_regions = df[~df['행정구역'].str.contains('전국', na=False)].copy()
    df_regions['지역명'] = df_regions['행정구역'].apply(lambda x: x.split('(')[0].strip())

    # 5. 메트릭 요약 스냅샷 (안전한 format 함수 사용)
    if not df_total.empty:
        st.markdown('### 대한민국 요약 현황')
        c1, c2, c3, c4 = st.columns(4)
        
        val1 = '{:,}'.format(int(df_total['2026년04월_총인구수'].values[0]))
        val2 = '{:,}'.format(int(df_total['2026년04월_세대수'].values[0]))
        val3 = '{:.2f}명'.format(df_total['2026년04월_세대당 인구'].values[0])
        val4 = '{:.2f}'.format(df_total['2026년04월_남여 비율'].values[0])
        
        c1.metric(label='총 인구수 (명)', value=val1)
        c2.metric(label='총 세대수 (가구)', value=val2)
        c3.metric(label='세대당 인구수', value=val3)
        c4.metric(label='남여 비율', value=val4)
        
    st.markdown('---')
    
    # 6. 라디오 버튼 메뉴 구성
    st.markdown('### STEP 2. 데이터 그래프 분석')
    topic = st.radio(
        '조회할 지표를 선택하세요:',
