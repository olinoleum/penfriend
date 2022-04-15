# Standard library imports

# Third party imports
from flask import Blueprint, render_template, request

# Local application imports
from penfriend.chatbot import chatbot

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/getResponse", methods=["GET", "POST"])
def get_response():
    if request.method == "POST":
        current_conversation = request.json
        response = chatbot.get_response(current_conversation)
        print(response)
