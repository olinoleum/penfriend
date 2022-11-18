# Standard library imports
from typing import List, Dict, Tuple
import logging
from enum import Enum
from dataclasses import dataclass
import random

# Third party imports

# Local application imports
from penfriend import db
from penfriend.openai_client import client
from penfriend.deepl_client import translate, LANGUAGES

OPENAI_ENGINES = {
    "Easy": client.GPT3Engine.EASY.value,
    "Mid": client.GPT3Engine.MEDIUM.value,
    "Advanced": client.GPT3Engine.HARD.value,
}

DEEPL_LANGUAGES = {
    "English": LANGUAGES.ENGLISH.value,
    "Polish": LANGUAGES.POLISH.value
}


class ChatbotPronounces(Enum):
    CHATBOT = "fromThem"
    USER = "myMessage"


@dataclass
class CurrentConversation:
    current_conversation: List[Dict[str, str]]
    lang: LANGUAGES

    @property
    def conversation_as_str(self) -> str:
        preprocessed_list = [f"{message['whoWrote']}: {message['wroteText']}" for message in self.current_conversation]
        joined_list = "\n".join(preprocessed_list)

        return f"{joined_list}\nfromThem:"

    @property
    def is_conversation_english(self) -> bool:
        return True if self.lang == LANGUAGES.ENGLISH.value else False

    def get_current_conversation_english(self) -> str:
        if not self.is_conversation_english:
            return translate(self.conversation_as_str, LANGUAGES.ENGLISH.value).text
        else:
            return self.conversation_as_str


class Chatbot:
    """
    Class that handles the interaction with chatbot
    """
    def __init__(self, engine: str, current_conversation: CurrentConversation):
        self.engine = OPENAI_ENGINES.get(engine, client.GPT3Engine.EASY.value)
        self.current_conversation = current_conversation

    def translate_response(self, response: str, lang: None | LANGUAGES = None) -> str:
        lang = self.current_conversation.lang.value if lang is None else lang
        return translate(response, lang).text

    def get_chatbot_response(self) -> str:

        logging.info(f"Preparing request: engine-{self.engine}, language-{self.current_conversation.lang}")

        response = client.openai_completion(self.engine,
                                            self.current_conversation.get_current_conversation_english(),
                                            ChatbotPronounces.USER.value
                                            )

        extracted_response_text = extract_response_text(response)

        logging.info(f"Generated message: {extracted_response_text}")

        return extracted_response_text if self.current_conversation.is_conversation_english else self.translate_response(extracted_response_text)


def get_corrected_grammar(msg) -> str:
    response = client.openai_grammar_correction(msg)
    extracted_response_text = extract_response_text(response)

    return extracted_response_text


def extract_response_text(response_obj: dict) -> str:
    return response_obj.get("choices")[0].get("text")


def get_chatbot_initial_message() -> Tuple[str, str]:
    messages = [
        ("Hi, how are you doing?", "Hej, jak się masz?"),
        ("Hello, what's up?", "Siema, co tam słychać?"),
        ("Hello, what is your favorite movie?", "Witaj, jaki jest Twój ulubiony film?")
    ]

    return random.choice(messages)
