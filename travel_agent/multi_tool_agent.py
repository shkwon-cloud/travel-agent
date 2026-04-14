import google.genai
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """특정 도시의 현재 날씨 정보를 조회합니다.
    Args:
        city: 날씨를 조회할 도시 이름 (예: '서울', '제주')
    Returns:
        온도, 상태, 습도 정보를 담은 딕셔너리
    """
    # 실습용 더미 데이터 (실제로는 API 호출)
    weather_data = {
        "서울": {"temp": 18, "condition": "맑음", "humidity": 45},
        "제주": {"temp": 22, "condition": "흐림", "humidity": 70},
        "부산": {"temp": 20, "condition": "맑음", "humidity": 55},
    }
    return weather_data.get(city, {"temp": 20, "condition": "정보없음", "humidity": 50})


def search_attractions(city: str, category: str) -> list:
    """도시의 관광지를 카테고리별로 검색합니다.
    Args:
        city: 검색할 도시
        category: 관광지 유형 ("자연", "문화", "맛집", "쇼핑")
    Returns:
        관광지 이름과 설명 리스트
    """
    data = {
        ("제주", "자연"): [
            {"name": "성산일출봉", "desc": "유네스코 세계자연유산"},
            {"name": "한라산", "desc": "해발 1,947m 한국 최고봉"},
        ],
        ("제주", "맛집"): [
            {"name": "흑돼지거리", "desc": "제주 특산 흑돼지 맛집 밀집"},
            {"name": "동문시장", "desc": "현지인이 사랑하는 전통시장"},
        ],
    }
    return data.get((city, category), [{"name": "정보 없음"}])


def estimate_budget(city: str, days: int, style: str) -> dict:
    """여행 예산을 추정합니다.
    Args:
        city: 여행 도시
        days: 여행 일수
        style: 여행 스타일 ("알뜰", "보통", "럭셔리")
    Returns:
        항목별 예상 비용
    """
    daily_cost = {
        "알뜰": {"숙소": 50000, "식비": 30000, "교통": 15000},
        "보통": {"숙소": 100000, "식비": 50000, "교통": 25000},
        "럭셔리": {"숙소": 250000, "식비": 100000, "교통": 50000},
    }
    base_costs = daily_cost.get(style, daily_cost["보통"])
    return {item: cost * days for item, cost in base_costs.items()}


root_agent = Agent(
    name="travel_assistant",
    model="gemini-flash-latest",
    instruction="""
    당신은 종합 여행 플래너입니다.
    - 날씨 질문 → get_weather 사용
    - 관광지 추천 → search_attractions 사용
    - 예산 문의 → estimate_budget 사용
    도구의 결과를 종합하여 친절하게 안내합니다.
    """,
    tools=[get_weather, search_attractions, estimate_budget],
)