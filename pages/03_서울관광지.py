import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(page_title="Seoul Top 10 Tourist Spots", layout="wide")

st.title("🗺️ 외국인이 가장 좋아하는 서울 관광지 Top 10")
st.caption("지도의 마커를 클릭하시면 하단에서 가까운 지하철역과 추천 놀거리를 확인할 수 있습니다.")

# 2. 서울 관광지 데이터 정의 (Top 10)
spots = [
    {
        "name": "경복궁 (Gyeongbokgung Palace)",
        "lat": 37.5796, "lon": 126.9770,
        "subway": "3호선 경복궁역 (5번 출구)",
        "todo": "한복 대여 체험 및 수문장 교대식 관람"
    },
    {
        "name": "N서울타워 (N Seoul Tower)",
        "lat": 37.5512, "lon": 126.9882,
        "subway": "4호선 명동역에서 남산케이블카 이용",
        "todo": "전망대에서 서울 야경 감상 및 사랑의 자물쇠 걸기"
    },
    {
        "name": "명동 쇼핑거리 (Myeongdong Street)",
        "lat": 37.5634, "lon": 126.9846,
        "subway": "4호선 명동역 / 2호선 을지로입구역",
        "todo": "K-뷰티 로드숍 쇼핑 및 길거리 음식(길거리 간식) 투어"
    },
    {
        "name": "북촌한옥마을 (Bukchon Hanok Village)",
        "lat": 37.5829, "lon": 126.9835,
        "subway": "3호선 안국역 (3번 출구)",
        "todo": "전통 한옥 골목길 산책 및 전통 찻집 체험"
    },
    {
        "name": "홍대 걷고싶은거리 (Hongdae Street)",
        "lat": 37.5567, "lon": 126.9237,
        "subway": "2호선/공항철도 홍대입구역",
        "todo": "저녁 시간 거리 버스킹 관람 및 이색 카페 탐방"
    },
    {
        "name": "동대문디자인플라자 (DDP)",
        "lat": 37.5668, "lon": 127.0094,
        "subway": "2, 4, 5호선 동대문역사문화공원역",
        "todo": "독특한 야간 건축물 조명 감상 및 패션 전시회 관람"
    },
    {
        "name": "인사동 문화의거리 (Insadong)",
        "lat": 37.5744, "lon": 126.9848,
        "subway": "3호선 안국역 / 1호선 종각역",
        "todo": "쌈지길에서 한국 전통 공예품 기념품 쇼핑"
    },
    {
        "name": "롯데월드타워 & 서울스카이 (Lotte World Tower)",
        "lat": 37.5126, "lon": 127.1025,
        "subway": "2, 8호선 잠실역",
        "todo": "세계 최고 수준의 초고층 전망대 스릴 체험 및 석촌호수 산책"
    },
    {
        "name": "강남역 & 코엑스몰 (Gangnam & COEX)",
        "lat": 37.5119, "lon": 127.0590,
        "subway": "2호선 삼성역 (코엑스 연결)",
        "todo": "별마당 도서관 인증샷 촬영 및 SM타운 등 K-Pop 문화 체험"
    },
    {
        "name": "광장시장 (Gwangjang Market)",
        "lat": 37.5701, "lon": 127.0010,
        "subway": "1호선 종로5가역 / 2, 5호선 을지로4가역",
        "todo": "녹두빈대떡, 육회, 마약김밥 등 넷플릭스에 나온 시장 먹거리 투어"
    }
]

# 3. 폴리움 지도 생성 (서울 중심부 세팅)
m = folium.Map(location=[37.555, 126.985], zoom_start=12)

# 마커 추가
for spot in spots:
    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=spot["name"],
        tooltip=spot["name"]
    ).add_to(m)

# 4. 스트림릿에 지도 렌더링 및 클라이언트 입력 감지
# returned_objects를 통해 사용자가 클릭한 마커 정보를 가져옵니다.
st_data = st_folium(m, width=900, height=500)

st.markdown("---")
st.subheader("🔍 선택한 관광지 상세 정보")

# 5. 클릭 이벤트 처리 및 하단 요약 출력
clicked_spot_name = None

# 마커가 클릭되었는지 감지하는 로직
if st_data and 'last_object_clicked_popup' in st_data and st_data['last_object_clicked_popup']:
    clicked_spot_name = st_data['last_object_clicked_popup'].strip()

if clicked_spot_name:
    # 데이터 매칭 후 출력
    matched_spot = next((s for s in spots if s["name"].strip() == clicked_spot_name), None)
    
    if matched_spot:
        st.success(f"📍 **{matched_spot['name']}**")
        st.info(f"🚇 **가까운 지하철역:** {matched_spot['subway']} | 🎡 **추천 놀거리:** {matched_spot['todo']}")
    else:
        st.write("💡 지도의 마커를 클릭하시면 상세 요약 정보가 표시됩니다.")
else:
    st.write("💡 지도의 마커를 클릭하시면 상세 요약 정보가 표시됩니다.")
