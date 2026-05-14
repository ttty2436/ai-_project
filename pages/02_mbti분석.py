import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 페이지 설정
st.set_page_config(page_title="MBTI Dashboard", layout="wide")

st.title("🌏 국가별 MBTI 분포 분석")

# 데이터 로드 함수 (오류 방지를 위한 다중 경로 탐색)
@st.cache_data
def load_data():
    file_name = 'countriesMBTI_16types.csv'
    # 1. 현재 폴더 2. pages 폴더 3. 상위 폴더 순서로 탐색
    paths = [file_name, os.path.join("pages", file_name), os.path.join("..", file_name)]
    
    for p in paths:
        if os.path.exists(p):
            try:
                return pd.read_csv(p)
            except Exception:
                continue
    return None

df = load_data()

if df is not None:
    # 사이드바 국가 선택
    countries = sorted(df['Country'].unique())
    selected_country = st.sidebar.selectbox("조회할 국가 선택", countries)

    # 데이터 가공
    # 선택된 국가 행 추출 후 'Country' 열 제외, 수치 내림차순 정렬
    target_data = df[df['Country'] == selected_country].drop(columns=['Country']).iloc[0]
    sorted_df = target_data.sort_values(ascending=False)

    mbti_labels = sorted_df.index.tolist()
    mbti_values = sorted_df.values.tolist()

    # 색상 설정 (1등 핑크, 나머지 파스텔 블루 그라데이션)
    bar_colors = []
    for i in range(len(mbti_labels)):
        if i == 0:
            bar_colors.append('#FFB6C1')  # 1위: 라이트 핑크
        else:
            # 뒤로 갈수록 점점 연해지는 파스텔 파란색
            # H:210, S:60%, L:60%~90%로 변화
            lightness = 60 + (i * 2.2)
            bar_colors.append(f'hsl(210, 60%, {min(lightness, 95)}%)')

    # Plotly 막대 그래프 생성
    fig = go.Figure(go.Bar(
        x=mbti_labels,
        y=mbti_values,
        marker_color=bar_colors,
        text=[f'{v:.1%}' for v in mbti_values],
        textposition='outside',
        hovertemplate='<b>%{x}</b>: %{y:.2%}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(text=f"<b>{selected_country}</b> MBTI 유형별 비중 (상위순)", font=dict(size=20)),
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        yaxis=dict(tickformat='.0%'),
        template="plotly_white",
        height=600
    )

    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 하단 데이터 표
    with st.expander("원본 데이터 테이블 보기"):
        st.dataframe(pd.DataFrame(sorted_df).T.style.format("{:.2%}"))

else:
    # 파일이 없을 경우 업로드 가이드 표시
    st.error("파일('countriesMBTI_16types.csv')을 찾을 수 없습니다.")
    st.info("해결 방법: GitHub 리포지토리의 최상위 폴더(Root)에 해당 CSV 파일을 업로드해 주세요.")
    
    # 임시 파일 업로더 (사용자가 직접 올릴 수도 있게 함)
    uploaded_file = st.file_uploader("또는 여기에서 직접 CSV 파일을 업로드하세요", type=['csv'])
    if uploaded_file:
        df_uploaded = pd.read_csv(uploaded_file)
        st.success("파일이 성공적으로 로드되었습니다! 페이지를 새로고침하거나 유지하세요.")
        # 이후 로직 진행 가능하도록 구성
