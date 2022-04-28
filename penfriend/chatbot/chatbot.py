# Standard library imports
from typing import List, Dict
import logging

# Third party imports

# Local application imports
from penfriend.openai_client import client
from penfriend.deepl_client import translate, LANGUAGES

OPENAI_ENGINES = {
    "Easy - babbage": client.GPT3Engine.EASY.value,
    "Medium - curie": client.GPT3Engine.MEDIUM.value,
    "Hard - davinci": client.GPT3Engine.HARD.value,
}

DEEPL_LANGUAGES = {
    "English": LANGUAGES.ENGLISH.value,
    "Polish": LANGUAGES.POLISH.value
}


def get_response(engine: str, current_conversation: List[Dict[str, Dict]], lang: str) -> str:

    openai_engine = OPENAI_ENGINES.get(engine, client.GPT3Engine.EASY.value)
    language = DEEPL_LANGUAGES.get(lang, LANGUAGES.ENGLISH.value)

    # If chosen language is not english, translate conversation into english so openai can understand it
    if language != LANGUAGES.ENGLISH.value:
        current_conversation = translate(current_conversation, LANGUAGES.ENGLISH.value).text

    logging.info(f"Preparing request: engine-{openai_engine}, language-{language}")

    response = client.openai_completion(openai_engine, current_conversation, "myMessage:")
    response_text = response.get("choices")[0].get("text")

    logging.info(f"Generated message: {response_text}")

    return translate(response_text).text if language != LANGUAGES.ENGLISH.value else response_text
