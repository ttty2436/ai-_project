import streamlit as st
import pandas as pd
import plotly.express as px

# 🎀 1. 상큼키치 공주풍 페이지 세팅
st.set_page_config(
    page_title="🍭키치발랄 인구 스튜디오🍭", 
    page_icon="🔮",
    layout="wide"
)

# 🎨 2. 하이틴 하이라이트 키치 CSS 스타일링
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    
    .main { background-color: #fff9fb; } /* 베이비 핑크빛 크림 배경 */
    
    /* 타이틀 감성 */
    .title-txt {
        color: #ff3377 !important;
        font-family: 'Jua', sans-serif;
        font-size: 45px !important;
        text-shadow: 3px 3px 0px #ffcc00;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .sub-txt {
        color: #4ea8de;
        font-weight: bold;
        text-align: center;
        margin-bottom: 25px;
    }

    /* 상큼 발랄 반짝이는 메트릭 카드 */
    .stMetric {
        background: #ffffff !important;
        border: 3px solid #ffb7c5 !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 5px 5px 0px #ffb7c5 !important;
        transition: transform 0.2s;
    }
    .stMetric:hover {
        transform: scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

# 💕 타이틀 구역
st.markdown("<div class='title-txt'>💖 𝓚𝓲𝓽𝓼𝓬𝓱 인구 하이라이트 🧃 💖</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-txt'>(｡♥‿♥｡) 칙칙한 숫자는 𝓝𝓞! 우리 동네 인구수 상콤하게 체킷-! ✧*｡</div>", unsafe_allow_html=True)
st.markdown("---")

# 📥 3. 스트림릿 클라우드 전용 상큼 업로더
st.subheader("🧁 STEP 1. 다운받은 CSV 파일을 먹여주세요! ✨")
uploaded_file = st.file_uploader(
    "여기에 인구현황 CSV 파일을 요정처럼 쏙- 던져주세요 🧚", 
    type=["csv"]
)

if uploaded_file is not None:
    # 데이터 로드 (인코딩 자동 방어벽 💖)
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except Exception:
        df = pd.read_csv(uploaded_file, encoding='cp949')

    # 공백 털어내기 명수링 🧹
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

    # 전국 vs 지역 쪼개기 🔪✨
    df_total = df[df['행정구역'].str.contains('전국', na=False)]
    df_regions = df[~df['행정구역'].str.contains('전국', na=False)].copy()
    df_regions['지역명'] = df_regions['행정구역'].apply(lambda x: x.split('(')[0].strip())

    # 4. 하이틴 스냅샷 보드 (대문짝만하게!)
    if not df_total.empty:
        st.markdown("### 🏹 𝓣𝓸𝓭𝓪𝔂'𝓼 대한민국 스냅샷 (*ˊᗜˋ*) ✨")
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

    # 5. 오늘의 팝(Pop!) 크러시 꺾은선 그래프 구역 ⚡
    st.markdown("### 🌈 STEP 2. 톡톡 튀는 비주얼 그래프 타임 🎡")
    
    topic = st.radio(
        "어떤 깜찍한 트렌드를 꺾은선으로 훔쳐볼까요? 👀",
        ["🍭 영차영차 총인구수", "🔮 하트시그널 세대수", "🍟 체리블라썸 남녀 밸런스"],
        horizontal=True
    )

    # 파스텔 & 네온 키치 컬러 패키지 정의 🎨
    kitsch_pink = "#ff007f"   # 핫체리핑크
    kitsch_mint = "#00f5d4"   # 네온민트
    kitsch_purple = "#9b5de5" # 하이틴퍼플
    kitsch_blue = "#00bbf9"   # 소다블루

    if topic == "🍭 영차영차 총인구수":
        fig = px.line(df_regions, x='지역명', y='2026년04월_총인구수', 
                      title="📈 [체리픽] 울트라 인구수 트렌드 라인 ✧*｡", 
                      markers=True)
        fig.update_traces(
            line=dict(color=kitsch_pink, width=5), 
            marker=dict(size=12, color='#ffffff', line=dict(width=3, color=kitsch_pink))
        )
        
    elif topic == "🔮 하트시그널 세대수":
        fig = px.line(df_regions, x='지역명', y='2026년04월_세대수', 
                      title="💎 [반짝] 블링블링 세대수 트렌드 라인 ✧*｡", 
                      markers=True)
        fig.update_traces(
            line=dict(color=kitsch_purple, width=5), 
            marker=dict(size=12, color='#ffffff', line=dict(width=3, color=kitsch_purple))
        )
        
    elif topic == "🍟 체리블라썸 남녀 밸런스":
        df_melted = pd.melt(df_regions, id_vars=['지역명'], 
                            value_vars=['2026년04월_남자 인구수', '2026년04월_여자 인구수'],
                            var_name='성별', value_name='인구수')
        df_melted['성별'] = df_melted['성별'].str.replace('2026년04월_', '')
        
        fig = px.line(df_melted, x='지역명', y='인구수', color='성별', 
                      title="🍿 [매칭] 소다보이 vs 피치걸 인구 크로스! ✧*｡", 
                      markers=True,
                      color_discrete_map={'남자 인구수': kitsch_blue, '여자 인구수': kitsch_pink})
        fig.update_traces(line=dict(width=4), marker=dict(size=10))

    # 그래프 뒷배경도 투명하고 힙하게 세팅 바이브 조정 🎧
    fig.update_layout(
        plot_bgcolor='rgba(255, 249, 251, 0.5)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='#ffe3ed', tickfont=dict(size=12, bold=True)),
        yaxis=dict(showgrid=True, gridcolor='#ffe3ed'),
        font=dict(size=13)
    )
    st.plotly_chart(fig, use_container_width=True)

    # 6. 비밀 옷장 데이터 필터
    st.markdown("---")
    st.markdown("### 💎 STEP 3. 갖고 싶은 지역만 요정 초이스 🧚‍♀️")
    
    chosen = st.multiselect("원하는 지역만 픽미픽미업! (텅 비워두면 전국 올패스!):", df_regions['지역명'].unique())
    
    final_df = df_regions[df_regions['지역명'].isin(chosen)] if chosen else df_regions
    
    st.dataframe(
        final_df[['지역명', '2026년04월_총인구수', '2026년04월_세대수', '2026년04월_세대당 인구', '2026년04월_남자 인구수', '2026년04월_여자 인구수']], 
        use_container_width=True
    )
    st.balloons() # 파일 업로드 성공 기념 풍선 팡팡🎈

else:
    # 파일 안올렸을 때 뜨는 귀여운 대기화면 🦄
    st.info("💡 아기 요정님! 상단의 업로드 박스에 CSV 파일을 쏙 넣어주시면 마법 대시보드가 열려요! (기다리는 중... ⏱️✨)")
