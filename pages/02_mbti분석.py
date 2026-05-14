import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 페이지 설정
st.set_page_config(page_title="Global MBTI Statistics", layout="wide")

st.title("📊 국가별 MBTI 분포 시각화")

# 데이터 로드 (경로 에러 방지)
@st.cache_data
def load_data():
    file_name = 'countriesMBTI_16types.csv'
    # 파일이 현재 폴더 혹은 상위 폴더에 있는지 확인
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    elif os.path.exists(f"pages/{file_name}"):
        return pd.read_csv(f"pages/{file_name}")
    else:
        return None

df = load_data()

if df is not None:
    # 사이드바 국가 선택
    countries = sorted(df['Country'].unique())
    selected_country = st.sidebar.selectbox("분석할 국가를 선택하세요", countries)

    # 데이터 추출 및 정렬 (비율 높은 순)
    country_data = df[df['Country'] == selected_country].drop(columns=['Country']).iloc[0]
    country_data = country_data.sort_values(ascending=False)

    mbti_types = country_series.index.tolist()
    values = country_series.values.tolist()

    # 색상 로직: 1등은 핑크, 나머지는 파란색 파스텔 그라데이션
    colors = []
    for i in range(len(mbti_types)):
        if i == 0:
            colors.append('#FFB6C1')  # 1등: 라이트 핑크
        else:
            # 순위가 뒤로 갈수록 점점 더 연해지는 파스텔 블루 (HSL 방식)
            lightness = 65 + (i * 1.8) # 65%에서 시작해서 점점 밝아짐
            colors.append(f'hsl(210, 80%, {min(lightness, 95)}%)')

    # Plotly 인터렉티브 차트 생성
    fig = go.Figure(go.Bar(
        x=mbti_types,
        y=values,
        marker_color=colors,
        text=[f'{v:.2%}' for v in values],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text=f"<b>{selected_country}</b>의 MBTI 유형 분포", font=dict(size=22)),
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        yaxis=dict(tickformat='.1%'),
        template="plotly_white",
        height=600,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)

    # 데이터 표 출력
    with st.expander("상
