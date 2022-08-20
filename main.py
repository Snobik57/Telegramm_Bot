import telebot
import sqlalchemy as sq
import time
import config as c
from VK_user import *
from telebot.types import InputMediaPhoto
from sqlalchemy.orm import sessionmaker
from news_bot_models import Users, Groups, Posts, create_tables


bot = telebot.TeleBot('THIS IS YOUR TOKEN TELEBOT')
DSN = f'postgresql://{c.USER}:{c.PASSWORD}@{c.HOST}:{c.PORT}/{c.NAME_DB}'
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()
create_tables(engine)


def add_data(model, **columns_values):
    session.add(model(**columns_values))
    session.commit()


def bd_get_id(chat_id):
    query = session.query(Users).filter(Users.chat_id == chat_id).all()
    for output in query:
        return str(output)


def bd_get_post_id(chat_id, name_group):
    posts = []
    query = session.query(Posts)
    query = query.join(Groups)
    query = query.join(Users)
    query = query.filter(Users.chat_id == chat_id, Groups.name == name_group).all()
    for output in query:
        posts.append(str(output))
    return posts


class User_TG:
    def __init__(self):
        self.chat_id = None
        self.id_vk = None
        self.name_group = None


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


session.close()


if __name__ == "__main__":
    bot.polling(non_stop=True)
