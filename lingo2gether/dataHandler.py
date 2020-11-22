import pymysql
import requests

from lingo2gether import config


class DataHandler:

    def __init__(self):
        # Open database connection
        self.connection = pymysql.connect(
            host=config.db_HOST,
            user=config.db_USER,
            password=config.db_PASSWORD,
            db=config.db_NAME,
            charset=config.db_CHARSET,
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute_query(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
        except:
            print(f"Error in query = {query}.")

    def select_record(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except:
            print(f"DB Error in select query = {query}.")

    def specialize_word(self, word, user_id):
        update_query = f'UPDATE words SET special = {1} WHERE wordName = "{word}" and userID = {user_id}'
        self.execute_query(update_query)
        return f"{word} is saved as a memorized word"

    def data_handler_forget(self, word, user_id):
        update_query = f'UPDATE words SET special = {0} WHERE wordName = "{word}" and userID = {user_id}'
        self.execute_query(update_query)
        return f"{word} was removed from memorized words"

    def add_word(self, word, user_id):
        if len(DataHandler.get_examples_2(word)):
            insert_query = f'INSERT INTO words (special, wordName, userID) VALUES ({0}, "{word.lower()}", {user_id})'
            self.execute_query(insert_query)

    # get the words from the database and make a pretty table then return it
    def get_vocabulary(self, user_id, first_index, last_index):
        get_words_query = f'SELECT wordName FROM words WHERE userID = {user_id} LIMIT {first_index},{last_index}'
        words_result_list = self.select_record(get_words_query)
        words_list = []
        for word in words_result_list:
            words_list.append(word["wordName"])
        return words_list

    @staticmethod
    def get_examples_2(word: str):
        url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/examples"
        headers = {
            'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
            'x-rapidapi-key': "f7fb4a7a0fmsh28234859514bb36p1fba8fjsnbc861b316075"
        }
        response = requests.request("GET", url, headers=headers)
        return response.json()['examples']
