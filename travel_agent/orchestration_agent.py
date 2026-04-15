# =============================================================================
# Lab 8-3: 복합 오케스트레이션 (Sequential + Parallel + Loop)
# 전체 파이프라인: 분석 → 병렬검색 → 반복개선 → 발표
# =============================================================================
from datetime import datetime
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent


# =============================================================================
# 도구(Tool) 정의 - 각 에이전트가 사용할 함수들
# =============================================================================

def get_weather(city: str) -> dict:
    """특정 도시의 현재 날씨 정보를 조회합니다.
    Args:
        city: 날씨를 조회할 도시 이름 (예: '서울', '제주', '부산', '경주', '여수')
    Returns:
        온도, 상태, 습도 정보를 담은 딕셔너리
    """
    weather_data = {
        "서울": {"temp": 18, "condition": "맑음", "humidity": 45},
        "제주": {"temp": 22, "condition": "흐림", "humidity": 70},
        "부산": {"temp": 20, "condition": "맑음", "humidity": 55},
        "경주": {"temp": 17, "condition": "맑음", "humidity": 40},
        "여수": {"temp": 19, "condition": "구름조금", "humidity": 60},
        "강릉": {"temp": 16, "condition": "맑음", "humidity": 50},
    }
    return weather_data.get(city, {"temp": 20, "condition": "정보없음", "humidity": 50})


def search_flights(departure: str, arrival: str, date: str) -> list:
    """항공편을 검색합니다.
    Args:
        departure: 출발 도시 (예: '서울', '김포', '인천')
        arrival: 도착 도시 (예: '제주', '부산')
        date: 출발 날짜 (예: '2026-05-01')
    Returns:
        항공편 목록 (항공사, 출발시간, 가격 포함)
    """
    flights = {
        ("서울", "제주"): [
            {"airline": "대한항공", "departure_time": "07:00", "price": 89000, "duration": "1시간 10분"},
            {"airline": "아시아나", "departure_time": "09:30", "price": 85000, "duration": "1시간 10분"},
            {"airline": "제주항공", "departure_time": "11:00", "price": 59000, "duration": "1시간 15분"},
            {"airline": "진에어", "departure_time": "14:00", "price": 55000, "duration": "1시간 15분"},
        ],
        ("서울", "부산"): [
            {"airline": "대한항공", "departure_time": "08:00", "price": 75000, "duration": "55분"},
            {"airline": "에어부산", "departure_time": "10:00", "price": 49000, "duration": "1시간"},
        ],
        ("서울", "여수"): [
            {"airline": "대한항공", "departure_time": "09:00", "price": 82000, "duration": "1시간"},
            {"airline": "진에어", "departure_time": "13:00", "price": 58000, "duration": "1시간 5분"},
        ],
    }
    # 김포/인천 → 서울로 매핑
    dep = "서울" if departure in ["김포", "인천"] else departure
    key = (dep, arrival)
    result = flights.get(key, [{"airline": "정보없음", "price": 0, "departure_time": "-", "duration": "-"}])
    return {"departure": departure, "arrival": arrival, "date": date, "flights": result}


def search_hotels(city: str, checkin: str, nights: int, style: str = "보통") -> list:
    """숙소를 검색합니다.
    Args:
        city: 숙소를 검색할 도시
        checkin: 체크인 날짜 (예: '2026-05-01')
        nights: 숙박 일수
        style: 숙소 스타일 ('알뜰', '보통', '럭셔리')
    Returns:
        숙소 목록 (이름, 가격, 평점 포함)
    """
    hotels = {
        ("제주", "알뜰"): [
            {"name": "제주 게스트하우스", "price_per_night": 40000, "rating": 4.2, "type": "게스트하우스"},
            {"name": "탑동 호스텔", "price_per_night": 35000, "rating": 4.0, "type": "호스텔"},
        ],
        ("제주", "보통"): [
            {"name": "제주 오션뷰 호텔", "price_per_night": 120000, "rating": 4.5, "type": "호텔"},
            {"name": "서귀포 리조트", "price_per_night": 150000, "rating": 4.3, "type": "리조트"},
        ],
        ("제주", "럭셔리"): [
            {"name": "롯데호텔 제주", "price_per_night": 350000, "rating": 4.8, "type": "5성급 호텔"},
            {"name": "해비치 호텔&리조트", "price_per_night": 400000, "rating": 4.9, "type": "5성급 리조트"},
        ],
        ("부산", "보통"): [
            {"name": "해운대 씨뷰 호텔", "price_per_night": 110000, "rating": 4.4, "type": "호텔"},
            {"name": "광안리 비치 호텔", "price_per_night": 95000, "rating": 4.2, "type": "호텔"},
        ],
        ("부산", "럭셔리"): [
            {"name": "파크 하얏트 부산", "price_per_night": 380000, "rating": 4.9, "type": "5성급 호텔"},
        ],
    }
    key = (city, style)
    result = hotels.get(key, [{"name": f"{city} 일반 호텔", "price_per_night": 100000, "rating": 4.0, "type": "호텔"}])
    return {"city": city, "checkin": checkin, "nights": nights, "style": style, "hotels": result}


