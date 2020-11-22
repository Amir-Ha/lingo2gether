import random

import requests
from wordfreq import zipf_frequency

from lingo2gether.dataHandler import DataHandler
from lingo2gether.translator import Translator


class WordsAPI:
    @staticmethod
    def choose_word(words: list):
        toReplace = {}  # k=index in words, v= translated word
        current_min = 10
        chosen_index = 0
        translator = Translator()
        for word in words:
            translated = translator.translate(word).text
            if zipf_frequency(translated, 'en') == 0:  # handle invalid words
                toReplace[translated] = 10
            else:
                toReplace[translated] = zipf_frequency(translated, 'en')
            if toReplace[translated] < current_min:
                current_min = toReplace[translated]
                chosen_index = words.index(word)
        chosen_word = min(toReplace, key=toReplace.get)

        return {chosen_index: chosen_word}

    @staticmethod
    def get_examples(word: str):
        url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/examples"
        headers = {
            'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
            'x-rapidapi-key': "f7fb4a7a0fmsh28234859514bb36p1fba8fjsnbc861b316075"
        }
        response = requests.request("GET", url, headers=headers)
        return response.json()['examples']

    @staticmethod
    def create_quiz_sentences(word: str):
        examples = WordsAPI.get_examples(word)
        quiz_sentences = [example.replace(word.lower(), '___') for example in examples]
        return quiz_sentences[:3]

    @staticmethod
    def get_poll_quiz(userID):
        dh = DataHandler()
        first_index = 0
        last_index = 1000
        questions = dh.get_vocabulary(userID, first_index, last_index)
        number_choices = len(questions) % 5
        options = random.sample(questions, number_choices)
        word = random.choice(options)
        if not len(WordsAPI.get_examples(word)):
            word = random.choice(options)
        question = WordsAPI.create_quiz_sentences(word)
        while word in options:
            options.remove(word)
        options.append(word)
        random.shuffle(options)
        return {"Question": question, "Options": options, "Answer": options.index(word)}

    @staticmethod
    def get_definitions(word):
        url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/definitions"

        headers = {
            'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
            'x-rapidapi-key': "5850353b43msh2988cdc0da36a59p1f7016jsn299b6d4d233a"
        }

        response = requests.request("GET", url, headers=headers)

        return response.json()['definitions']
