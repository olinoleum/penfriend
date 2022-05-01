# Standard library imports
import os
from pathlib import Path
from enum import Enum

# Third party imports
import openai
from dotenv import load_dotenv

# Local application imports

load_dotenv(Path().cwd() / 'penfriend/.env')

OPEN_API_KEY = os.environ.get("OPEN_API_KEY")

openai.api_key = OPEN_API_KEY


class GPT3Engine(Enum):
    EASY = "text-babbage-001"
    MEDIUM = "text-curie-001"
    HARD = "text-davinci-002"


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


def openai_grammar_correction(prompt: str) -> dict:
    response = openai.Completion.create(
        engine=GPT3Engine.HARD.value,
        prompt=f"Correct this to standard English:\n\n{prompt}",
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response
