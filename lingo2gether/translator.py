from googletrans import Translator

translator = Translator()


class Translator:
    # get translation from API .
    @staticmethod
    def translate(word):
        return translator.translate(word)
