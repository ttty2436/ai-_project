import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 🎀 1. 상큼키치 공주풍 페이지 세팅
st.set_page_config(
    page_title="Kitsch Population Studio", 
    page_icon="🔮",
    layout="wide"
)

# 🎨 2. SyntaxError 완벽 방어형 스타일 주입 (st.html 사용으로 파이썬 매직 실수를 원천 차단!)
st.html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    .title-txt {
        color: #ff3377 !important;
        font-family: 'Jua', sans-serif;
        font-size: 45px !important;
        text-shadow: 3px 3px 0px #ffcc00;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-txt {
        color: #4ea8de !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 25px;
    }
    .stMetric {
        border: 3px solid #ffb7c5 !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 5px 5px 0px #ffb7c5 !important;
    }
</style>
""")

# 💕 타이틀 구역
st.markdown("<div class='title-txt'>💖 Kitsch 인구 하이라이트 🧃 💖</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-txt'>(｡♥‿♥｡) 다크모드에서도 눈부신 키치 비주얼 오픈! ✧*｡</div>", unsafe_allow_html=True)
st.markdown("---")

# 기본 파일명 설정
DEFAULT_FILE = "202604_202604_주민등록인구및세대현황_월간.csv"
df_source = None

# 깃허브 자동 로드 검사
if os.path.exists(DEFAULT_FILE):
    try:
        df_source = pd.read_csv(DEFAULT_FILE, encoding='utf-8')
    except Exception:
        df_source = pd.read_csv(DEFAULT_FILE, encoding='cp949')
    st.success("✨ 데이터를 자동으로 불러왔어요! 편리하죠? 😎")
else:
    st.subheader("🧁 STEP 1. 다운받은 CSV 파일을 먹여주세요! ✨")
    uploaded_file = st.file_uploader(
        "여기에 인구현황 CSV 파일을 요정처럼 쏙 던져주세요 🧚", 
        type=["csv"]
    )
    if uploaded_file is not None:
        try:
            df_source = pd.read_csv(uploaded_file, encoding='utf-8')
        except Exception:
            uploaded_file.seek(0)
            df_source = pd.read_csv(uploaded_file, encoding='cp949')

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

    # 4. 하이틴 스냅샷 보드
    if not df_total.empty:
        st.markdown("### 🏹 Today's 대한민국 스냅샷 (*ˊᗜˋ*) ✨")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric(label="🧸 총 인구수 (명)", value=f"{int(df_total['2026년04월_총인구수'].values[0]):,}")
        with c2:
            st.metric(label="🍰 총 세대수 (가구)", value=f"{int(df_total['2026년04월_세대수'].values[0]):,}")
        with c3:
            st.metric(label="🍡 오순도순 세대당 인구", value=f"{df_total['2026년04월_세대당 인구'].values[0]:.2f}명")
        with c4:
            st.metric(label="🦄 황금 남녀 비율", value=f"{df_total['2026년04월_남여 비율'].values[0]:.2f}")
    
    st.markdown("---")

    # 5. 오늘의 팝 비주얼 그래프 구역 ⚡
    st.markdown("### 🌈 STEP 2. 톡톡 튀는 비주얼 그래프 타임 🎡")
    
    topic = st.radio(
        "어떤 깜찍한 트렌드를 훔쳐볼까요? 👀",
