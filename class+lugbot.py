
# coding: utf-8

# In[2]:


import requests  

import datetime


# In[3]:

token = '496491775:AAEAXNyNrQojPSwmcOEgaqk3WkTo2hf7_5w'

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=10):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return last_update


# In[4]:


greet_bot = BotHandler(token)  
greetings = ('hello', 'hi', 'greetings', 'sup')  
badwords = ('шакал', 'толстый', 'свинья', 'жирный', 'попа', 'жопа', 'тварь', 'тупой', 'ишак', 'дурак', 'балда', 'fuck you', 'гавно', 'ублюдок', 'баран', 'идиот')
now = datetime.datetime.now()


def main():  
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()
        if not last_update:
            continue
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']


        if last_chat_text.lower() in badwords:
            greet_bot.send_message(last_chat_id, 'сам ты {}'.format(last_chat_text))
        elif last_chat_text.lower() == 'боря хуй':
            greet_bot.send_message(last_chat_id, 'сам ты, Сережа, хуй')
        else:
            greet_bot.send_message(last_chat_id, last_chat_text)
                
        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()

