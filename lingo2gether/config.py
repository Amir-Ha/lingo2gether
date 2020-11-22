# Server Configuration
TOKEN = '948531097:AAEVGvOZy6_TlonD4s22U7a0nz-067WoFg0'
NGROK = 'https://63aed598.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, NGROK)
SEND_REQUEST = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
PORT = 5000
POLL_REQ = "https://api.telegram.org/bot{}/sendPoll?chat_id={}&question={}&options={}&type={}&correct_option_id={}"

# DataBase Configuration
db_HOST = "localhost"
db_USER = "root"
db_PASSWORD = "root"
db_CHARSET = "utf8"
db_NAME = "lingo2gether"
