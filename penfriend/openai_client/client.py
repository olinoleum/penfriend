# Standard library imports
import os
from pathlib import Path

# Third party imports
import openai
from dotenv import load_dotenv

# Local application imports

load_dotenv(Path().cwd() / 'penfriend/.env')

OPEN_API_KEY = os.environ.get("OPEN_API_KEY")

openai.api_key = OPEN_API_KEY


def openai_completion(engine: str, prompt: str, stop: str) -> dict:

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