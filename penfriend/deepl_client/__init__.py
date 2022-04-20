# Standard library imports
from pathlib import Path
import os

# Third party imports
from dotenv import load_dotenv
import deepl

# Local application imports

load_dotenv(Path().cwd() / 'penfriend/.env')

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY")


def translate(text: str, target_lang: str = "PL"):
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    translated_text = translator.translate_text(text, target_lang=target_lang)
    print(translated_text)
    return translated_text
