import json
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.prompt import SYSTEM_PROMPT
from app.schemas import LogAnalysis, LogRequest

load_dotenv()

model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")
google_cloud_location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")

if not google_cloud_project:
    raise RuntimeError("GOOGLE_CLOUD_PROJECT must be set for Vertex AI mode.")

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_PROJECT"] = google_cloud_project
os.environ["GOOGLE_CLOUD_LOCATION"] = google_cloud_location

APP_NAME = "devops-log-analyzer"
USER_ID = "http-api-user"

root_agent = Agent(
    name="devops_log_analyzer",
    model=model_name,
    description="Analyzes DevOps logs and returns issue, cause, fix, and severity.",
    instruction=SYSTEM_PROMPT,
    input_schema=LogRequest,
    output_schema=LogAnalysis,
)

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


async def analyze_log_agent(log: str) -> LogAnalysis:
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    request_content = types.Content(
        role="user",
        parts=[types.Part(text=json.dumps({"log": log}))],
    )

    final_response = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=request_content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = "".join(
                part.text for part in event.content.parts if getattr(part, "text", None)
            )

    if not final_response:
        raise RuntimeError("The ADK agent did not produce a final response.")

    return LogAnalysis.model_validate_json(final_response)
