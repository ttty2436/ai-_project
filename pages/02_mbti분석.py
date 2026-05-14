import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="Global MBTI Explorer", layout="wide")

st.title("🌏 국가별 MBTI 분포 시각화")
st.write("국가를 선택하면 해당 국가의 MBTI 비율을 확인할 수 있습니다.")

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

df = load_data()

# 사이드바에서 국가 선택
countries = df['Country'].unique()
selected_country = st.sidebar.selectbox("국가를 선택하세요", countries)

# 선택된 국가 데이터 추출
country_df = df[df['Country'] == selected_country].iloc[:, 1:].T
country_df.columns = ['Proportion']
country_df = country_df.sort_values(by='Proportion', ascending=False)

# 색상 설정 (1등은 핑크, 나머지는 파란색 파스텔 그라데이션)
n_types = len(country_df)
colors = []
for i in range(n_types):
    if i == 0:
        colors.append('#FFB6C1')  # Light Pink (1등)
    else:
        # 파란색 계열 파스텔 그라데이션 (진한 파스텔 -> 연한 파스텔)
        blue_val = 200 + (i * 3) # 점점 연해지도록 설정
        colors.append(f'rgb(135, 206, {min(blue_val, 255)})')

# 플로틀리 차트 생성
fig = go.Figure(go.Bar(
    x=country_df.index,
    y=country_df['Proportion'],
    marker_color=colors,
    text=country_df['Proportion'].apply(lambda x: f'{x:.2%}'),
    textposition='auto',
    hovertemplate='MBTI: %{x}<br>비율: %{y:.2%}<extra></extra>'
))

fig.update_layout(
    title=f"<b>{selected_country}</b>의 MBTI 유형별 비율",
    xaxis_title="MBTI Type",
    yaxis_title="Proportion",
    template="plotly_white",
    height=500,
    showlegend=False
)

# 스트림릿에 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 상세 데이터 표
with st.expander("데이터 자세히 보기"):
    st.dataframe(country_df.style.format("{:.2%}"))
