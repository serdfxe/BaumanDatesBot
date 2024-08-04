import random
import string
from pythondi import inject

from app.models.profile.repository import ProfileRepo
from app.models.user.repository import UserRepo
from utils.db import *
from utils.db.uow import UOW
from utils.di import init_di

import click

init_di()

# Предполагаем, что у нас есть некоторые базовые данные для генерации имен и фамилий
FIRST_NAMES = ["Алексей", "Ирина", "Сергей", "Ольга", "Дмитрий", "Мария", "Анна", "Максим", "Екатерина", "Светлана"]
LAST_NAMES = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Федоров", "Морозов", "Лебедев", "Попов", "Ковалев"]

def generate_random_username(first_name: str, last_name: str) -> str:
    # Генерируем логин в формате "фамилия.имя<случайный постфикс>"
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    return f"{last_name.lower()}.{first_name.lower()}{random_suffix}"

def generate_random_email(username: str) -> str:
    domains = ["example.com", "test.com", "mail.com"]
    random_domain = random.choice(domains)
    return f"{username}@{random_domain}"

@click.command()
@click.option('--n', default=100)
@inject()
def create_random_users(n: int, user_repo: UserRepo, profile_repo: ProfileRepo, uow: UOW):
    for i in range(1, n + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = generate_random_username(first_name, last_name)
        email = generate_random_email(username)
        
        profile_repo.session = user_repo.session
        
        with uow(user_repo):
            # Создание пользователя
            user = user_repo.create(
                id=i,
                first_name=first_name,
                last_name=last_name,
                username=username,
                role='user',
                banned=False,
                email=email,
                verified=True
            )
            
            uow.commit()
            
            # Генерация профиля
            age = random.randint(18, 60)  # Генерируем случайный возраст
            sex = random.choice(["male", "female"])  # Генерация пола
            description = "Описание пользователя {} {}".format(first_name, last_name)
            photo = "url_to_photo_{}.jpg".format(i)  # Пример URL фото, можно заменить на реальный
            
            profile_repo.create(
                user_id=user.id,
                name=f"{first_name} {last_name}",
                age=age,
                sex=sex,
                description=description,
                photo=photo
            )
            
            uow.commit()
        
if __name__ == "__main__":
    create_random_users()