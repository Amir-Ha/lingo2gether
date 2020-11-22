import json
import requests

from lingo2gether.config import TOKEN, POLL_REQ
from lingo2gether.dataHandler import DataHandler
from lingo2gether.translator import Translator
from lingo2gether.wordsAPI import WordsAPI
from prettytable import PrettyTable
from collections import defaultdict
import random


user_questions = {}
user_vocab_counter = defaultdict(int)


class CommandUtils:

    @staticmethod
    def print_help(*args, **vargs):
        return "Hi, I'm lingo2gether bot, I can help you learn some new words, just answer my questions with whatever you like.\n\n" \
               "You can control me by sending these commands:\n\n" \
               "/teachme: I start questioning you \n" \
               "/showvocabulary: get a list of all the words we've learned" \
               "/help: prints this message \n" \
               "/stopme: I won't ask another question for a while \n" \
               "/memorize Type /memorize <word> if you're struggling with a word that you need help remembering, " \
               "I'll ask about it again! \n" \
               "/forget: Once you've got your word down, type /forget <word> and I'll stop asking about it\n" \
               "/resume: I'll start asking questions again \n" \
               "/quiz: Ask for a quiz to review some of the words I mentioned \n" \
               "/translate: write one or more words \n\n\n" \
               "היי, אני lingo2gether, אני יכול לעזור לך ללמוד מלים חדשות, רק תענה/תעני לשאלות שלי." \
               "אתה/את יכול/ה לשלוט בי דרך הפקודות הבאות:\n\n" \
               "/teachme: אני מתחיל לשאול אותך \n" \
               "/help: מדפיס את ההסבר שאתם קוראים \n" \
               "/stopme: אני לא אשאל שאלות לפרק זמן מסויים \n" \
               "/memorize תרשום/תרשמי את המילה שקשה לזכור, " \
               "ואני אשאל/ אחזור על המילה שוב \n" \
               "/forget: תרשום/תרשמי את המילה שכבר זכרתם, ואני אפסיק לשאול על זה\n" \
               "/resume: אני אמשיך לשאול שאלות \n" \
               "/quiz: לבקש בוחן במלים שהוזכרו קודם \n" \
               "/translate: תרשום/תרשמי מילה או יותר לתרגום \n"

    @staticmethod
    def command_specialize(args, **vargs):
        data_handler = DataHandler()
        return DataHandler.specialize_word(data_handler, args[0], vargs["user_id"])

    @staticmethod
    def translate(*args):
        return Translator.translate(args[0])

    @staticmethod
    def command_forget(args, **vargs):
        data_handler = DataHandler()
        return DataHandler.data_handler_forget(data_handler, args[0], vargs["user_id"])

    @staticmethod
    def stopMe(*args):
        pass

    @staticmethod
    def quiz(*args, **vargs):
        quiz_dict = WordsAPI.get_poll_quiz(vargs['user_id'])
        res = requests.get(
            POLL_REQ.format(TOKEN, vargs['user_id'], quiz_dict["Question"], json.dumps(quiz_dict["Options"]), "quiz",
                            quiz_dict["Answer"]))
        print(res)
    # continue to the next question
    @staticmethod
    def resume(args, **vargs):
        return CommandUtils.next_question(vargs['user_id'])

    # open the questions file and read all the questions into a user's list
    @staticmethod
    def fill_list(user_id):
        with open("bot_questions.txt", 'r') as questions_file:
            lines = questions_file.readlines()
        user_questions[user_id] = lines

    # fill the questions list for the first time and return a question
    @staticmethod
    def teach_me(args, **vargs):
        CommandUtils.fill_list(vargs['user_id'])
        return CommandUtils.next_question(vargs['user_id'])

    # pick random question, pop it from user's questions list and return it
    # fill list again if it's empty
    @staticmethod
    def next_question(user_id):
        if not user_id in user_questions.keys():  # if user doesn't exist inside the list of questions
            CommandUtils.fill_list(user_id)
        user_list = user_questions[user_id]
        index = random.randint(0, len(user_list))
        random_question = user_list.pop(index)
        if not len(user_list):
            CommandUtils.fill_list(user_id)
        return random_question

    @staticmethod
    def replace_words(words_list, chat_id):
        # Receive translated words from WordsAPI
        translated_dict = WordsAPI.choose_word(words_list)
        dh = DataHandler()
        for index in translated_dict:
            words_list[int(index)] = translated_dict[index].strip('?')
            dh.add_word(words_list[int(index)], chat_id)
        return ' '.join(words_list)

    # get from data handler list of words from vocabulary
    @staticmethod
    def show_vocabulary(args, **vargs):
        user_vocab_counter[vargs['user_id']] += 10
        next_set = user_vocab_counter[vargs['user_id']]
        dh = DataHandler()

        words_list = dh.get_vocabulary(vargs['user_id'], next_set - 10, next_set)

        # check if there is truly exist a next vocab, if doesn't exist enough, next time we should restart the counter
        if len(words_list) < 10:
            user_vocab_counter[vargs['user_id']] = 0

        # Pretty Table - put the words in
        prettyWords = PrettyTable()
        prettyWords.add_column('Word', words_list)
        prettyWords.add_column('Definition',
                               ([random.choice(WordsAPI.get_definitions(word))['definition'] for word in words_list]))
        return prettyWords