def search_attractions(city: str, category: str = "전체") -> list:
    """도시의 관광지 및 활동을 검색합니다.
    Args:
        city: 검색할 도시
        category: 관광지 유형 ('자연', '문화', '맛집', '액티비티', '전체')
    Returns:
        관광지/활동 이름, 설명, 예상 비용 리스트
    """
    data = {
        ("제주", "자연"): [
            {"name": "성산일출봉", "desc": "유네스코 세계자연유산, 일출 명소", "cost": 5000},
            {"name": "한라산", "desc": "해발 1,947m 한국 최고봉 등반", "cost": 0},
            {"name": "만장굴", "desc": "세계 최장 용암동굴", "cost": 4000},
        ],
        ("제주", "맛집"): [
            {"name": "흑돼지거리", "desc": "제주 특산 흑돼지 맛집 거리", "cost": 25000},
            {"name": "동문시장", "desc": "현지인이 사랑하는 전통시장", "cost": 15000},
            {"name": "협재해물탕", "desc": "신선한 해산물 전문", "cost": 30000},
        ],
        ("제주", "액티비티"): [
            {"name": "스쿠버다이빙", "desc": "제주 바다 다이빙 체험", "cost": 80000},
            {"name": "승마 체험", "desc": "제주 조랑말 승마", "cost": 40000},
            {"name": "카약 투어", "desc": "해안 절경 카약", "cost": 50000},
        ],
        ("부산", "자연"): [
            {"name": "해운대해수욕장", "desc": "대한민국 대표 해수욕장", "cost": 0},
            {"name": "태종대", "desc": "부산의 절경을 한눈에", "cost": 3000},
        ],
        ("부산", "맛집"): [
            {"name": "자갈치시장", "desc": "국내 최대 수산시장", "cost": 20000},
            {"name": "BIFF 광장", "desc": "부산 길거리 음식 성지", "cost": 10000},
        ],
        ("부산", "문화"): [
            {"name": "감천문화마을", "desc": "한국의 산토리니", "cost": 0},
            {"name": "해동용궁사", "desc": "바다 위의 사찰", "cost": 0},
        ],
    }
    if category == "전체":
        results = []
        for key, items in data.items():
            if key[0] == city:
                results.extend(items)
        return {"city": city, "category": "전체", "attractions": results if results else [{"name": "정보 없음"}]}
    return {"city": city, "category": category, "attractions": data.get((city, category), [{"name": "정보 없음"}])}


def estimate_budget(city: str, days: int, style: str) -> dict:
    """여행 예산을 추정합니다.
    Args:
        city: 여행 도시
        days: 여행 일수
        style: 여행 스타일 ('알뜰', '보통', '럭셔리')
    Returns:
        항목별 예상 비용과 총 비용
    """
    daily_cost = {
        "알뜰": {"숙소": 50000, "식비": 30000, "교통": 15000, "관광": 10000},
        "보통": {"숙소": 100000, "식비": 50000, "교통": 25000, "관광": 30000},
        "럭셔리": {"숙소": 250000, "식비": 100000, "교통": 50000, "관광": 80000},
    }
    base_costs = daily_cost.get(style, daily_cost["보통"])
    breakdown = {item: cost * days for item, cost in base_costs.items()}
    breakdown["총합"] = sum(breakdown.values())
    return {"city": city, "days": days, "style": style, "budget": breakdown}


