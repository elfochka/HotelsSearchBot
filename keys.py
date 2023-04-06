import os
from dotenv import set_key

bot_token = os.environ.get('BOT_TOKEN')
rapid_api_key = os.environ.get('RAPID_API_KEY')

set_key('.env', 'BOT_TOKEN', bot_token)
set_key('.env', 'RAPID_API_KEY', rapid_api_key)
