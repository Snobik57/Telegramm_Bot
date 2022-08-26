import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True)
    chat_id = sq.Column(sq.Integer, nullable=False)
    first_name = sq.Column(sq.VARCHAR(60))
    last_name = sq.Column(sq.VARCHAR(60))
    vk_id = sq.Column(sq.Integer, nullable=False)

    def __str__(self):
        return f'{self.id}'


class Groups(Base):
    __tablename__ = 'groups'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'), nullable=False)
    name = sq.Column(sq.VARCHAR(100), nullable=False)

    user = relationship('Users', backref='groups')

    def __str__(self):
        return f"{self.id}"


class Posts(Base):
    __tablename__ = 'posts'

    id = sq.Column(sq.Integer, primary_key=True)
    group_id = sq.Column(sq.Integer, sq.ForeignKey('groups.id'), nullable=False)
    vk_id = sq.Column(sq.Integer, nullable=False)

    group = relationship('Groups', backref='posts')

    def __str__(self):
        return f"{self.vk_id}"


def create_tables(engine):
    Base.metadata.create_all(engine)

