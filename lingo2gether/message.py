from lingo2gether.parser import Parser


class Message:
    def __init__(self):
        self.chat_id = 0
        self.chat_message = ""

    def set_chat_id(self, req):
        self.chat_id = Parser.get_chat_id(req)

    def set_chat_message(self, req):
        self.chat_message = Parser.get_messsage(req)
