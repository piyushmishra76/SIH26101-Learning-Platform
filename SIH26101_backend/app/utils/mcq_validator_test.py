from app.schemas.mcq import MCQ, MCQResponse
from app.utils.mcq_validator import validate_mcqs


mcq = MCQ(
    question="What is sampling?",
    option_a="Selecting a subset from a population",
    option_b="Studying every individual",
    option_c="Removing data",
    option_d="Sorting data",
    correct_answer="option_a",
    difficulty="easy"
)

response = MCQResponse(
    questions=[mcq]
)

print(validate_mcqs(response))