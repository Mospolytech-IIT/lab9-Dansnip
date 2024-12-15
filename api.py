'''FASTapi'''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import add_users, add_posts, get_all_users, get_all_posts
from main import get_posts_by_user, update_user_email, update_post_content
from main import delete_post, delete_user_and_posts

app = FastAPI()

class UserCreate(BaseModel):
    """Что писать здесь ыыы, ну пусть так: модель для создания пользователя."""
    username: str
    email: str
    password: str

class PostCreate(BaseModel):
    """Модель для создания поста."""
    title: str
    content: str
    user_id: int

class UserUpdate(BaseModel):
    """Модель для обновления информации о пользователе."""
    email: str

class PostUpdate(BaseModel):
    """Модель для обновления содержимого поста."""
    content: str

@app.post("/users/")
def create_user(user: UserCreate):
    """Создает нового пользователя."""
    add_users([user.dict()])
    return {"msg": "User created"}

@app.post("/posts/")
def create_post(post: PostCreate):
    """Создает новый пост."""
    add_posts([post.dict()])
    return {"msg": "Post created"}

@app.get("/users/")
def read_users():
    """Получает список всех пользователей."""
    users = get_all_users()
    return users

@app.get("/posts/")
def read_posts():
    """Получает список всех постов."""
    posts = get_all_posts()
    return posts

@app.get("/users/{user_id}/posts/")
def read_posts_by_user(user_id: int):
    """Получает посты конкретного пользователя по его ID."""
    posts = get_posts_by_user(user_id)
    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")
    return posts

@app.put("/users/{user_id}/")
def update_user(user_id: int, user: UserUpdate):
    """Обновляет email о пользователе по его ID."""
    update_user_email(user_id, user.email)
    return {"msg": "User updated"}

@app.put("/posts/{post_id}/")
def update_post(post_id: int, post: PostUpdate):
    """Обновляет содержимое поста по ID пользоваляа ."""
    update_post_content(post_id, post.content)
    return {"msg": "Post updated"}

@app.delete("/posts/{post_id}/")
def delete_post_route(post_id: int):
    """Удаляет пост по его ID."""
    delete_post(post_id)
    return {"msg": "Post deleted"}

@app.delete("/users/{user_id}/")
def delete_user_route(user_id: int):
    """Удаляет пользователя и все его посты по его ID."""
    delete_user_and_posts(user_id)
    return {"msg": "User and their posts deleted"}