def evaluate_itinerary(itinerary: str) -> dict:
    """생성된 여행 일정의 품질을 평가합니다.
    Args:
        itinerary: 평가할 여행 일정 텍스트
    Returns:
        점수(0~100)와 개선 포인트
    """
    score = 0
    feedback = []

    # 필수 요소 체크
    checks = {
        "숙소": "숙소 정보가 포함되어야 합니다",
        "식사": "식사 계획이 포함되어야 합니다",
        "교통": "이동 수단 정보가 포함되어야 합니다",
        "시간": "시간대별 일정이 포함되어야 합니다",
        "비용": "예상 비용이 포함되어야 합니다",
    }
    for keyword, msg in checks.items():
        if keyword in itinerary:
            score += 20
        else:
            feedback.append(msg)

    return {
        "score": score,
        "passed": score >= 80,
        "feedback": feedback,
        "message": "✅ 합격! 충분한 품질입니다." if score >= 80 else "⚠️ 개선이 필요합니다. 피드백을 반영하세요."
    }


def get_travel_context() -> dict:
    """현재 여행 컨텍스트(계절, 성수기 등)를 감지합니다.
    Returns:
        현재 시간, 계절, 여행 성수기 여부 등 환경 정보
    """
    now = datetime.now()
    month = now.month
    seasons = {
        (3, 4, 5): "봄", (6, 7, 8): "여름",
        (9, 10, 11): "가을", (12, 1, 2): "겨울"
    }
    season = next(v for k, v in seasons.items() if month in k)
    peak = month in [7, 8, 12, 1]
    return {
        "current_date": now.strftime("%Y-%m-%d"),
        "season": season,
        "is_peak_season": peak,
        "recommendation": "성수기입니다. 조기 예약을 권장합니다." if peak else "비수기라 할인 혜택이 많습니다."
    }


# =============================================================================
# Phase 1: 요구사항 분석 (단일 에이전트)
# =============================================================================
analyzer = Agent(
    name="requirement_analyzer",
    model="gemini-flash-latest",
    instruction="""
    당신은 여행 요구사항 분석 전문가입니다.
    
    사용자의 여행 요구사항을 분석하여 구조화하세요.
    
    반드시 다음 정보를 파악하여 명확하게 정리하세요:
    - 목적지 (destination)
    - 여행 날짜/기간 (dates/days)
    - 예산 스타일 (budget_style: 알뜰/보통/럭셔리)
    - 관심사 (interests: 자연, 문화, 맛집, 액티비티 등)
    
    get_travel_context 도구로 현재 계절과 성수기 여부를 확인하세요.
    
    분석 결과를 아래 형식으로 정리하세요:
    📋 요구사항 분석 결과:
    - 목적지: [도시명]
    - 기간: [N박 M일]
    - 예산 스타일: [스타일]
    - 관심사: [관심사 목록]
    - 현재 계절: [계절]
    - 성수기 여부: [여부]
    """,
    tools=[get_travel_context],
)


# =============================================================================
# Phase 2: 병렬 검색 (ParallelAgent)
# 항공편, 숙소, 관광지를 동시에 검색
# =============================================================================
flight_search = Agent(
    name="flight_search",
    model="gemini-flash-latest",
    instruction="""
    당신은 항공편 검색 전문가입니다.
    
    이전 단계에서 분석된 요구사항(목적지, 날짜)을 참고하여
    search_flights 도구로 항공편을 검색하세요.
    
    출발지를 알 수 없으면 '서울'을 기본값으로 사용하세요.
    날짜를 알 수 없으면 현재 날짜 기준 1주일 후를 사용하세요.
    
    결과를 아래 형식으로 정리하세요:
    ✈️ 항공편 검색 결과:
    - 항공사, 출발시간, 소요시간, 가격을 포함
    - 가장 저렴한 옵션과 가장 빠른 옵션을 표시
    """,
    tools=[search_flights],
)

hotel_search = Agent(
    name="hotel_search",
    model="gemini-flash-latest",
    instruction="""
    당신은 숙소 검색 전문가입니다.
    
    이전 단계에서 분석된 요구사항(목적지, 기간, 예산 스타일)을 참고하여
    search_hotels 도구로 숙소를 검색하세요.
    
    결과를 아래 형식으로 정리하세요:
    🏨 숙소 검색 결과:
    - 숙소명, 1박 가격, 평점, 숙소 유형 포함
    - 예산에 맞는 추천 숙소를 강조
    """,
    tools=[search_hotels],
)

