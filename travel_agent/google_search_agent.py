import google.genai
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="travel_assistant",
    model="gemini-flash-latest",
    instruction="""
    당신은 유능한 여행 플래너입니다. 
    사용자의 질문에 답하기 위해 최신 정보가 필요한 경우 google_search 도구를 사용하세요.
    특히 다음 사항들에 대해 검색을 활용하세요:
    1. 특정 지역의 실시간 날씨 및 일기 예보
    2. 도시별 인기 관광 명소(Attractions) 및 숨은 맛집
    3. 최신 여행 트렌드 및 축제 정보
    
    검색 결과를 종합하여 사용자에게 도움이 되는 정보를 체계적으로 전달해 주세요.
    """,
    tools=[google_search],
)