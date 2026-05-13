import streamlit as st

# 1. 쿠키 데이터 구성 (PDB의 주요 인기 쿠키 및 유형 반영)
# 이름, MBTI, 성격 특징을 포함합니다.
cookie_data = [
    {"name": "퓨어바닐라 쿠키", "mbti": "INFJ", "desc": "부드럽고 인자하며, 모두를 포용하는 성인군자 같은 성격입니다."},
    {"name": "세인트릴리 쿠키", "mbti": "INFJ", "desc": "진리를 탐구하며 조용하고 사색에 잠기는 편입니다."},
    {"name": "홀리베리 쿠키", "mbti": "ESFP", "desc": "호탕하고 에너지가 넘치며, 친구와 연회를 즐기는 분위기 메이커입니다."},
    {"name": "다크초코 쿠키", "mbti": "ISFP", "desc": "무뚝뚝해 보이지만 내면에는 고뇌와 따뜻한 마음을 품고 있습니다."},
    {"name": "바다요정 쿠키", "mbti": "INFP", "desc": "감수성이 풍부하고 고독을 즐기며, 소중한 것을 그리워합니다."},
    {"name": "감초맛 쿠키", "mbti": "ENTP", "desc": "야망이 크고 잔머리가 좋으며, 투덜대면서도 자기 일을 해냅니다."},
    {"name": "에스프레소맛 쿠키", "mbti": "INTJ", "desc": "효율을 중시하고 철두철미하며, 마법 공학에 대한 자부심이 강합니다."},
    {"name": "마들렌맛 쿠키", "mbti": "ESTP", "desc": "자신감이 넘치고 행동력이 빠르며, 빛의 가호 아래 직진하는 성격입니다."},
    {"name": "호밀맛 쿠키", "mbti": "ESTP", "desc": "거침없고 자유분방하며 목표를 정하면 바로 실행에 옮깁니다."},
    {"name": "클로버맛 쿠키", "mbti": "ENFP", "desc": "자유롭고 낙천적이며, 노래와 이야기를 통해 행복을 전파합니다."},
    {"name": "허브맛 쿠키", "mbti": "ISFJ", "desc": "다정다감하고 식물을 사랑하며 주변을 따뜻하게 돌봅니다."},
    {"name": "벨벳케이크맛 쿠키", "mbti": "ENTJ", "desc": "카리스마 있는 리더십을 가졌으며 목표를 위해 단호하게 행동합니다."},
    {"name": "밀키웨이맛 쿠키", "mbti": "ENFP", "desc": "꿈이 많고 활발하며 기차 운행에 열심인 귀여운 몽상가입니다."},
    {"name": "딸기크레페맛 쿠키", "mbti": "ENTP", "desc": "호기심이 많고 영리하며 실험과 기계 장치를 매우 좋아합니다."},
    {"name": "와일드베리맛 쿠키", "mbti": "ISTJ", "desc": "과묵하고 충성심이 강하며 맡은 바 책임을 끝까지 완수합니다."}
]

# 2. 스트림릿 UI 구성
st.title("🍪 쿠키런 킹덤 MBTI 도감")
st.write("궁금한 MBTI를 선택하면 해당되는 쿠키와 특징을 보여드려요!")

# 3. MBTI 선택 셀렉트박스
mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ", 
    "ISTP", "ISFP", "INFP", "INTP", 
    "ESTP", "ESFP", "ENFP", "ENTP", 
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]
selected_mbti = st.selectbox("MBTI 유형을 골라보세요:", mbti_list)

st.divider()

# 4. 필터링 및 결과 출력
results = [cookie for cookie in cookie_data if cookie["mbti"] == selected_mbti]

if results:
    st.subheader(f"✨ {selected_mbti} 유형의 쿠키들")
    for cookie in results:
        with st.expander(f"📌 {cookie['name']}"):
            st.write(f"**MBTI:** {cookie['mbti']}")
            st.write(f"**성격 특징:** {cookie['desc']}")
else:
    st.info(f"현재 데이터에 {selected_mbti} 유형인 쿠키가 아직 등록되지 않았어요!")

# 하단 정보
st.caption("출처: Personality Database (PDB) 사용자 투표 기반")
