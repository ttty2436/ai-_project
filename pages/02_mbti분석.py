import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 페이지 설정
st.set_index = False # 멀티페이지일 경우 생략 가능

st.title("🌏 국가별 MBTI 분포")

# 데이터 파일 경로 설정 (상위 폴더나 현재 폴더에서 csv 찾기)
def find_data_file(filename):
    # 현재 파일 위치 기준 상위 폴더까지 탐색
    search_paths = [filename, f"../{filename}", f"pages/{filename}"]
    for path in search_paths:
        if os.path.exists(path):
            return path
    return None

data_path = find_data_file('countriesMBTI_16types.csv')

if data_path:
    df = pd.read_csv(data_path)
    
    # 국가 선택
    countries = df['Country'].unique()
    selected_country = st.selectbox("국가를 선택하세요", countries)

    # 데이터 추출 및 정렬
    row = df[df['Country'] == selected_country].drop(columns=['Country'])
    country_series = row.iloc[0].sort_values(ascending=False)
    
    mbti_types = country_series.index.tolist()
    proportions = country_series.values.tolist()

    # 핑크 & 파란색 파스텔 그라데이션 설정
    colors = ['#FFB6C1'] + [f'hsl(200, 70%, {70 + (i * 1.5)}%)' for i in range(1, len(mbti_types))]

    # 플로틀리 차트
    fig = go.Figure(go.Bar(
        x=mbti_types,
        y=proportions,
        marker_color=colors,
        text=[f'{p:.1%}' for p in proportions],
        textposition='auto',
    ))

    fig.update_layout(
        title=f"<b>{selected_country}</b> MBTI 비율",
        template="plotly_white",
        yaxis=dict(tickformat='.0%')
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("csv 파일을 찾을 수 없습니다. 파일명을 확인해 주세요.")
