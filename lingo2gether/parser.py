class Parser:
    @staticmethod
    def get_messsage(req):
        return (req['message']['text']).split()

    @staticmethod
    def get_chat_id(req):
        return req['message']['chat']['id']

    @staticmethod
    def get_type_message(req):
        if "message" in req:
            return "message"
        elif "poll" in req:
            return "poll"
