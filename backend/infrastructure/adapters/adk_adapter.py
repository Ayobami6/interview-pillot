import os
import json
from typing import List
from domain.ports.ai_service import IAiService
from domain.models.question import InterviewQuestion
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


class AdkAdapter(IAiService):
    """ADK implementation of the AI service port."""

    def __init__(self):
        # Defaulting to Gemini 2.5 Flash as seen in other projects
        model_name = os.getenv("AI_MODEL", "gemini-2.5-flash")

        self.agent = Agent(
            model=model_name,
            name="interview_generator",
            description="Expert technical interviewer and career coach.",
            instruction=(
                "You are an expert technical interviewer and career coach. "
                "Your task is to generate high-quality, relevant interview questions for a given job role.\n\n"
                "## Output Format\n"
                "Always return a JSON list of objects. Each object must have:\n"
                "- 'text': The question text.\n"
                "- 'category': The type of question (e.g., 'Technical', 'Behavioral', 'System Design').\n"
                "- 'difficulty': The level (e.g., 'Easy', 'Medium', 'Hard').\n\n"
                "Only return the JSON list. No preamble or explanation."
            ),
        )
        self.session_service = InMemorySessionService()

    async def generate_questions(
        self, role: str, count: int
    ) -> List[InterviewQuestion]:
        """Generates questions using the ADK Runner."""
        user_id = "default_user"
        session_id = f"gen_{os.urandom(4).hex()}"

        runner = Runner(
            app_name="interview_pillot",
            agent=self.agent,
            session_service=self.session_service,
        )

        await self.session_service.create_session(
            app_name="interview_pillot", user_id=user_id, session_id=session_id
        )

        prompt = f"Generate {count} interview questions for the role of {role}."

        full_response = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(role="user", parts=[types.Part(text=prompt)]),
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        full_response += part.text

        try:
            # Clean response if LLM adds backticks
            cleaned_json = full_response.strip()
            if cleaned_json.startswith("```json"):
                cleaned_json = cleaned_json[7:]
            if cleaned_json.endswith("```"):
                cleaned_json = cleaned_json[:-3]
            cleaned_json = cleaned_json.strip()

            questions_data = json.loads(cleaned_json)
            return [InterviewQuestion(**q) for q in questions_data]
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            # Fallback or error handling
            # In a real scenario, we might want to retry or raise a ServiceException
            print(f"Error parsing AI response: {e}")
            return []
