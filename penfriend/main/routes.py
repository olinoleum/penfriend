# Standard library imports
import logging

# Third party imports
from flask import Blueprint, render_template, request, jsonify, make_response

# Local application imports
from penfriend.chatbot import chatbot


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/getResponse", methods=["GET", "POST"])
def get_response():
    if request.method == "POST":
        response_dict = {}
        conversation_data = request.json
        bot = chatbot.Chatbot(conversation_data['engine'],
                              conversation_data['prompt'],
                              conversation_data['lang']
                              )
        response = bot.get_chatbot_response()

        response_dict.update({"chatbotResponse": response})

        if conversation_data["langMistakes"] == "Show me":
            corrected_message = bot.get_corrected_grammar()
            response_dict.update({"correctedMessage": corrected_message})

        if conversation_data["translate"] == "Yes":
            logging.info("translating last response")
            translated_response = bot.translate_response(response, chatbot.DEEPL_LANGUAGES["Polish"])
            response_dict.update({"translatedResponse": translated_response})

        return make_response(jsonify(response_dict), 200)

