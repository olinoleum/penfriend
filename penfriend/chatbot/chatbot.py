# Standard library imports
from typing import List, Dict

# Third party imports

# Local application imports
from penfriend.openai_mock_client import client


def get_response(engine: str, current_conversation: List[Dict[str, Dict]]) -> str:
    current_conversation_str = ""
    # for msg in current_conversation:
    #     current_conversation_str += msg['sender']
    #     current_conversation_str += msg['message']
    #     current_conversation_str += "\n"

    response = client.openai_completion(engine, current_conversation, "You:")
    print(response)

    #current_conversation.append({"sender": "Bot:", "message": response})
    return response
