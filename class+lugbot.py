
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
    
    def send_photo(self, chat_id, photo):
        params = {'chat_id': chat_id, 'photo': photo}
        method = 'sendPhoto'
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
        try:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['from']['first_name']
            print (last_chat_text)
            print (last_chat_id)
            print (last_chat_name)
        except Exception as e:
            pass
            print(e)
        
        if last_chat_text == 'У':
            greet_bot.send_photo(last_chat_id, 'https://pp.userapi.com/c540108/v540108844/815c/0Ei7pxV3gyE.jpg')
        elif last_chat_text == 'R':
            greet_bot.send_photo(last_chat_id, 'https://web.telegram.org/86194106-93ac-40d4-8126-03f865f15540')
            
            
#        if last_chat_name == 'PhazMinze':
#            greet_bot.send_message(last_chat_id, 'Даур, не надо')
#        elif last_chat_name == 'Arsen':
#            greet_bot.send_message(last_chat_id, 'Не слушайте его')
#        elif last_chat_name == 'Boris':
#            greet_bot.send_message(last_chat_id, 'Он прав')
            
#        if last_chat_text.lower() in badwords:
#            greet_bot.send_message(last_chat_id, 'сам ты {}'.format(last_chat_text))
#        elif last_chat_text.lower() == 'боря хуй':
#            greet_bot.send_message(last_chat_id, 'сам ты, Сережа, хуй')
#        else:
#           greet_bot.send_message(last_chat_id, last_chat_text)

            
        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()

