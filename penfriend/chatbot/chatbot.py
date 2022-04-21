# Standard library imports
from typing import List, Dict

# Third party imports

# Local application imports
from penfriend.openai_client import client
from penfriend.deepl_client import translate


def get_response(engine: str, current_conversation: List[Dict[str, Dict]], lang: str) -> str:

    if lang != "EN-GB":
        current_conversation = translate(current_conversation, "EN-GB").text

    print(current_conversation)
    response = client.openai_completion(engine, current_conversation, "You:")

    response_text = response.get("choices")[0].get("text")

    return translate(response_text).text if lang != "EN-GB" else response_text
