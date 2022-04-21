# Standard library imports

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
        conversation_data = request.json
        print(conversation_data['lang'])
        response = chatbot.get_response(conversation_data['engine'], conversation_data['prompt'],
                                        conversation_data['lang'])
        return make_response(jsonify(response), 200)

