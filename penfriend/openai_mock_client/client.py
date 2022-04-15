# Standard library imports
import os

# Third party imports
import openai

# Local application imports

#openai.api_key = os.getenv("OPEN_API_KEY")


def mock_response(engine: str, prompt: str, temperature: float, max_tokens: int, top_p: float,
        frequency_penalty: float, presence_penalty: float, stop: list) -> str:
    return f"Response created with {engine} engine, {prompt} as a prompt"


def openai_completion(engine: str, prompt: str, stop: str) -> str:
    response = mock_response(
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
