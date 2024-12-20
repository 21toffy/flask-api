import openai
from openai import OpenAI

from flask import current_app

def get_openai_answer(question):
    openai.api_key = current_app.config["OPENAI_API_KEY"]
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an all knowing assistant, whi=o has knowledge on almost anything  need you to answer this questons"},
            {"role": "user", "content": question},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


