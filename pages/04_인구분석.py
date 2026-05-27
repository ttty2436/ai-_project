import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="인구 분석 통계", layout="wide")

st.title("주민등록 인구 통계 대시보드")
st.markdown("---")

DEFAULT_FILE = "202604_202604_주민등록인구및세대현황_월간.csv"
df_source = None

if os.path.exists(DEFAULT_FILE):
    try:
        df_source = pd.read_csv(DEFAULT_FILE, encoding="utf-8")
    except:
        df_source = pd.read_csv(DEFAULT_FILE, encoding="cp949")
else:
    st.subheader("파일 업로드")
    uploaded_file = st.file_uploader("인구현황 CSV 파일을 업로드해주세요.", type=["csv"])
    if uploaded_file is not None:
        try:
            df_source = pd.read_csv(uploaded_file, encoding="utf-8")
        except:
            uploaded_file.seek(0)
            df_source = pd.read_csv(uploaded_file, encoding="cp949")

if df_source is not None:
    df = df_source.copy()
    df.columns = df.columns.str.strip()
    
    target_cols = [
        "2026년04월_총인구수", "2026년04월_세대수", 
        "2026년04월_남자 인구수", "2026년04월_여자 인구수", 
        "2026년04월_세대당 인구", "2026년04월_남여 비율"
    ]
    
    for col in target_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", "").str.strip()
            df[col] = pd.to_numeric(df[col], errors="coerce")
            
    df_total = df[df["행정구역"].str.contains("전국", na=False)]
    df_regions = df[~df["행정구역"].str.contains("전국", na=False)].copy()
    df_regions["지역명"] = df_regions["행정구역"].apply(lambda x: x.split("(")[0].strip())

    if not df_total.empty:
        st.subheader("전국 현황")
        c1, c2, c3, c4 = st.columns(4)
        
        val1 = "{:,}".format(int(df_total["2026년04월_총인구수"].values[0]))
        val2 = "{:,}".format(int(df_total["2026년04월_세대수"].values[0]))
        val3 = "{:.2f}명".format(df_total["2026년04월_세대당 인구"].values[0])
        val4 = "{:.2f}".format(df_total["2026년04월_남여 비율"].values[0])
        
        c1.metric(label="총 인구수", value=val1)
        c2.metric(label="총 세대수", value=val2)
        c3.metric(label="세대당 인구", value=val3)
        c4.metric(label="남여 비율", value=val4)
        
    st.markdown("---")
    
    st.subheader("그래프 시각화")
    topic = st.radio(
        "지표 선택",
        ["총인구수", "세대수", "남녀 인구 비교"],
        horizontal=True
    )
    
    if topic == "총인구수":
        fig = px.bar(
            df_regions, x="지역명", y="2026년04월_총인구수",
            title="지역별 총 인구수",
            template="plotly_dark"
        )
    elif topic == "세대수":
        fig = px.bar(
            df_regions, x="지역명", y="2026년04월_세대수",
            title="지역별 총 세대수",
            template="plotly_dark"
        )
    elif topic == "남녀 인구 비교":
        df_melted = pd.melt(
            df_regions, id_vars=["지역명"],
            value_vars=["2026년04월_남자 인구수", "2026년04월_여자 인구수"],
            var_name="성별", value_name="인구수"
        )
        df_melted["성별"] = df_melted["성별"].str.replace("2026년04월_", "")
        
        fig = px.bar(
            df_melted, x="지역명", y="인구수", color="성별",
            title="지역별 남녀 인구 분포 (나란히 보기)",
            barmode="group",
            template="plotly_dark"
        )
        
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("상세 데이터")
    
    chosen = st.multiselect("조회할 지역 선택 (미선택 시 전체 조회)", df_regions["지역명"].unique())
    final_df = df_regions[df_regions["지역명"].isin(chosen)] if chosen else df_regions
    
    st.dataframe(
        final_df
