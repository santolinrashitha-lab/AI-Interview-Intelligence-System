INTERVIEW_PROMPT = """
Generate 1 technical interview question for a {role} with {experience} years of experience.
Make it realistic and industry-level.
"""

EVALUATION_PROMPT = """
Evaluate the following interview answer.

Question:
{question}

Answer:
{answer}

Give:
1. Score out of 10
2. Strengths
3. Weaknesses
4. Improved Answer
"""