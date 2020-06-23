"""
    Домашнее задание модуля В4.12. Автор: Павел Гвоздев
    Модуль find_athlete.py ищет ближайшего к пользователю атлета. Логика работы модуля такова:

    Запрашивает идентификатор пользователя;
    если пользователь с таким идентификатором существует в таблице user, то выводит на экран двух атлетов:
    ближайшего по дате рождения к данному пользователю и ближайшего по росту к данному пользователю;
    если пользователя с таким идентификатором нет, выводит соответствующее сообщение.

    Примечание: в тестовой базе данных sochi_athletes.sqlite3 отсутствует значение роста по меньшей мере у одного спортсмена.
    Для обработки этой не штатной ситуации в программу добавлены соответствующие инструкции.

"""
# импортируем модули для работы с базой данных
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# импортируем модули для работы с датами для обработки др
import datetime 

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

class Athelete(Base):
    """
    Описывает структуру таблицы athlete для хранения данных и результатов спортсменов
    athelete("id" integer primary key autoincrement, "age" integer,"birthdate" text,"gender" text,
    "height" real,"name" text,"weight" integer,"gold_medals" integer,"silver_medals" integer,
    "bronze_medals" integer,"total_medals" integer,"sport" text,"country" text)
    
    """
    __tablename__= 'athelete'
    id = sa.Column(sa.INTEGER, primary_key=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.TEXT)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.TEXT)
    country = sa.Column(sa.TEXT)

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

def find_user(id, session):
    """
    Производит поиск пользователя в таблице user по заданному идентифекатору.
    
    """
    # находим все записи в таблице User, у которых поле User.id совпадает с параметром id
    user = []
    
    for id, height, birthdate in session.query(User.id, User.height, User.birthdate).filter(User.id == id):
        user.append(id)
        user.append(height)
        user.append(birthdate)
    
    try:
        if user:
            # ищем в базе
            target_a = find_athlete(user, session)
            
            # возвращает текст с ближайшими атлетами
            return 'Пользователь с идентификатором {0}. Ближайший к пользователю спортсмен по росту: {1}, его рост {2}. Ближайший к пользователю спортсмен по дню рождения: {3}, его день рождения {4}'.format(user[0], target_a[0], target_a[1], target_a[2], target_a[3]) 
        else:
            return "Пользователь с идетификатором {} не найден.".format(id)    
    except IndexError:
        print("Пользователь с идетификатором {} не найден.".format(id))

def find_athlete(user, session):
    """
    Производит поиск атлета, ближайшего по дате рождения к данному пользователю
    и атлета, ближайшего по росту к данному пользователю.
    Возвращает список с именами и целевыми значениями найденных спортсменов
    
    """
    # создаем список ростов всех атлетов
    height_list =  [athelete.height for athelete in session.query(Athelete).all()] 
    # вычисляем разницу между ростом пользователя и ростом каждого спортсмена.
    # создаем список абсолютных значений этих разниц
    list_of_h = []
    for height in height_list:
        if isinstance(height, float): # проверяем валидность данных
            list_of_h.append(abs(user[1] - height))
        else:
            # для невалидных данных добавляем заведомо максимальное значение для совпадения 
            # порядкa элементов в списках height_list и list_of_h
            list_of_h.append(200) 
    # получаем индекс, по которому содержится минимальная разница
    result_index = list_of_h.index(min(list_of_h))  
    # Предполагая, что порядок элементов в списках height_list и list_of_h одинаков, получаем искомый рост
    target_h = height_list[result_index]
    
    # находим атлета с ближайшим ростом
    target_a = []
    temp = session.query(Athelete).filter(Athelete.height == target_h).first()
    target_a.append(temp.name)
    target_a.append(temp.height)
    
    # создаем список др всех атлетов
    birthdate_list =  [athelete.birthdate for athelete in session.query(Athelete).all()]
    # вычисляем разницу между др пользователя и др каждого спортсмена.
    # создаем список абсолютных значений этих разниц
    list_of_bd = []
    user_bd = datetime.datetime.strptime(user[2], '%Y-%m-%d')
    for birthdate in birthdate_list:
        birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
        list_of_bd.append(abs(user_bd - birthdate))
    # получаем индекс, по которому содержится минимальная разница
    result_index = list_of_bd.index(min(list_of_bd))
    # Предполагая, что порядок элементов в списках height_list и list_of_bd одинаков, получаем искомый рост
    target_bd = birthdate_list[result_index]
    # находим атлета с ближайшим ростом
    temp = session.query(Athelete).filter(Athelete.birthdate == target_bd).first()
    target_a.append(temp.name)
    target_a.append(temp.birthdate)
    return target_a

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    В текущей версии поддерживает только один режим: 1 - поиск ближайшего к пользователю атлета
    
    """
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выбери режим.\n1 - поиск ближайшего к пользователю атлета\n")
    # проверяем режим
    if mode == "1":
        # выбран режим поиска, запускаем его
        id = input("Введи идентификатор пользователя для поиска: ")
        # вызываем функцию поиска по идентификатору
        text = find_user(id, session)
        # вызываем функцию печати на экран результатов поиска
        print(text)
    else:
        print("Некорректный режим:")

if __name__ == "__main__":
    main()