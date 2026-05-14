import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 페이지 설정
st.set_page_config(page_title="MBTI Analysis", layout="wide")

st.title("🌏 국가별 MBTI 분포 분석")

# 데이터 로드 함수
@st.cache_data
def load_data():
    # 파일명 정의 (정확하게 일치해야 함)
    file_name = 'countriesMBTI_16types.csv'
    
    # 여러 경로에서 파일 찾기 시도
    paths = [
        file_name,
        os.path.join("pages", file_name),
        os.path.join("..", file_name)
    ]
    
    for p in paths:
        if os.path.exists(p):
            return pd.read_csv(p)
    return None

df = load_data()

if df is not None:
    # 1. 국가 선택 (사이드바)
    countries = sorted(df['Country'].unique())
    selected_country = st.sidebar.selectbox("국가를 선택하세요", countries)

    # 2. 데이터 추출 및 정렬
    # 선택한 국가의 행만 가져와서 Country 컬럼 제외 후 내림차순 정렬
    target_row = df[df['Country'] == selected_country].drop(columns=['Country']).iloc[0]
    sorted_data = target_row.sort_values(ascending=False)

    mbti_types = sorted_data.index.tolist()
    proportions = sorted_data.values.tolist()

    # 3. 색상 설정 (1등 핑크, 나머지 파란색 파스텔 그라데이션)
    colors = []
    for i in range(len(mbti_types)):
        if i == 0:
            colors.append('#FFB6C1')  # 1등: 핑크
        else:
            # 순위가 낮아질수록 더 연해지는 파스텔 블루
            # HSL: 210(파랑), 70%(채도), L(명도)를 조정
            lightness = 65 + (i * 2)
            colors.append(f'hsl(210, 70%, {min(lightness, 95)}%)')

    # 4. Plotly 차트 생성
    fig = go.Figure(go.Bar(
        x=mbti_types,
        y=proportions,
        marker_color=colors,
        text=[f'{p:.1%}' for p in proportions],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>'
    ))

    fig.update_layout(
        title=f"<b>{selected_country}</b> MBTI 유형별 비율 (상위순)",
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        yaxis=dict(tickformat='.0%'),
        template="plotly_white",
        height=550,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # 차트 출력
    st.plotly_chart(fig, use_container_width=True)

    # 데이터 표 출력
    with st.expander("원본 데이터 보기"):
        st.dataframe(pd.DataFrame(sorted_data).T.style.format("{:.2%}"))

else:
    st.error("데이터 파일('countriesMBTI_16types.csv')을 찾을 수 없습니다. 파일 이름을 확인하거나 GitHub 최상위 폴더에 파일을 업로드해 주세요.")
