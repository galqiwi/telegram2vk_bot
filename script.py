# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from twx.botapi import TelegramBot, ReplyKeyboardMarkup
import traceback
import vk
import time
import config

##По мотивам exlmoto.ru/writing-telegram-bots/


def get_api(access_token):
    session = vk.Session(access_token=access_token)
    return vk.API(session)

def vk_send_message(api, user_id, message, **kwargs):
    data_dict = {
        'chat_id': user_id,
        'message': message,
    }
    data_dict.update(**kwargs)
    print(data_dict)
    return api.messages.send(**data_dict)

class DigestBot(object):
    token = config.telegram_token
    stack_list = []
    admin = 'galqiwi'
    
    def __init__(self):
        vk_token = config.vk_token
        self.api = get_api(vk_token)
        res = vk_send_message(self.api, user_id=83, message="Убить всех человеков.")
        self.bot = TelegramBot(self.token)
        self.bot.get_me()
        last_updates = self.bot.get_updates(offset=0).wait()
        try:
            self.last_update_id = list(last_updates)[-1].update_id
        except IndexError:
            self.last_update_id = None
        print('last update id: {0}'.format(self.last_update_id))
    
    def process_message(self, message):
        text = message.message.text
        chat = message.message.chat
        user = message.message.sender.username
        if user is None:
            user = message.message.sender.first_name + ' ' + message.message.sender.last_name
        text = text.strip()
        digest_tag = '#digest'
        print(message.message)
        print('Got message: \33[0;32m{0}\33[0m from user: {1} '.format(text, user))
        try:
            if chat.id==-190218142:
                vk_send_message(self.api, user_id=83, message=(user + ': ' + text))
                time.sleep(0.5)
        except Exception:
            pass

    def run(self):
        print('Main loop started')
        while True:
            updates = self.bot.get_updates(offset=self.last_update_id).wait()
            try:
                for update in updates:
                    if int(update.update_id) > int(self.last_update_id):
                        self.last_update_id = update.update_id
                        self.process_message(update)
            except Exception as ex:
                print(traceback.format_exc())

if __name__ == '__main__':
    try:
        DigestBot().run()
    except KeyboardInterrupt:
        print('Exiting...')
