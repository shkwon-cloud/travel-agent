from datetime import datetime
from google.adk.agents import Agent

def get_travel_context() -> dict:
    """현재 여행 컨텍스트를 감지합니다.
    Returns:
        현재 시간, 계절, 여행 성수기 여부 등 환경 정보
    """
    now = datetime.now()
    month = now.month
    # 계절 판단
    seasons = {
        (3,4,5): "봄", (6,7,8): "여름",
        (9,10,11): "가을", (12,1,2): "겨울"
    }
    season = next(v for k, v in seasons.items() if month in k)
    # 성수기 판단
    peak = month in [7, 8, 12, 1]
    return {
        "current_date": now.strftime("%Y-%m-%d"),
        "season": season,
        "is_peak_season": peak,
        "recommendation": "성수기입니다. 조기 예약을 권장합니다." if peak else "비수기라 할인 혜택이 많습니다."
    }

def get_weather(city: str) -> dict:
    """특정 도시의 현재 날씨 정보를 조회합니다."""
    weather_data = {
        "서울": {"temp": 18, "condition": "맑음"},
        "제주": {"temp": 22, "condition": "흐림"},
        "부산": {"temp": 20, "condition": "맑음"},
    }
    return weather_data.get(city, {"temp": 20, "condition": "정보없음"})

def search_attractions(city: str) -> dict:
    """특정 도시의 관광지를 검색합니다."""
    attractions_data = {
        "서울": ["경복궁", "남산타워", "북촌한옥마을", "명동"],
        "제주": ["성산일출봉", "만장굴", "협재해수욕장", "우도"],
        "부산": ["해운대", "감천문화마을", "자갈치시장", "태종대"],
    }
    return {"city": city, "attractions": attractions_data.get(city, ["정보없음"])}

root_agent = Agent(
    name="travel_assistant",
    model="gemini-flash-latest",
    instruction="""
    당신은 여행 플래너입니다.
    여행 추천 전에 반드시 get_travel_context를 호출하여
    현재 계절과 성수기 여부를 확인하고, 이를 반영하여 추천하세요.
    """,
    tools=[get_travel_context, get_weather, search_attractions],
)