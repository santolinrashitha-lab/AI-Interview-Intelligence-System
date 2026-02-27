from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_answer(question, answer):
    prompt = f"""
    Evaluate the following interview answer.

    Question:
    {question}

    Answer:
    {answer}

    Provide:
    1. Score out of 10
    2. Strengths
    3. Weaknesses
    4. Improved Answer
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert technical interviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content