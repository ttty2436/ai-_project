import streamlit as st

# 1. 방대한 쿠키 데이터 (PDB 최신 투표 기반 50인 이상)
cookie_data = [
    # INFJ
    {"name": "퓨어바닐라 쿠키", "mbti": "INFJ", "desc": "모두를 포용하는 성인군자. 평화를 사랑하고 통찰력이 깊습니다."},
    {"name": "세인트릴리 쿠키", "mbti": "INFJ", "desc": "진리를 갈구하며 조용히 사색에 잠기는 탐구자입니다."},
    {"name": "미스틱플라워 쿠키", "mbti": "INFJ", "desc": "해탈의 경지에 이른 차분함으로 허무의 힘을 다스립니다."},
    {"name": "서리여왕 쿠키", "mbti": "INFJ", "desc": "차갑지만 섭리를 수호하며, 감정을 절제하는 현자입니다."},
    
    # INFP
    {"name": "바다요정 쿠키", "mbti": "INFP", "desc": "깊은 그리움과 고독을 간직한 섬세하고 서정적인 영혼입니다."},
    {"name": "목화맛 쿠키", "mbti": "INFP", "desc": "소중한 친구를 기다리며 따뜻한 등불을 밝히는 헌신적인 성격입니다."},
    {"name": "박하사탕맛 쿠키", "mbti": "INFP", "desc": "조용하고 내성적이며, 고래와 바다의 이야기를 듣는 것을 좋아합니다."},
    {"name": "눈설탕맛 쿠키", "mbti": "INFP", "desc": "외로움을 많이 타지만 친구들과 어울리고 싶어 하는 순수한 마음을 가졌습니다."},

    # ENFP
    {"name": "파르페맛 쿠키", "mbti": "ENFP", "desc": "자신만의 색깔로 노래하는 긍정적인 에너지의 싱어송라이터입니다."},
    {"name": "밀키웨이맛 쿠키", "mbti": "ENFP", "desc": "꿈과 상상이 가득한 은하 열차의 밝고 활기찬 차장님입니다."},
    {"name": "소르베맛 쿠키", "mbti": "ENFP", "desc": "자유로운 영혼으로 세상을 누비며 새로운 경험을 즐깁니다."},
    {"name": "체리맛 쿠키", "mbti": "ENFP", "desc": "폭발하는 불꽃놀이를 즐기는 파괴적(?)이지만 명랑한 성격입니다."},

    # ENFJ
    {"name": "바람궁수 쿠키", "mbti": "ENFJ", "desc": "자연을 수호하겠다는 강한 사명감과 카리스마를 지닌 수호자입니다."},
    {"name": "휘낭시에맛 쿠키", "mbti": "ENFJ", "desc": "자신이 믿는 대상을 향한 무한한 충성심과 따뜻한 리더십을 보여줍니다."},
    {"name": "코코아맛 쿠키", "mbti": "ENFJ", "desc": "모두에게 따뜻한 코코아를 권하며 행복을 나누는 친절한 성격입니다."},

    # INTJ
    {"name": "에스프레소맛 쿠키", "mbti": "INTJ", "desc": "효율과 논리를 중시하며, 완벽한 커피 마법을 위해 연구에 매진합니다."},
    {"name": "다크카카오 쿠키", "mbti": "INTJ", "desc": "엄격하고 무거운 책임감을 짊어진, 고독하고 단호한 군주입니다."},
    {"name": "감초맛 쿠키", "mbti": "INTJ", "desc": "자신의 능력을 과신하며 은밀하게 큰 계획을 세우는 전략가입니다."},

    # INTP
    {"name": "연금술사맛 쿠키", "mbti": "INTP", "desc": "게으름을 싫어하고 원리 원칙을 분석하는 냉철한 이론가입니다."},
    {"name": "슈크림맛 쿠키", "mbti": "INTP", "desc": "실수투성이지만 마법 공부에 대한 열정만큼은 누구보다 깊은 학구파입니다."},
    {"name": "블루파이맛 쿠키", "mbti": "INTP", "desc": "도서관의 금서를 지키며 지식을 탐구하는 차분한 지식인입니다."},

    # ENTP
    {"name": "딸기크레페맛 쿠키", "mbti": "ENTP", "desc": "호기심이 폭발하는 천재. 상대를 당황하게 만드는 날카로운 질문을 즐깁니다."},
    {"name": "체스초코 쿠키", "mbti": "ENTP", "desc": "상대를 수 싸움으로 압도하며 상황을 장난처럼 즐기는 지략가입니다."},
    {"name": "구미호맛 쿠키", "mbti": "ENTP", "desc": "자신의 매력을 이용해 상대를 꾀어내는 재치 있고 영리한 성격입니다."},

    # ENTJ
    {"name": "골드치즈 쿠키", "mbti": "ENTJ", "desc": "황금 도시의 여왕. 강력한 추진력과 야망으로 왕국을 지배합니다."},
    {"name": "벨벳케이크맛 쿠키", "mbti": "ENTJ", "desc": "확고한 목표 의식을 가지고 군단을 지휘하는 카리스마 리더입니다."},
    {"name": "캡틴아이스 쿠키", "mbti": "ENTJ", "desc": "냉철한 판단력으로 함선을 진두지휘하는 엄격한 사령관입니다."},

    # ISTJ
    {"name": "와일드베리맛 쿠키", "mbti": "ISTJ", "desc": "말수가 적고 행동으로 증명하는, 바위처럼 든든한 호위무사입니다."},
    {"name": "에클레어맛 쿠키", "mbti": "ISTJ", "desc": "역사와 유물에 대한 집착에 가까운 열정과 꼼꼼한 기록광입니다."},
    {"name": "아몬드맛 쿠키", "mbti": "ISTJ", "desc": "사건 현장에서 철저하게 증거를 수집하는 노련한 형사입니다."},

    # ISFJ
    {"name": "허브맛 쿠키", "mbti": "ISFJ", "desc": "식물들의 목소리에 귀 기울이는 따뜻하고 성실한 정원사입니다."},
    {"name": "클로티드 크림 쿠키", "mbti": "ISFJ", "desc": "예의 바르고 품위 있으며, 가문의 명예와 책임을 중시합니다."},
    {"name": "달빛술사 쿠키", "mbti": "ISFJ", "desc": "오랜 시간 마법사들의 도시를 묵묵히 지켜온 헌신적인 수호자입니다."},

    # ESFJ
    {"name": "민트초코 쿠키", "mbti": "ESFJ", "desc": "매너가 몸에 배어 있으며, 음악을 통해 대중과 교감하는 것을 좋아합니다."},
    {"name": "웨어울프맛 쿠키", "mbti": "ESFJ", "desc": "타인에게 피해를 줄까 걱정하며 거리를 두지만, 사실 정이 많습니다."},
    {"name": "크림유니콘 쿠키", "mbti": "ESFJ", "desc": "사라져가는 추억을 아쉬워하며 모두의 행복을 바라는 몽상가입니다."},

    # ESTJ
    {"name": "실론나이트 쿠키", "mbti": "ESTJ", "desc": "전장의 기강을 잡고 규율을 강조하는 엄격한 베테랑 기사입니다."},
    {"name": "호밀맛 쿠키", "mbti": "ESTJ", "desc": "자신만의 정의를 관철하며 질서를 지키는 거침없는 현상금 사냥꾼입니다."},
    {"name": "라즈베리맛 쿠키", "mbti": "ESTJ", "desc": "가문의 자부심이 강하며 승리를 위해 혹독하게 자신을 채찍질합니다."},

    # ISTP
    {"name": "닌자맛 쿠키", "mbti": "ISTP", "desc": "수행에만 전념하며 필요한 말만 하는 냉철한 개인주의자입니다."},
    {"name": "블랙레이즌맛 쿠키", "mbti": "ISTP", "desc": "현실적이고 실용적인 판단으로 마을을 지키는 츤데레 수호자입니다."},
    {"name": "칠리맛 쿠키", "mbti": "ISTP", "desc": "복잡한 건 질색! 일단 훔치고 보는 본능적인 행동파 도둑입니다."},

    # ISFP
    {"name": "다크초코 쿠키", "mbti": "ISFP", "desc": "내면의 상처를 안고 정처 없이 떠도는 고독한 검사입니다."},
    {"name": "뱀파이어맛 쿠키", "mbti": "ISFP", "desc": "자유로운 삶을 지향하며 귀찮은 일은 피하고 싶은 낙천주의자입니다."},
    {"name": "딸기맛 쿠키", "mbti": "ISFP", "desc": "낯을 많이 가리지만 자신만의 세계가 뚜렷하고 소중한 친구를 아낍니다."},

    # ESTP
    {"name": "마들렌맛 쿠키", "mbti": "ESTP", "desc": "자신감이 넘쳐흐르며, 어떤 위기에도 당당하게 맞서는 모험가입니다."},
    {"name": "캡사이신맛 쿠키", "mbti": "ESTP", "desc": "뜨거운 열정으로 돌진하며 매 순간 스릴을 즐기는 에너자이저입니다."},
    {"name": "불꽃정령 쿠키", "mbti": "ESTP", "desc": "자신만만하고 승부욕이 강하며 타오르는 불꽃처럼 화끈한 성격입니다."},

    # ESFP
    {"name": "홀리베리 쿠키", "mbti": "ESFP", "desc": "호탕한 웃음과 의리! 잔치와 친구를 사랑하는 열정의 여왕입니다."},
    {"name": "트위즐젤리맛 쿠키", "mbti": "ESFP", "desc": "파괴와 혼돈을 즐기며, 짜릿한 재미를 위해서라면 어디든 달려갑니다."},
    {"name": "공주맛 쿠키", "mbti": "ESFP", "desc": "왕실의 격식보다 모험과 새로운 친구들을 좋아하는 활발한 성격입니다."}
]

