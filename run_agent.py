# run_agent.py (프로젝트 루트에 생성)
import asyncio
import sys
from dotenv import load_dotenv
load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from travel_agent.agent import root_agent

async def main():
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name="travel_app", session_service=session_service)
    
    session = await session_service.create_session(app_name="travel_app", user_id="user1")
    # 사용자 메시지 전송
    message = types.Content(
        role="user",
        parts=[types.Part(text="서울 날씨 어때?, 예산 200만원으로 럭셔리한 10일 여행을 하고 싶어.")]
        #parts=[types.Part(text="제주도 2박 3일 여행 추천해줘")]
    )
    response = runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=message,
    )
    async for event in response:
        if event.content and event.content.parts:
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())