import re
from google.adk.agents import Agent
from google.adk.models import LlmResponse
from google.genai import types

# 1. 도구 함수들 정의
def get_weather(city: str) -> dict:
    """특정 도시의 현재 날씨 정보를 조회합니다."""
    weather_data = {"서울": {"temp": 18, "condition": "맑음"}, "제주": {"temp": 22, "condition": "흐림"}}
    return weather_data.get(city, {"temp": 20, "condition": "정보없음"})

def estimate_budget(city: str, days: int, style: str) -> dict:
    """여행 예산을 추정합니다."""
    daily_cost = {"알뜰": 50000, "보통": 100000, "럭셔리": 250000}
    cost = daily_cost.get(style, 100000) * days
    return {"total_estimated_budget": cost, "currency": "KRW"}

# 2. 가드레일 설정
BLOCKED_KEYWORDS = ['도박', '마약', '불법']

def input_guardrail(callback_context, llm_request):
    """모델 호출 전 입력을 검사합니다."""
    user_message = llm_request.contents[-1].parts[0].text
    
    # 메시지가 텍스트가 아닌 경우(예: 도구 실행 결과가 전달되는 경우) 검사를 건너뜁니다.
    if not user_message:
        return None

    for keyword in BLOCKED_KEYWORDS:
        if keyword in user_message:
            # 차단된 경우 LlmResponse 객체로 감싸서 반환
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text=f"죄송합니다. 해당 주제('{keyword}')에 대해서는 도움을 드릴 수 없습니다.")]
                )
            )
    return None # None 반환 = 통과

def output_guardrail(callback_context, llm_response):
    """모델 응답 후 출력을 검사합니다."""
    if not llm_response or not llm_response.content or not llm_response.content.parts:
        return None

    part = llm_response.content.parts[0]
    text = part.text

    # 텍스트가 없는 경우(예: 도구 호출인 경우) 검사를 건너뜁니다.
    if not text:
        return llm_response

    # 개인정보(전화번호 패턴) 마스킹
    masked = re.sub(r"\d{2,3}-\d{3,4}-\d{4}", "[전화번호 마스킹]", text)
    if masked != text:
        part.text = masked
    return llm_response

def tool_guardrail(tool, args, tool_context):
    """도구 호출 전 검사합니다."""
    if tool.name == "estimate_budget":
        days = args.get("days", 0)
        if days > 30:
            # 도구 실행 대신 경고 메시지 반환
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text="30일을 초과하는 여행 예산은 산출할 수 없습니다. 짧은 기간으로 다시 문의해주세요.")]
                )
            )
    return None # 정상 진행

# 3. 에이전트 생성
root_agent = Agent(
    name="travel_assistant",
    model="gemini-flash-latest",
    instruction="당신은 여행 플래너입니다. 날씨와 예산 질문에 답변해 주세요.",
    tools=[get_weather, estimate_budget],
    before_model_callback=input_guardrail,
    after_model_callback=output_guardrail,
    before_tool_callback=tool_guardrail,
)