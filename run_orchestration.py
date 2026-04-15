# =============================================================================
# Lab 8-3 실행 스크립트
# 복합 오케스트레이션: 분석 → 병렬검색 → 반복개선 → 최종발표
# =============================================================================
import asyncio
import sys
import warnings
warnings.filterwarnings("ignore", message=".*EXPERIMENTAL.*")
warnings.filterwarnings("ignore", message=".*non-text parts.*")

from dotenv import load_dotenv
load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from travel_agent.orchestration_agent import root_agent


async def main():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="travel_orchestrator_app",
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name="travel_orchestrator_app",
        user_id="user1",
    )

    # =========================================================================
    # 여행 요청 메시지 (원하는 대로 수정하세요!)
    # =========================================================================
    user_request = "제주도 2박 3일 여행을 계획해줘. 보통 예산이고, 자연과 맛집에 관심이 많아."

    print("=" * 70)
    print(f"🧳 여행 요청: {user_request}")
    print("=" * 70)
    print()

    message = types.Content(
        role="user",
        parts=[types.Part(text=user_request)],
    )

    response = runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=message,
    )

    # 각 에이전트별 출력 추적
    current_agent = None
    async for event in response:
        # 에이전트 전환 감지
        if hasattr(event, 'author') and event.author and event.author != current_agent:
            current_agent = event.author
            print(f"\n{'─' * 50}")
            print(f"🤖 [{current_agent}] 에이전트 실행 중...")
            print(f"{'─' * 50}")

        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    print(part.text)


if __name__ == "__main__":
    print("🚀 Lab 8-3: 복합 오케스트레이션 시작!")
    print("📋 파이프라인: 분석 → 병렬검색 → 반복개선 → 최종발표")
    print()
    asyncio.run(main())
    print("\n✅ 오케스트레이션 완료!")
