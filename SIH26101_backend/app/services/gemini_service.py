import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.schemas.mcq import MCQResponse
from google.genai import types
from app.utils.mcq_validator import validate_mcqs
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def generate_mcqs(
    text: str,
    number_of_questions: int = 3,
    competencies=None
):
    competency_text = ""
    if competencies:
        competency_text = "\n".join(
            f"- ID: {c.id}, Name: {c.name}, Description: {c.description or 'No description'}"
            for c in competencies
    )
    prompt = f"""
You are an educational assessment generator.

Generate {number_of_questions} multiple-choice questions
based ONLY on the provided content.

Rules:
- Each question must have exactly 4 options.
- Only one option must be correct.
- Do not use information outside the provided content.
- Questions should test understanding, not just memorization.
- Difficulty must be one of: easy, medium, hard.
- correct_answer must contain only A, B, C, or D.
- Provide a short explanation for why the correct answer is correct.
- source_page must be null for now.
- competency_id must be selected ONLY from the provided competency list.
- If none of the competencies are relevant, competency_id must be null.
- Never invent a competency ID.

Available competencies:
{competency_text}

Content:
{text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MCQResponse,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            )
        )
    )

    mcq_response = MCQResponse.model_validate_json(response.text)

    validate_mcqs(mcq_response)

    return mcq_response