import telebot
import time
from telebot.types import InputMediaPhoto
from Fedya_news_bot.Class.VK_user import UsersVK
from Fedya_news_bot.Class.TG_user import User_TG
from Fedya_news_bot.DB.news_bot_db import add_data, bd_get_id, bd_get_post_id
from Fedya_news_bot.DB.news_bot_models import Users, Groups, Posts


bot = telebot.TeleBot('THIS IS YOUR TOKEN TELEBOT')

user_tg = User_TG()


@bot.message_handler(commands=['start', 'help'])
def start(message, red=False):
    mes = bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}! Just do it!'
                                            f'\nВведите ваш ID Вконтакте')
    bot.register_next_step_handler(mes, user_get_vk_id)


def user_get_vk_id(message):
    user_tg.id_vk = int(message.text)
    user_tg.chat_id = int(message.chat.id)
    add_data(
        Users,
        chat_id=user_tg.chat_id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        vk_id=int(message.text)
    )

    mes = bot.send_message(user_tg.chat_id, 'Введите название группы, из которой вы хотите получать посты')
    bot.register_next_step_handler(mes, user_get_name_group)


def user_get_name_group(message):
    name_group = message.text
    user_tg.name_group = name_group
    user_id = bd_get_id(int(message.chat.id))
    add_data(
        Groups,
        user_id=user_id,
        name=name_group
    )

    mes = bot.send_message(user_tg.chat_id, 'Я готов к работе. Давайте начнем!')
    bot.register_next_step_handler(mes, send_media_group_from_sc)


def send_media_group_from_sc(message):
    while True:
        channel_name = '-1001591377404'
        user_vk = UsersVK()
        content = user_vk.get_content(user_tg.id_vk, user_tg.name_group)
        for key, con in content.items():
            if str(key) not in bd_get_post_id(user_tg.chat_id, user_tg.name_group):
                add_data(
                    Posts,
                    group_id=bd_get_id(user_tg.chat_id),
                    vk_id=key
                         )
                media = []
                count = 0
                for i in con['url']:
                    if count == 0:
                        photo = InputMediaPhoto(media=i, caption=con['text'])
                        media.append(photo)
                        count += 1
                    else:
                        photo = InputMediaPhoto(media=i)
                        media.append(photo)
                bot.send_media_group(channel_name, media=media)
        time.sleep(60)


if __name__ == "__main__":
    bot.polling(non_stop=True)
