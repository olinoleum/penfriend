# Standard library imports
from pathlib import Path
import os
from enum import Enum

# Third party imports
from dotenv import load_dotenv
import deepl

# Local application imports

load_dotenv(Path().cwd() / 'penfriend/.env')

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY")


class LANGUAGES(Enum):
    ENGLISH = "EN-GB"
    POLISH = "PL"


def translate(text: str, target_lang: str = "PL"):
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    translated_text = translator.translate_text(text, target_lang=target_lang)
    return translated_text
