import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 스트림릿 클라우드(리눅스) 환경에서 한글 깨짐을 방지하기 위한 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic' or 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 페이지 설정
st.set_page_config(page_title="서울 역대 기온 조회기", page_icon="🌡️", layout="wide")

st.title("🌡️ 서울 역대 날짜별 기온 변화 조회기")
st.markdown("선택한 월/일에 해당하는 역대 연도별 최고기온과 최저기온 추이를 한눈에 확인하세요.")

# 데이터 로드 및 전처리 함수 (캐싱 적용으로 속도 향상)
@st.cache_data
def load_data():
    # 기상청 파일 특유의 한글 인코딩(CP949) 문제를 해결하기 위한 설정
    try:
        df = pd.read_csv('seoul.csv', encoding='cp949')
    except UnicodeDecodeError:
        # 혹시 모를 다른 인코딩 형식(EUC-KR)에 대한 대비
        df = pd.read_csv('seoul.csv', encoding='euc-kr')
    
    # 날짜 열의 공백 문자(\t 등) 제거 후 데이트타임 형식으로 변환
    df['날짜'] = df['날짜'].astype(str).str.strip()
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치 제거 (날짜가 제대로 변환되지 않은 행 제거)
    df = df.dropna(subset=['날짜'])
    
    # 연, 월, 일 컬럼 추가
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    
    # 분석에 필요한 컬럼명 정리 및 데이터 타입 정렬
    df['최고기온(℃)'] = pd.to_numeric(df['최고기온(℃)'], errors='coerce')
    df['최저기온(℃)'] = pd.to_numeric(df['최저기온(℃)'], errors='coerce')
    
    return df

# 데이터 로딩 메시지
with st.spinner("100년 치 서울 기상 데이터를 불러오는 중입니다..."):
    df = load_data()

# 사이드바에서 월/일 선택 UI 구성
st.sidebar.header("📅 날짜 선택")
selected_month = st.sidebar.selectbox("월을 선택하세요", options=sorted(df['월'].unique()))
selected_day = st.sidebar.selectbox("일을 선택하세요", options=sorted(df[df['월'] == selected_month]['일'].unique()))

# 선택된 날짜 데이터 필터링
filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values(by='연도')

if filtered_df.empty:
    st.warning("선택한 날짜에 해당하는 데이터가 존재하지 않습니다.")
else:
    # 대시보드 레이아웃 (카드형 지표 레이아웃)
    st.subheader(f"📊 매년 {selected_month}월 {selected_day}일의 기온 추이")
    
    col1, col2, col3 = st.columns(3)
    
    # 극값 계산 (결측치 제외)
    valid_max = filtered_df.dropna(subset=['최고기온(℃)'])
    valid_min = filtered_df.dropna(subset=['최저기온(℃)'])
    
    if not valid_max.empty and not valid_min.empty:
        max_row = valid_max.loc[valid_max['최고기온(℃)'].idxmax()]
        min_row = valid_min.loc[valid_min['최저기온(℃)'].idxmin()]
        
        with col1:
            st.metric(label="역대 최고 기온", value=f"{max_row['최고기온(℃)']} ℃", delta=f"{int(max_row['연도'])}년")
        with col2:
            st.metric(label="역대 최저 기온", value=f"{min_row['최저기온(℃)']} ℃", delta=f"{int(min_row['연도'])}년")
        with col3:
            st.metric(label="관측 연도 수", value=f"{len(filtered_df)}개 연도")

    # 그래프 그리기 (Matplotlib 설정 호출 부분을 명확하게 고쳤습니다!)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 요구사항에 따른 색상 반영 (찐빨강: #B22222, 연한 파란색: #87CEFA)
    ax.plot(filtered_df['연도'], filtered_df['최고기온(℃)'], color='#B22222', marker='o', linestyle='-', linewidth=2, label='최고기온')
    ax.plot(filtered_df['연도'], filtered_df['최저기온(℃)'], color='#87CEFA', marker='o', linestyle='-', linewidth=2, label='최저기온')
    
    # 격자 및 라벨 디자인 수정
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlabel('연도 (Year)', fontsize=11, labelpad=10)
    ax.set_ylabel('기온 (℃)', fontsize=11, labelpad=10)
    ax.set_title(f"역대 {selected_month}월 {selected_day}일의 기온 변화 추세", fontsize=14, pad=15)
    ax.legend(loc='best', frameon=True, shadow=True)
    
    # 스트림릿 웹 화면에 그래프 출력
    st.pyplot(fig)
    
    # 데이터 테이블 펼치기 기능 제공
    with st.expander("🔍 상세 데이터 테이블 확인하기"):
        display_df = filtered_df[['연도', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].reset_index(drop=True)
        st.dataframe(display_df, use_container_width=True)
