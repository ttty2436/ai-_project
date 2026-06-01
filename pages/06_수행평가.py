import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------------------
# 0. 페이지 기본 설정 및 제목 🎈
# ----------------------------------------------------------------
st.set_page_config(page_title="알코올 & 행복지수 분석", layout="wide", page_icon="📊")

st.title("🍻 술을 많이 마시는 나라가 더 행복할까?")
st.subheader("나라별 알코올 소비량과 행복지수 상관관계 분석 (수행평가)")
st.markdown("---")

# ----------------------------------------------------------------
# 1. 데이터 불러오기 및 전처리 🛠️
# ----------------------------------------------------------------
# 캐글 데이터셋 파일명 설정 (최상위 폴더에 있다고 가정)
ALCOHOL_FILE = "alcohol_consumption_around_the_world.csv"
HAPPINESS_FILE = "world-happiness-report-2024.csv"

@st.cache_data
def load_and_process_data():
    try:
        # 데이터 읽기
        df_alc = pd.read_csv(ALCOHOL_FILE)
        df_hap = pd.read_csv(HAPPINESS_FILE)
        
        # 컬럼명 소문자 및 공백 제거로 다루기 쉽게 만들기
        df_alc.columns = df_alc.columns.str.strip().str.lower()
        df_hap.columns = df_hap.columns.str.strip().str.lower()
        
        # [중요] 국가 데이터 병합을 위한 국가명 표준화 (예시)
        # 행복지수 데이터의 'country name'을 'country'로 통일
        if 'country name' in df_hap.columns:
            df_hap = df_hap.rename(columns={'country name': 'country'})
            
        name_mapping = {
            'united states': 'usa',
            'united kingdom': 'uk',
            'south korea': 'korea, south',
            'republic of korea': 'korea, south'
        }
        df_alc['country'] = df_alc['country'].str.strip().str.lower().replace(name_mapping)
        df_hap['country'] = df_hap['country'].str.strip().str.lower().replace(name_mapping)
        
        return df_alc, df_hap
    except Exception as e:
        st.error(f"⚠️ 데이터를 불러오는 중 오류가 발생했어요! 파일명과 위치를 확인해 주세요. 에러 내용: {e}")
        return None, None

df_alc, df_hap = load_and_process_data()

