'''БД'''
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import relationship

# Задаем путь к вашей существующей базе данных, нужно заменить на свою путь
DATABASE_URL = 'sqlite:///C:/Users/finpy/Desktop/лабы питон/лаба9/lab9-Dansnip/app.db'

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

class User(Base):
    """Модель пользователя."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    posts = relationship('Post', back_populates='user')

class Post(Base):
    """Модель поста."""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='posts')

# Создаем таблицы в базе данных, если они не существуют
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)

def add_users(users_data):
    """Добавляет пользователей в базу данных."""
    session = Session()
    for user_data in users_data:
        new_user = User(**user_data)
        session.add(new_user)
    session.commit()
    session.close()

def add_posts(posts_data):
    """Добавляет посты в базу данных."""
    session = Session()
    for post_data in posts_data:
        new_post = Post(**post_data)
        session.add(new_post)
    session.commit()
    session.close()

def get_all_users():
    """Получает всех пользователей из базы данных."""
    session = Session()
    users = session.query(User).all()
    session.close()
    return users

def get_all_posts():
    """Получает все посты из базы данных с пользователями."""
    session = Session()
    posts = session.query(Post).join(User).all()
    session.close()
    return posts

def get_posts_by_user(user_id):
    """Получает все посты конкретного пользователя по его ID."""
    session = Session()
    posts = session.query(Post).filter(Post.user_id == user_id).all()
    session.close()
    return posts

def update_user_email(user_id, new_email):
    """Обновляет адрес электронной почты пользователя по его ID."""
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        session.commit()
    session.close()

def update_post_content(post_id, new_content):
    """Обновляет содержимое поста по его ID."""
    session = Session()
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        session.commit()
    session.close()

def delete_post(post_id):
    """Удаляет пост по его ID."""
    session = Session()
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        session.delete(post)
        session.commit()
    session.close()

def delete_user_and_posts(user_id):
    """Удаляет пользователя и все его посты по его ID."""
    session = Session()
    posts = session.query(Post).filter(Post.user_id == user_id).all()
    for post in posts:
        session.delete(post)
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
    session.close()
