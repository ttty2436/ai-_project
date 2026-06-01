import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 및 친근한 제목
st.set_page_config(page_title="알코올과 행복의 상관관계", layout="wide")

st.title("🍻 술을 많이 마시는 나라는 정말 더 행복할까?")
st.markdown("### 📊 **새로운 연도별 데이터셋으로 분석하는 인과관계**")
st.write("안녕하세요! 고등학교 데이터 분석 수행평가 대시보드에 오신 것을 환영합니다. 🎯")
st.markdown("---")

# 2. 데이터 불러오기
try:
    # 새로 제공해주신 연도별 알코올 데이터셋과 2024 행복지수 데이터셋 로드
    df_alc = pd.read_csv("alcohol-consumption.csv")
    df_hap = pd.read_csv("world-happiness-report-2024.csv")
    
    # 컬럼명 전처리 (대소문자 불일치 방지)
    df_alc.columns = df_alc.columns.str.strip().str.lower()
    df_hap.columns = df_hap.columns.str.strip().str.lower()
    
    # 국가 컬럼명 통일
    if "country name" in df_hap.columns:
        df_hap = df_hap.rename(columns={"country name": "country"})
    if "entity" in df_alc.columns: # Our World in Data 기반 데이터는 보통 country 대신 entity로 되어있음
        df_alc = df_alc.rename(columns={"entity": "country"})

    df_alc["country"] = df_alc["country"].str.strip().str.lower()
    df_hap["country"] = df_hap["country"].str.strip().str.lower()

    # 실제 데이터의 컬럼 찾기 (자동 인식)
    alc_year_col = "year" if "year" in df_alc.columns else ""
    hap_year_col = "year" if "year" in df_hap.columns else ""
    
    # 알코올 소비량 수치 컬럼 찾기
    alc_col = ""
    for col in df_alc.columns:
        if "consumption" in col or "total" in col or "liter" in col or "alcohol" in col:
            alc_col = col
            break
            
    # 행복지수 점수 컬럼 찾기
    hap_col = ""
    for col in df_hap.columns:
        if "score" in col or "happiness" in col or "ladder" in col:
            hap_col = col
            break

    # 3. 사이드바 연도 선택 (슬라이더 기능 구현 완료! ✨)
    st.sidebar.header("⚙️ 분석 조건 설정")
    common_years = sorted(list(set(df_alc[alc_year_col].unique()).intersection(set(df_hap[hap_year_col].unique()))))
    
    if len(common_years) > 0:
        selected_year = st.sidebar.slider("📅 어떤 연도의 데이터를 볼까요?", min_value=int(min(common_years)), max_value=int(max(common_years)), value=int(max(common_years)))
        df_alc_filtered = df_alc[df_alc[alc_year_col] == selected_year]
        df_hap_filtered = df_hap[df_hap[hap_year_col] == selected_year]
        st.sidebar.success(f"현재 {selected_year}년 데이터 반영 중!")
    else:
        # 공통 연도가 안 맞아도 분석이 깨지지 않게 최신 행복지수 연도 기준으로 자동 보정해주는 친절함!
        st.sidebar.warning("💡 연도가 완전히 일치하지 않아, 각 데이터의 최신 연도 기준으로 매칭합니다.")
        selected_year = 2024
        df_alc_filtered = df_alc[df_alc[alc_year_col] == df_alc[alc_year_col].max()]
        df_hap_filtered = df_hap[df_hap[hap_year_col] == df_hap[hap_year_col].max()]

    # 📈 1. 전 세계 알코올 소비량 추이 (꺾은선)
    st.header("📈 1. 전 세계 알코올 소비량은 어떻게 변했을까?")
    df_trend = df_alc.groupby(alc_year_col)[alc_col].mean().reset_index()
    fig_line = px.line(df_trend, x=alc_year_col, y=alc_col, title="연도별 전 세계 평균 알코올 소비량 변화 추이", markers=True)
    fig_line.update_traces(line_color="#2E86C1", line_width=3)
    st.plotly_chart(fig_line, use_container_width=True)
    st.info("💡 **차트 해석 도움말:** 시간이 흐를수록 전 세계 사람들의 술 소비량이 늘어나는지, 줄어드는지 트렌드를 파악해 보세요!")
    st.markdown("---")

    # 📊 2. 술을 가장 많이 마시는 나라 Top 20 (막대그래프)
    st.header(f"📊 2. 술을 가장 많이 마시는 나라 Top 20 ({selected_year}년 기준)")
    df_top20 = df_alc_filtered.sort_values(by=alc_col, ascending=False).head(20)
    
    bar_colors = []
    for c in df_top20["country"]:
        if "korea" in str(c):
            bar_colors.append("#E74C3C") # 한국은 강렬한 빨간색! 🔴
        else:
            bar_colors.append("#34495E") # 다른 나라는 차분한 네이비
            
    fig_bar = px.bar(df_top20, x="country", y=alc_col, title="국가별 알코올 소비량 상위 20개국")
    fig_bar.update_traces(marker_color=bar_colors)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("---")

    # 🎯 3. 알코올 소비량 vs 행복지수 상관관계 (산점도)
    st.header("🎯 3. 알코올 소비량과 행복지수의 실시간 관계")
    df_merged = pd.merge(df_alc_filtered, df_hap_filtered, on="country", how="inner")

    if not df_merged.empty:
        df_group = []
        df_size = []
        for c in df_merged["country"]:
            if "korea" in str(c):
                df_group.append("대한민국 🔴")
                df_size.append(18) # 한국은 점 크기를 엄청 크게!
            else:
                df_group.append("다른 국가들 🔵")
                df_size.append(8)
                
        df_merged["group"] = df_group
        
        fig_scatter = px.scatter(
            df_merged, x=alc_col, y=hap_col, color="group",
            color_discrete_map={"대한민국 🔴": "#E74C3C", "다른 국가들 🔵": "#AED6F1"},
            hover_name="country", title="알코올 소비량(X축)과 행복지수(Y축)의 분포",
            size=df_size, size_max=18
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # 💡 데이터 분석 결론 도출 (피어슨 상관계수 이용)
        corr_value = df_merged[alc_col].corr(df_merged[hap_col])
        st.subheader("💡 대시보드가 도출한 최종 결론")
        st.write(f"두 데이터의 상관계수는 현재 **{corr_value:.2f}** 입니다.")
        
        if corr_value > 0.4:
            st.success(f"✨ **상관관계가 꽤 높아요! ({corr_value:.2f})** 실제로 술을 많이 마시는 나라들이 더 높은 행복지수를 기록하고 있네요! 사회적 유대감이나 축제 문화가 영향을 미쳤을지도 모릅니다.")
        elif corr_value < -0.4:
            st.warning(f"✨ **반대 관계가 나타나요! ({corr_value:.2f})** 술을 많이 마시는 나라일수록 오히려 행복지수가 낮아집니다. 스트레스나 사회적 알코올 의존증 문제를 의심해볼 수 있어요.")
        else:
            st.info(f"✨ **뚜렷한 관계가 없어요! ({corr_value:.2f})** 산점도 점들이 넓게 퍼져 있죠? 즉, 술을 많이 마신다고 더 행복해지거나 불행해지는 건 아니라는 뜻이에요! 행복은 다른 요인이 더 중요해요. 🎉")
    else:
        st.error("😭 선택한 연도에 알코올 데이터와 행복지수 데이터가 일치하는 국가가 없습니다. 사이드바에서 연도를 조절해 보세요!")

except FileNotFoundError:
    st.error("⚠️ [파일 에러] 파일명을 확인할게요! 깃허브 최상위 폴더에 'alcohol-consumption.csv'와 'world-happiness-report-2024.csv'가 있는지 다시 봐주세요!")