if df_alc is not None and df_hap is not None:
    # ----------------------------------------------------------------
    # 2. 사이드바 - 연도 선택 슬라이더 🎛️
    # ----------------------------------------------------------------
    st.sidebar.header("⚙️ 데이터 필터링")
    
    # 두 데이터셋에 공통으로 존재하는 연도 찾기
    alc_years = set(df_alc['year'].unique())
    hap_years = set(df_hap['year'].unique())
    common_years = sorted(list(alc_years.intersection(hap_years)))
    
    if not common_years:
        # 공통 연도가 없으면 각각의 최신 연도 기준으로 매칭을 시도하거나 안내
        st.sidebar.warning("💡 두 데이터의 연도가 일치하지 않아 전체 데이터 기준으로 분석합니다.")
        selected_year = None
    else:
        selected_year = st.sidebar.slider(
            "📅 분석할 연도를 선택하세요",
            min_value=int(min(common_years)),
            max_value=int(max(common_years)),
            value=int(max(common_years)), # 기본값은 가장 최신 연도
            step=1
        )

    # ----------------------------------------------------------------
    # 3. 그래프 1: 연도별 전 세계 평균 알코올 소비량 추이 (꺾은선) 📈
    # ----------------------------------------------------------------
    st.header("📈 1. 전 세계 알코올 소비량은 어떻게 변하고 있을까?")
    
    # 연도별 평균 소비량 계산 (여기선 'alcohol_consumption' 또는 'liters' 등 컬럼명 확인 필요)
    # 캐글 데이터의 대표적인 수치 컬럼을 찾아 평균을 구합니다. (대부분 'consumption' 혹은 'total' 단어 포함)
    alc_col = [col for col in df_alc.columns if 'consumption' in col or 'total' in col or 'liter' in col][0]
    
    df_alc_trend = df_alc.groupby('year')[alc_col].mean().reset_index()
    
    fig_line = px.line(
        df_alc_trend, 
        x='year', 
        y=alc_col, 
        title="연도별 전 세계 평균 알코올 소비량 추이",
        labels={'year': '연도', alc_col: '평균 알코올 소비량 (L)'},
        markers=True
    )
    fig_line.update_traces(line_color='#2E86C1', line_width=3)
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.markdown("---")

    # ----------------------------------------------------------------
    # 데이터 필터링 (선택된 연도 기준)
    # ----------------------------------------------------------------
    if selected_year:
        df_alc_filtered = df_alc[df_alc['year'] == selected_year]
        df_hap_filtered = df_hap[df_hap['year'] == selected_year]
        st.success(f" 현재 **{selected_year}년** 데이터를 분석 중입니다!")
    else:
        df_alc_filtered = df_alc.groupby('country')[alc_col].mean().reset_index()
        # 행복지수 점수 컬럼 찾기 ('ladder score' 또는 'happiness score')
        hap_col = [col for col in df_hap.columns if 'score' in col or 'happiness' in col][0]
        df_hap_filtered = df_hap.groupby('country')[hap_col].mean().reset_index()

    hap_col = [col for col in df_hap.columns if 'score' in col or 'happiness' in col][0]

    # ----------------------------------------------------------------
    # 4. 그래프 2: 나라별 알코올 소비량 Top 20 (막대 - 한국 강조) 📊
    # ----------------------------------------------------------------
    st.header("📊 2. 술을 가장 많이 마시는 나라는 어디일까? (Top 20)")
    
    df_alc_top20 = df_alc_filtered.sort_values(by=alc_col, ascending=False).head(20)
    
    # 한국이 Top 20에 있는지 확인하고 색상 지정 (한국은 빨간색, 나머지는 파란색계열)
    colors = ['#E74C3C' if 'korea' in str(c).lower() else '#34495E' for c in df_alc_top20['country']]
    
    fig_bar = px.bar(
        df_alc_top20,
        x='country',
        y=alc_col,
        title=f"{selected_year if selected_year else '전체'}년 알코올 소비량 상위 20개국 (대한민국은 빨간색 🔴)",
        labels={'country': '국가', alc_col: '알코올 소비량'},
    )
    fig_bar.update_traces(marker_color=colors)
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")

    # ----------------------------------------------------------------
    # 5. 그래프 3 & 4: 알코올 소비량 vs 행복지수 산점도 (한국 강조) 🎯
    # ----------------------------------------------------------------
    st.header("🎯 3. 알코올 소비량과 행복지수의 상관관계")
    
    # 두 데이터셋 합치기
    df_merged = pd.merge(df_alc_filtered, df_hap_filtered, on='country', how='inner')
    
    if df_merged.empty:
        st.warning("⚠️ 선택한 연도에 매칭되는 국가 데이터가 없습니다. 데이터의 국가 이름을 확인해 주세요.")
    else:
        # 한국 데이터 분리해서 강조하기 위해 조건 부여
        df_merged['is_korea'] = df_merged['country'].apply(lambda x: '대한민국 (Korea)' if 'korea' in str(x).lower() else '다른 나라들')
        
        # 한국을 더 돋보이게 하기 위해 색상 맵핑 직접 지정
        color_map = {'대한민국 (Korea)': '#E74C3C', '다른 나라들': '#AED6F1'}
        
        fig_scatter = px.scatter(
            df_merged,
            x=alc_col,
            y=hap_col,
            color='is_korea',
            color_discrete_map=color_map,
            hover_name='country',
            title=f"알코올 소비량 vs 행복지수 산점도 ({selected_year if selected_year else '전체'}년)",
            labels={alc_col: '인당 알코올 소비량', hap_col: '행복 지수', 'is_korea': '구분'},
            size=[15 if 'korea' in str(c).lower() else 8 for c in df_merged['country']], # 한국 점 크기를 더 크게!
            size_max=15
        )
        
        # 텍스트로 국가명 표시 (한국만 텍스트를 고정으로 띄우거나, 마우스 올릴 때 보이게 처리)
        # Plotly Express에서는 기본적으로 hover_name으로 깔끔하게 보이므로 가독성을 위해 hover 유지!
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # 💡 수행평가용 한줄 결론 자동 도출 (상관계수 계산)
        correlation = df_merged[alc_col].corr(df_merged[hap_col])
        
        st.subheader("💡 데이터로 보는 수행평가 결론 결론")
        st.write(f"선택하신 데이터에서 알코올 소비량과 행복지수의 상관계수는 **{correlation:.2f}** 입니다.")
        
        if correlation > 0.3:
            st.info("✨ **결론:** 상관계수가 양수입니다! 술을 많이 마시는 나라가 비교적 더 행복한 경향이 있네요! (알코올이 사회적 즐거움을 반영할지도?)")
        elif correlation < -0.3:
            st.info("✨ **결론:** 상관계수가 음수입니다! 술을 많이 마시는 나라일수록 덜 행복한 경향이 있군요! (스트레스로 인한 음주성향일지도?)")
        else:
            st.info("✨ **결론:** 상관계수가 0에 가깝습니다! 술 소비량과 행복지수 사이에는 **뚜렷한 관계가 없다**고 볼 수 있어요. 행복은 술이 아닌 다른 요소가 더 중요해 보입니다! 🎉")
