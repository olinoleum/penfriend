# Standard library imports
from typing import List, Dict

# Third party imports

# Local application imports
from penfriend.openai_client import client


def get_response(engine: str, current_conversation: List[Dict[str, Dict]]) -> str:

    response = client.openai_completion(engine, current_conversation, "You:")

    return response.get("choices")[0].get("text")
