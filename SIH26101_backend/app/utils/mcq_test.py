from app.services.gemini_service import generate_mcqs


text = """
Sampling is the process of selecting a subset of individuals
from a larger population. The selected subset is called a sample.
Sampling is commonly used because studying an entire population
can be expensive and time-consuming.
"""

result = generate_mcqs(text, 3)

print(result)