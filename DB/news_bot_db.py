import sqlalchemy as sq
import Fedya_news_bot.DB.config as c
from sqlalchemy.orm import sessionmaker
from Fedya_news_bot.DB.news_bot_models import create_tables, Users, Posts, Groups

DSN = f'postgresql://{c.USER}:{c.PASSWORD}@{c.HOST}:{c.PORT}/{c.NAME_DB}'
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()


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


if __name__ == '__main__':
    create_tables(engine)
    session.close()