# 2. UI 레이아웃 설정
st.set_page_config(page_title="쿠키런 MBTI 대백과", page_icon="🍪", layout="wide")

st.title("🍪 쿠키런 킹덤 MBTI 대백과 (50인+)")
st.markdown("PDB 데이터를 기반으로 총 **16가지 유형, 50명 이상의 쿠키**를 정리했습니다.")

# 3. 사이드바 MBTI 선택
mbti_list = sorted(list(set(c["mbti"] for c in cookie_data)))
selected_mbti = st.sidebar.selectbox("🎯 궁금한 MBTI 유형을 선택하세요", mbti_list)

# 4. 메인 화면 출력
st.header(f"✨ {selected_mbti} 유형의 쿠키들")
filtered_cookies = [c for c in cookie_data if c["mbti"] == selected_mbti]

if filtered_cookies:
    # 3열 배치를 통해 더 많은 정보를 한눈에 확인
    cols = st.columns(3)
    for i, cookie in enumerate(filtered_cookies):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ff4b4b;">
                <h3 style="margin-top: 0;">{cookie['name']}</h3>
                <p style="color: #555;">{cookie['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("해당 유형의 쿠키를 준비 중입니다!")

# 5. 하단 통계
st.divider()
st.caption(f"현재 총 {len(cookie_data)}명의 쿠키 정보가 수록되어 있습니다.")
