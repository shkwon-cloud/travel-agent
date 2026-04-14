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

root_agent = Agent(
    name="travel_assistant",
    model="gemini-2.0-flash",
    instruction="""
    당신은 여행 플래너입니다.
    사용자가 여행지 날씨를 물으면 get_weather 도구를 사용하세요.
    날씨 정보를 바탕으로 적절한 옷차림과 준비물을 추천해 주세요.
    """,
    tools=[get_weather],
)