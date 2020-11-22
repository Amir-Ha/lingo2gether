import requests
from flask import Flask, Response, request

from lingo2gether.command import Command
from lingo2gether.command_utils import CommandUtils
from lingo2gether.config import PORT, TELEGRAM_INIT_WEBHOOK_URL, TOKEN, SEND_REQUEST
from lingo2gether.parser import Parser

app = Flask(__name__)


@app.route('/sanity')
def sanity():
    return "Server is running"


def establish_connection():
    requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/message', methods=["POST"])
def handle_message():
    try:
        req = request.get_json()
        type_message = Parser.get_type_message(req)

        if type_message is "message":
            parsed_message = Parser.get_messsage(req)
            chat_id = Parser.get_chat_id(req)  # User ID
            message = "default_value"
            if parsed_message[0][0] == '/':  # check if input is command.
                command = parsed_message[0]
                args = parsed_message[1:]
                message = Command.execute(command, args, user_id=chat_id)
            else:  # call functions related to the normal message, BOT JOB, Ask Questions ....
                message = CommandUtils.replace_words(parsed_message, chat_id)
                message += "\n" + CommandUtils.next_question(chat_id)
            if message:  # in order to avoid performing Poll response
                res = requests.get(SEND_REQUEST.format(TOKEN, chat_id, message))
        elif type_message is "poll":
            pass

        return Response("success")
    except Exception as e:
        return Response("Error")


if __name__ == '__main__':
    establish_connection()
    app.run(port=PORT)
