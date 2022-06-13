# Standard library imports
import logging
import random
from typing import List
import datetime

# Third party imports
from flask import Blueprint, render_template, request, jsonify, make_response
from sqlalchemy import or_

# Local application imports
from penfriend import db
from penfriend.chatbot import chatbot
from penfriend.models import User, Message


main = Blueprint("main", __name__)


def uniqueid():
    seed = random.getrandbits(9)
    while True:
        yield seed
        seed += 1


unique_sequence = uniqueid()


def get_all_messages_by_user(user_id) -> List:
    messages = Message.query.filter(or_(Message.user_id == user_id,
                                        Message.receiver == user_id)).all()
    return messages


def get_msg_lang(raw_lang_data: str) -> chatbot.LANGUAGES:
    msg_lang_as_str = "Polish" if raw_lang_data else "English"
    return chatbot.DEEPL_LANGUAGES.get(msg_lang_as_str, chatbot.LANGUAGES.ENGLISH.value)


def get_corrected_grammar(msg_text: str, lang: chatbot.LANGUAGES) -> str | None:
    if lang != chatbot.LANGUAGES.ENGLISH.value:
        return None

    return chatbot.get_corrected_grammar(msg_text)


def get_sender_name(user_id: int) -> str:
    return chatbot.ChatbotPronounces.CHATBOT.value if user_id == 1 else chatbot.ChatbotPronounces.USER.value


@main.route("/")
def index():
    cookie = request.cookies.get("cookie_id")
    if cookie:
        print(cookie)
        user = User.query.filter_by(cookie_id=cookie).first()

        messages = get_all_messages_by_user(user.id)

        return render_template("index.html", messages=messages)
    else:
        cookie_id = str(next(unique_sequence))

        user = User(cookie_id=int(cookie_id))
        db.session.add(user)
        db.session.commit()
        db.session.flush()

        initial_message_en, initial_message_pl = chatbot.get_chatbot_initial_message()

        message = Message(user_id=1, receiver=user.id, msg=initial_message_en, translated_msg=initial_message_pl)
        db.session.add(message)
        db.session.commit()

        messages = get_all_messages_by_user(user.id)

        resp = make_response(render_template("index.html", messages=messages))
        resp.set_cookie("cookie_id", cookie_id)

        return resp


@main.route("/sendMsg", methods=["GET", "POST"])
def send_msg():
    if request.method == "POST":
        user = User.query.filter_by(cookie_id=request.cookies.get("cookie_id")).first()

        msg_text = request.json.get("msgText")
        msg_lang_raw = request.json.get("lang")

        msg_lang = get_msg_lang(msg_lang_raw)

        user_msg = Message(user_id=user.id, receiver=1, msg=msg_text, lang=msg_lang)

        db.session.add(user_msg)
        db.session.commit()
        db.session.flush()

        response_dict = {"msgText": user_msg.msg, "msgId": user_msg.id, "msgIsCorrected": user_msg.is_corrected}

        return make_response(jsonify(response_dict), 200)


@main.route("/correctGrammar", methods=["GET", "POST"])
def correct_grammar():
    if request.method == "POST":

        msg_id = request.json.get("msgId")
        message = Message.query.get(msg_id)

        msg_corrected = get_corrected_grammar(message.msg, message.lang)

        message.corrected_msg = msg_corrected

        db.session.commit()
        db.session.flush()

        response_dict = {"msgId": msg_id, "msgIdCorrected": message.is_corrected}

        return make_response(jsonify(response_dict), 200)


@main.route("/getResponse", methods=["GET", "POST"])
def get_response():
    if request.method == "POST":
        user = User.query.filter_by(cookie_id=request.cookies.get("cookie_id")).first()

        conversation_data = request.json

        messages = get_all_messages_by_user(user.id)

        preprocessed_msg = [{"whoWrote": get_sender_name(msg.user_id),
                             "wroteText": msg.msg} for msg in messages]

        current_conversation = chatbot.CurrentConversation(preprocessed_msg,
                                                           get_msg_lang(conversation_data.get("lang")))

        bot = chatbot.Chatbot(conversation_data['engine'], current_conversation)

        response = bot.get_chatbot_response()
        translated_response = bot.translate_response(response, chatbot.DEEPL_LANGUAGES["Polish"])

        ai_msg = Message(user_id=1, receiver=user.id, msg=response, translated_msg=translated_response)
        db.session.add(ai_msg)
        db.session.commit()
        db.session.flush()

        response_dict = {"msgText": response,
                         "msgId": ai_msg.id}

        return make_response(jsonify(response_dict), 200)


@main.route("/getTranslation", methods=["GET", "POST"])
def get_translation():
    if request.method == "POST":
        msg_id = request.json.get("msgId")

        translated_msg = Message.query.get(msg_id)

        data = {"translatedMsg": translated_msg.translated_msg,
                "orgMsg": request.json.get("orgMsg")}

        return make_response(jsonify(data), 200)


@main.route("/getCorrection", methods=["GET", "POST"])
def get_correction():
    if request.method == "POST":
        msg_id = request.json.get("msgId")
        corrected_msg = Message.query.get(msg_id)
        data = {"correctedMsg": corrected_msg.corrected_msg,
                "orgMsg": request.json.get("orgMsg"),
                "msgIsCorrected": corrected_msg.is_corrected}

        return make_response(jsonify(data), 200)
