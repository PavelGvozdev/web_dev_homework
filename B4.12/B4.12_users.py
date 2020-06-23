"""
Домашнее задание модуля В4.12. Автор: Павел Гвоздев
Модуль users.py, который регистрирует новых пользователей. Скрипт запрашивает следующие данные:

    имя
    фамилию
    пол
    адрес электронной почты
    дату рождения
    рост

Данные о пользователях сохраняются в таблице user базы данных sochi_athletes.sqlite3.
"""
# импортируем модули для работы с базой данных 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

try:
    # константа, указывающая способ соединения  с базой данных
    DB_PATH = "sqlite:///sochi_athletes.sqlite3"
except FileNotFoundError as err:
    print('Файл базы данных не найден', err)    

# описываем базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    user("id" integer primary key autoincrement, "first_name" text, "last_name" text,
     "gender" text, "email" text, "birthdate" text, "height" real)
    """
    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.INTEGER, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.TEXT)
    # фамилия пользователя
    last_name = sa.Column(sa.TEXT)
    # пол пользователя
    gender = sa.Column(sa.TEXT)
    # адрес электронной почты пользователя
    email = sa.Column(sa.TEXT)
    # день рождения пользователя
    birthdate = sa.Column(sa.TEXT)
    # рост пользователя
    height = sa.Column(sa.REAL)
    

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def request_data():
    """
    Запрашивает у пользователя данные и возвращает на их основе объект User
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("Tеперь пол: ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    birthdate = input("И дата твоего дня рождения в формате ГГГГ-ММ-ДД: ")
    height = float(input("И последнее, твой рост в формате М.СМ: "))
    
    # создаем нового пользователя
    user = User(
        first_name = first_name,
        last_name = last_name,
        gender = gender,
        email = email,
        birthdate =  birthdate,
        height = height
    )
    # возвращаем созданного пользователя
    return user

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    В текущей версии поддерживает только один режим: 1 - добавление нового пользователя
    """
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выбери режим.\n1 - ввести данные нового пользователя\n")
    # проверяем режим
    if mode == "1":
        # запрашиваем данные пользоватлея
        user = request_data()
        # добавляем нового пользователя в сессию
        session.add(user)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
    else:
        print("Некорректный режим:")

if __name__ == "__main__":
    main()