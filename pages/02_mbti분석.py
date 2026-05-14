import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="Global MBTI Visualizer", layout="wide")

st.title("🌏 국가별 MBTI 분포 데이터 시각화")
st.info("좌측 사이드바에 'countriesMBTI_16types.csv' 파일을 업로드하거나 프로젝트 폴더에 넣어주세요.")

# 데이터 로드 함수
@st.cache_data
def load_data(file_path):
    try:
        # 데이터 로드 시 인덱스나 공백 문제 방지
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"데이터를 읽는 중 오류가 발생했습니다: {e}")
        return None

# 1. 파일 업로드 로직 (사이드바)
uploaded_file = st.sidebar.file_uploader("CSV 파일을 업로드하세요", type=['csv'])

# 만약 업로드된 파일이 없으면 기존 경로에서 시도
df = None
if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    try:
        df = load_data('countriesMBTI_16types.csv')
    except:
        st.warning("현재 업로드된 파일이 없습니다. 왼쪽에서 파일을 올려주세요.")

if df is not None:
    # 국가 선택
    countries = df['Country'].unique()
    selected_country = st.sidebar.selectbox("조회할 국가를 선택하세요", countries)

    # 데이터 정리
    # 'Country' 열을 제외한 수치 데이터만 추출 및 정렬
    row = df[df['Country'] == selected_country].drop(columns=['Country'])
    country_series = row.iloc[0].sort_values(ascending=False)
    
    # 그래프 데이터 준비
    mbti_types = country_series.index.tolist()
    proportions = country_series.values.tolist()

    # 색상 설정 (1등 핑크, 나머지 파란색 파스텔 그라데이션)
    # n=16 (MBTI 유형 수)
    colors = []
    for i in range(len(mbti_types)):
        if i == 0:
            colors.append('#FFB6C1')  # 1등: 핑크 (Light Pink)
        else:
            # 점진적으로 연해지는 파란색 파스텔 (H:200, S:50~20, L:70~90)
            # 순위가 뒤로 갈수록 더 연한 파란색이 됨
            lightness = 70 + (i * 1.5)
            colors.append(f'hsl(200, 60%, {min(lightness, 95)}%)')

    # 플로틀리 차트 생성
    fig = go.Figure(go.Bar(
        x=mbti_types,
        y=proportions,
        marker_color=colors,
        text=[f'{p:.2%}' for p in proportions],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>{selected_country}</b>의 MBTI 분포 (상위 유형 강조)",
            font=dict(size=20)
        ),
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        yaxis=dict(tickformat='.1%'),
        template="plotly_white",
        height=600,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # 차트 출력
    st.plotly_chart(fig, use_container_width=True)

    # 하단 데이터 테이블
    st.subheader(f"📊 {selected_country} 상세 수치")
    st.dataframe(pd.DataFrame(country_series).T.style.format("{:.2%}"))

else:
    st.stop() # 데이터가 없으면 진행 중단
