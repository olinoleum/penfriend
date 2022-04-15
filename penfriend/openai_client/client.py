# Standard library imports
import os

# Third party imports
import openai

# Local application imports

openai.api_key = os.getenv("OPEN_API_KEY")

def openai_completion(engine: str, prompt: str, stop: str):
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=[stop]
    )
    return response