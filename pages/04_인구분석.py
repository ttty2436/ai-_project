import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 페이지 세팅 (가장 표준적인 문자열만 사용)
st.set_page_config(
    page_title='Kitsch Studio',
    page_icon='🔮',
    layout='wide'
)

# 2. 타이틀 구역 (매직 파서가 오독할 수 있는 멀티라인 이중 따옴표 전면 제거)
st.markdown('# 💖 Kitsch 인구 하이라이트 🧃 💖')
st.markdown('### (｡♥‿♥｡) 다크모드에서도 눈부신 키치 비주얼 오픈! ✧*｡')
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
    st.subheader('🧁 STEP 1. CSV 파일을 올려주세요!')
    uploaded_file = st.file_uploader('인구현황 CSV 파일을 여기에 던져주세요 🧚', type=['csv'])
    if uploaded_file is not None:
        try:
            df_source = pd.read_csv(uploaded_file, encoding='utf-8')
        except:
            uploaded_file.seek(0)
            df_source = pd.read_csv(uploaded_file, encoding='cp949')

# 4. 데이터 정제 및 시각화 작동
if df_source is not None:
    df = df_source.copy()
    df.columns = df.columns.str.strip()
    
    # 변환할 컬럼 리스트 명시
    target_cols = ['2026년04월_총인구수', '2026년04월_세대수', '2026년04월_남자 인구수', '2026년04월_여자 인구수', '2026년04월_세대당 인구', '2026년04월_남여 비율']
    
    for col in target_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # 전국 데이터와 지역 데이터 분리
    df_total = df[df['행정구역'].str.contains('전국', na=False)]
    df_regions = df[~df['행정구역'].str.contains('전국', na=False)].copy()
    df_regions['지역명'] = df_regions['행정구역'].apply(lambda x: x.split('(')[0].strip())

    # 5. 상큼한 메트릭 대시보드 스냅샷
    if not df_total.empty:
        st.markdown('### 🏹 Today 대한민국 스냅샷 (*ˊᗜˋ*) ✨')
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(label='🧸 총 인구수 (명)', value=f"{int(df_total['2026년04월_총인구수'].values[0]):,}")
        c2.metric(label='🍰 총 세대수 (가구)', value=f"{int(df_total['2026년04월_세대수'].values[0]):,}")
        c3.metric(label='🍡 세대당 인구수', value=f"{df_total['2026년04월_세대당 인구'].values[0]:.2f}명")
        c4.metric(label='🦄 남여 성별 비율', value=f"{df
