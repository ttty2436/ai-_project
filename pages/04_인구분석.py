import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. 페이지 설정
st.set_page_config(
    page_title='Kitsch Studio',
    page_icon='🔮',
    layout='wide'
)

# 2. 타이틀 구역
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

    # 5. 메트릭 대시보드 스냅샷 (★ 파이썬 3.14 에러 주범인 f-string 중괄호 포맷팅 완전 박멸 ★)
    if not df_total.empty:
        st.markdown('### 🏹 Today 대한민국 스냅샷 (*ˊᗜˋ*) ✨')
        c1, c2, c3, c4 = st.columns(4)
        
        # 문법 충돌을 피하기 위해 안전한 format() 구조로 완전 변경
        val1 = '{:,}'.format(int(df_total['2026년04월_총인구수'].values[0]))
        val2 = '{:,}'.format(int(df_total['2026년04월_세대수'].values[0]))
        val3 = '{:.2f}명'.format(df_total['2026년04월_세대당 인구'].values[0])
        val4 = '{:.2f}'.format(df_total['2026년04월_남여 비율'].values[0])
        
        c1.metric(label='🧸 총 인구수 (명)', value=val1)
        c2.metric(label='🍰 총 세대수 (가구)', value=val2)
        c3.metric(label='🍡 세대당 인구수', value=val3)
        c4.metric(label='🦄 남여 성별 비율', value=val4)
        
    st.markdown('---')
    
    # 6. 라디오 버튼 메뉴 구성
    st.markdown('### 🌈 STEP 2. 톡톡 튀는 비주얼 그래프 타임 🎡')
    topic = st.radio(
        '어떤 깜찍한 트렌드를 훔쳐볼까요? 👀',
        ['🍭 총인구수 트렌드', '🔮 세대수 트렌드', '🍟 남녀 인구 밸런스'],
        horizontal=True
    )
    
    # 키치 컬러 코드 선언
    kitsch_pink = '#ff007f'
    kitsch_purple = '#9b5de5'
    kitsch_blue = '#00bbf9'
    
    # 다크모드 완벽 호환 템플릿
    theme_setting = 'plotly_dark'
    
    if topic == '🍭 총인구수 트렌드':
        fig = px.bar(
            df_regions, x='지역명', y='2026년04월_총인구수',
            title='지역별 총 인구수 현황',
            color_discrete_sequence=[kitsch_pink],
            template=theme_setting
        )
    elif topic == '🔮 세대수 트렌드':
        fig = px.bar(
            df_regions, x='지역명', y='2026년04월_세대수',
            title='지역별 총 세대수 현황',
            color_discrete_sequence=[kitsch_purple],
            template=theme_setting
        )
    elif topic == '🍟 남녀 인구 밸런스':
        df_melted = pd.melt(
            df_regions, id_vars=['지역명'],
            value_vars=['2026년04월_남자 인구수', '2026년04월_여자 인구수'],
            var_name='성별', value_name='인구수'
        )
        df_melted['성별'] = df_melted['성별'].str.replace('2026년04월_', '')
        
        # barmode='group'으로 남녀 차트가 절대 겹치지 않게 가로 배치!
        fig = px.bar(
            df_melted, x='지역명', y='인구수', color='성별',
            title='소다보이 vs 피치걸 남녀 인구 밸런스',
            barmode='group',
            color_discrete_map={'남자 인구수': kitsch_blue, '여자 인구수': kitsch_pink},
            template=theme_setting
        )
        
    # 그래프 스타일 다듬기
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(size=12, bold=True)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 7. 필터링 구역
    st.markdown('---')
    st.markdown('### 💎 STEP 3. 갖고 싶은 지역만 요정 초이스 🧚‍♀️')
    
    chosen = st.multiselect('원하는 지역만 선택해 주세요 (비워두면 전체 조회):', df_regions['지역명'].unique())
    final_df = df_regions[df_regions['지역명'].isin(chosen)] if chosen else df_regions
    
    st.dataframe(
        final_df[['지역명', '2026년04월_총인구수', '2026년04월_세대수', '2026년04월_세대당 인구', '2026년04월_남자 인구수', '2026년04월_여자 인구수']],
        use
