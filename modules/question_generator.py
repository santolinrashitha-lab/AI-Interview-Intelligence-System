import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_question(role, experience, round_type):

    prompt = f"""
    Generate ONE {round_type} interview question 
    for a {experience}-year experienced {role}.

    Only return the question.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",   # cost-efficient & powerful
        messages=[
            {"role": "system", "content": "You are an expert technical interviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()