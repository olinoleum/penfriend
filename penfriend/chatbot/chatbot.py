# Standard library imports
from typing import List, Dict
import logging
from enum import Enum
import re

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


class ChatbotPronounces(Enum):
    CHATBOT = "fromThem:"
    USER = "myMessage:"


class Chatbot:
    def __init__(self, engine: str, current_conversation: str, lang: str):
        self.engine = OPENAI_ENGINES.get(engine, client.GPT3Engine.EASY.value)
        self.lang = DEEPL_LANGUAGES.get(lang, LANGUAGES.ENGLISH.value)
        self.current_conversation = current_conversation
        self.current_conversation_english = self.get_current_conversation_english()

    def is_conversation_english(self):
        return True if self.lang == LANGUAGES.ENGLISH.value else False

    def get_current_conversation_english(self):
        if not self.is_conversation_english():
            return translate(self.current_conversation, LANGUAGES.ENGLISH.value).text
        else:
            return self.current_conversation

    def translate_response(self, response: str, lang: None | LANGUAGES = None) -> str:
        lang = self.lang if lang is None else lang
        return translate(response, lang).text

    @property
    def split_conversation(self):
        delimiters = re.compile(f"{ChatbotPronounces.CHATBOT.value}|{ChatbotPronounces.USER.value}")
        return delimiters.split(self.current_conversation_english)

    @staticmethod
    def extract_response_text(response_obj: dict) -> str:
        return response_obj.get("choices")[0].get("text")

    def get_chatbot_response(self):

        logging.info(f"Preparing request: engine-{self.engine}, language-{self.lang}")

        response = client.openai_completion(self.engine,
                                            self.current_conversation_english,
                                            ChatbotPronounces.USER.value
                                            )

        extracted_response_text = self.extract_response_text(response)

        logging.info(f"Generated message: {extracted_response_text}")

        return extracted_response_text if self.is_conversation_english() else self.translate_response(extracted_response_text)

    def get_corrected_grammar(self) -> str:

        logging.debug(f"Split Conversation looks like {self.split_conversation}")

        last_message = self.split_conversation[-2]

        response = client.openai_grammar_correction(last_message)
        extracted_response_text = self.extract_response_text(response)

        logging.info(f"Message: {last_message} corrected into {extracted_response_text}")

        return extracted_response_text
