from app.schemas.mcq import MCQ


mcq = MCQ(
    question="What is sampling?",
    option_a="Selecting a subset from a population",
    option_b="Studying every individual",
    option_c="Removing data",
    option_d="Sorting data",
    correct_answer="option_a",
    difficulty="easy"
)

print(mcq)