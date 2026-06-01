import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & Korean Title
st.set_page_config(page_title="Alcohol & Happiness", layout="wide", page_icon="📊")

st.title("🍻 술을 많이 마시는 나라가 더 행복할까?")
st.subheader("나라별 알코올 소비량과 행복지수 상관관계 분석 (수행평가)")
st.markdown("---")

# 2. Load CSV Files (From root directory)
try:
    df_alc = pd.read_csv("alcohol_consumption_around_the_world.csv")
    df_hap = pd.read_csv("world-happiness-report-2024.csv")
    
    # Standardize column names to lowercase
    df_alc.columns = df_alc.columns.str.strip().str.lower()
    df_hap.columns = df_hap.columns.str.strip().str.lower()
    
    # Rename country name column for merging
    if 'country name' in df_hap.columns:
        df_hap = df_hap.rename(columns={'country name': 'country'})

    df_alc['country'] = df_alc['country'].str.strip().str.lower()
    df_hap['country'] = df_hap['country'].str.strip().str.lower()

    # Find relevant column names automatically
    alc_col = [col for col in df_alc.columns if 'consumption' in col or 'total' in col or 'liter' in col][0]
    hap_col = [col for col in df_hap.columns if 'score' in col or 'happiness' in col][0]

    # 3. Sidebar - Year Slider
    st.sidebar.header("⚙️ 연도 선택")
    common_years = sorted(list(set(df_alc['year'].unique()).intersection(set(df_hap['year'].unique()))))
    
    if common_years:
        selected_year = st.sidebar.slider("📅 분석할 연도를 골라보세요", min_value=min(common_years), max_value=max(common_years), value=max(common_years))
        df_alc_filtered = df_alc[df_alc['year'] == selected_year]
        df_hap_filtered = df_hap[df_hap['year'] == selected_year]
    else:
        st.sidebar.warning("공통 연도가 없어 전체 평균으로 분석합니다.")
        df_alc_filtered = df_alc
        df_hap_filtered = df_hap

    # 4. Chart 1: Line Chart (Global Trend)
    st.header("📈 1. 전 세계 알코올 소비량 추이")
    df_trend = df_alc.groupby('year')[alc_col].mean().reset_index()
    fig_line = px.line(df_trend, x='year', y=alc_col, title="연도별 전 세계 평균 알코올 소비량 변화", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("---")

    # 5. Chart 2: Bar Chart (Top 20 Countries & Highlight Korea)
    st.header("📊 2. 술을 가장 많이 마시는 나라 Top 20")
    df_top20 = df_alc_filtered.sort_values(by=alc_col, ascending=False).head(20)
    
    # Pure English logic for colors (No Korean text inside variables)
    bar_colors = ['#E74C3C' if 'korea' in str(c) else '#34495E' for c in df_top20['country']]
    fig_bar = px.bar(df_top20, x='country', y=alc_col, title="알코올 소비량 상위 20개국 (대한민국은 빨간색 🔴)")
    fig_bar.update_traces(marker_color=bar_colors)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("---")

    # 6. Chart 3 & 4: Scatter Plot (Alcohol vs Happiness)
    st.header("🎯 3. 알코올 소비량과 행복지수의 관계")
    df_merged = pd.merge(df_alc_filtered, df_hap_filtered, on='country', how='inner')

    if not df_merged.empty:
        # Categorize for visualization using English labels
        df_merged['group'] = df_merged['country'].apply(lambda x: 'Korea' if 'korea' in str(x) else 'Others')
        
        fig_scatter = px.scatter(
            df_merged, x=alc_col, y=hap_col, color='group',
            color_discrete_map={'Korea': '#E74C3C', 'Others': '#AED6F1'},
            hover_name='country', title="알코올 소비량과 행복지수 산점도 (국가 이름은 마우스를 대보세요!)",
            size=[16 if 'korea' in str(c) else 8 for c in df_merged['country']], size_max=16
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # 7. Correlation & Dynamic Conclusion (Korean only in st.write)
        corr_value = df_merged[alc_col].corr(df_merged[hap_col])
        st.subheader("💡 데이터 분석 결론")
        st.write(f"두 데이터의 상관계수는 **{corr_value:.2f}** 입니다.")
        
        if corr_value > 0.2:
            st.info("✨ **결론:** 술을 많이 마시는 나라가 더 행복한 경향이 있네요!")
        elif corr_value < -0.2:
            st.info("✨ **결론:** 술을 많이 마시는 나라일수록 덜 행복한 경향이 있네요!")
        else:
            st.info("✨ **결론:** 술 소비량과 행복지수 사이에는 뚜렷한 관계가 없어요. 행복은 술이 아닌 다른 게 결정하나 봐요! 🎉")
    else:
        st.error("데이터 매칭에 실패했습니다.")

except FileNotFoundError:
    st.error("⚠️ [파일 에러] CSV 파일 이름을 찾을 수 없어요! 깃허브 최상위 폴더에 파일이 제대로 있는지 꼭 확인해 주세요.")
