import json
from google.adk.agents import Agent
from google.adk.models import LlmResponse
from google.genai import types

def observe_tool_result(callback_context, tool_name, tool_args, tool_result):
    """도구 실행 후 결과를 관찰하고 상태를 업데이트합니다."""
    # 날씨 결과 관찰 → 악천후 감지
    if tool_name == "get_weather":
        result = json.loads(str(tool_result)) if isinstance(tool_result, str) else tool_result
        condition = result.get("condition", "")
        if condition in ["태풍", "폭우", "폭설"]:
            # 세션 상태에 경고 플래그 설정
            callback_context.state["weather_alert"] = True
            callback_context.state["alert_type"] = condition
            print(f"⚠ 악천후 감지: {condition}")
    
    # 예산 결과 관찰 → 고비용 감지
    if tool_name == "estimate_budget":
        result = json.loads(str(tool_result)) if isinstance(tool_result, str) else tool_result
        total = sum(result.values()) if isinstance(result, dict) else 0
        if total > 2000000:
            callback_context.state["high_budget_alert"] = True
            print(f"💰 고비용 감지: {total:,}원")
    return None # 결과는 변경하지 않고 관찰만

root_agent = Agent(
    name="travel_assistant",
    model="gemini-2.0-flash",
    instruction="""
    당신은 여행 플래너입니다.
    weather_alert 상태가 True이면 실내 활동을 우선 추천하세요.
    high_budget_alert가 True이면 절약 팁을 함께 제공하세요.
    """,
    tools=[get_weather, search_attractions, estimate_budget],
    after_tool_callback=observe_tool_result,
)