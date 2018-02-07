
# coding: utf-8

# In[2]:


import requests  
from wikiapi import WikiApi
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
    
    def wiki_search(self, text):
        wiki = WikiApi()
        results = wiki.find(text)
        article = wiki.get_article(results[0])
        return article

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
        try:
            if 'wiki' in last_chat_text.lower():
                a = last_chat_text.lower()
                txt = a.replace("wiki ","")
                head = greet_bot.wiki_search(txt).heading
                desc = greet_bot.wiki_search(txt).summary
                content = greet_bot.wiki_search(txt).content
                url = greet_bot.wiki_search(txt).url
                if 'may refer to' in desc:
                    greet_bot.send_message(last_chat_id, 'There are several options found, please use URL below to choose')
                    greet_bot.send_message(last_chat_id, url)
                else:
                    greet_bot.send_message(last_chat_id, head)
                    greet_bot.send_message(last_chat_id, desc)
                    greet_bot.send_message(last_chat_id, url)
        except Exception as e2:
                pass
                print(e2)
                greet_bot.send_message(last_chat_id, 'there is nothing in Wiki, please input only English words')
            
        if  last_chat_text.lower() == 'сдр' and last_chat_name.lower() == 'boris':
            greet_bot.send_message(last_chat_id, 'С днем рождения, Арсенушка! Радости, улыбок, безмерного и бесконечного счастья. Желаю заиметь побольше рычагов управления своей жизни, чтобы мог влиять на все! Желаю тебе оказываться всегда в нужном месте и в нужное время!')
            greet_bot.send_photo(last_chat_id, 'https://fresh-cards.ru/resized/images/stories/virtuemart/product/otkrytka-s-dnyom-rozhdeniya-komputerschikou.jpg')
            
#       if 'уходи' in last_chat_text.lower():
#            greet_bot.send_photo(last_chat_id, 'https://pp.userapi.com/c540108/v540108844/815c/0Ei7pxV3gyE.jpg')
#        if 'ретард' in last_chat_text.lower() or 'тупой' in last_chat_text.lower():
#            greet_bot.send_photo(last_chat_id, 'https://i.imgur.com/xeYzahch.jpg')
#        if 'alert' in last_chat_text.lower() or 'тревога' in last_chat_text.lower():
#            greet_bot.send_photo(last_chat_id, 'https://i.imgur.com/QASOJat.gif')
#        if 'шта' in last_chat_text.lower() or 'wat' in last_chat_text.lower():
#            greet_bot.send_photo(last_chat_id, 'https://pbs.twimg.com/media/ByObDPcIQAAoG2V.jpg')
#        if 'лел' in last_chat_text.lower():
#            greet_bot.send_message(last_chat_id, 'не надо тут лел')
#        if last_chat_text.lower() in badwords:
#            greet_bot.send_message(last_chat_id, 'сам ты {}'.format(last_chat_text))

            
        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()