activity_search = Agent(
    name="activity_search",
    model="gemini-flash-latest",
    instruction="""
    당신은 관광지/활동 검색 전문가입니다.
    
    이전 단계에서 분석된 요구사항(목적지, 관심사)을 참고하여
    search_attractions 도구로 관광지와 활동을 검색하세요.
    get_weather 도구로 현지 날씨도 확인하세요.
    
    결과를 아래 형식으로 정리하세요:
    🎯 관광지/활동 검색 결과:
    - 장소명, 설명, 예상 비용 포함
    - 날씨에 맞는 활동을 우선 추천
    """,
    tools=[search_attractions, get_weather],
)

# 세 에이전트를 병렬 실행
parallel_search = ParallelAgent(
    name="parallel_search",
    sub_agents=[flight_search, hotel_search, activity_search],
)


# =============================================================================
# Phase 3: 일정 조합 + 품질 검증 루프 (LoopAgent)
# =============================================================================
composer = Agent(
    name="itinerary_composer",
    model="gemini-flash-latest",
    instruction="""
    당신은 여행 일정 조합 전문가입니다.
    
    이전 단계에서 병렬로 검색된 항공편, 숙소, 관광지 결과를 종합하여
    완전한 여행 일정을 조합하세요.
    
    estimate_budget 도구로 전체 예산을 추정하세요.
    
    반드시 다음 요소를 모두 포함하세요:
    - 시간대별 상세 일정 (오전/오후/저녁)
    - 숙소 정보 (이름, 가격)
    - 식사 계획 (조식/중식/석식)
    - 교통 정보 (이동 수단, 비용)
    - 비용 항목별 정리
    
    이전 반복에서 피드백이 있었다면 반드시 반영하세요.
    
    📅 여행 일정:
    [일차별 상세 일정 작성]
    """,
    tools=[estimate_budget],
)

quality_checker = Agent(
    name="quality_checker",
    model="gemini-flash-latest",
    instruction="""
    당신은 여행 일정 품질 검증 전문가입니다.
    
    이전 에이전트(itinerary_composer)가 생성한 일정을 
    evaluate_itinerary 도구로 평가하세요.
    
    평가 기준:
    - 숙소 정보 포함 여부
    - 식사 계획 포함 여부
    - 교통 정보 포함 여부
    - 시간대별 일정 포함 여부
    - 비용 정보 포함 여부
    
    점수가 80점 이상이면:
    - "✅ 품질 검증 통과!" 메시지를 출력하세요.
    - 반드시 escalate 키워드를 포함: "일정이 완성되었습니다. 최종 발표 단계로 넘어갑니다."
    
    점수가 80점 미만이면:
    - 부족한 부분의 피드백을 구체적으로 전달하세요.
    - 다음 반복에서 개선할 점을 명확히 제시하세요.
    """,
    tools=[evaluate_itinerary],
)

# 루프: composer → quality_checker 반복 (최대 3회)
refinement_loop = LoopAgent(
    name="refinement_loop",
    sub_agents=[composer, quality_checker],
    max_iterations=3,
)


# =============================================================================
# Phase 4: 최종 프레젠테이션 (단일 에이전트)
# =============================================================================
presenter = Agent(
    name="final_presenter",
    model="gemini-flash-latest",
    instruction="""
    당신은 여행 일정 프레젠터입니다.
    
    앞선 모든 단계에서 생성되고 검증된 일정을 
    보기 좋고 깔끔한 형식으로 최종 정리하세요.
    
    반드시 다음을 포함하세요:
    
    🗺️ 최종 여행 일정표
    ━━━━━━━━━━━━━━━━━━━━
    
    1. 📋 여행 개요 (목적지, 기간, 테마)
    
    2. 📅 일별 상세 일정
       - 일차별로 시간대(오전/오후/저녁)에 따른 활동
       - 각 활동의 예상 소요시간과 비용
    
    3. 💰 총 예산 요약
       - 항공편, 숙소, 식비, 교통, 관광 비용 항목별 정리
       - 총 예상 비용
    
    4. 🎒 준비물 체크리스트
       - 여행에 필요한 준비물 목록
       - 날씨에 맞는 옷차림 추천
    
    5. 💡 여행 팁
       - 현지 유용한 정보
       - 주의사항
    """,
)


# =============================================================================
# 전체 파이프라인: 분석 → 병렬검색 → 반복개선 → 발표
# =============================================================================
root_agent = SequentialAgent(
    name="travel_orchestrator",
    sub_agents=[analyzer, parallel_search, refinement_loop, presenter],
)
