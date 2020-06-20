from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


"""

Веб-сервер принимает GET-запросы по адресу /albums/<artist> и выводит на экран сообщение с количеством альбомов
исполнителя artist и списком названий этих альбомов.

Веб-сервер принимает POST-запросы по адресу /albums/ и сохраняет переданные пользователем данные об альбоме.
Данные передаются в формате веб-формы. Если пользователь пытается передать данные об альбоме,
который уже есть в базе данных, обработчик запроса отвечает HTTP-ошибкой 409 и выводит соответствующее сообщение.

"""
DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

@route("/albums/<artist>")
def albums(artist):
    """
    Запрашивает сервер о поиске альбомов по заданному артисту. Выводит сообщение с результатом поиска.
    """
    albums_list = find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "{} записал {} альбомов:<br>".format(artist, len(albums_list)) # сообщение с количеством альбомов
        result += "Список альбомов {}<br>".format(artist) # заголовок перечня альбомов
        result += "<br>".join(album_names) # перечень альбомов
    return result

@route("/albums/", method="POST")
def checkAlbum(): #проверяем наличие альбома в базе данных
    """
    Запрашивает сервер о проверке наличия альбома конкретного артиста при попытке добавить его в базу.
    Выводит сообщений с результатом добавления.
    """
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album = request.forms.get("album")

    albums_list = find(artist)
    if not albums_list:
        addAlbums(year, artist, genre, album)
    else:
        session = connect_db()
        _ = session.query(Album).filter(Album.album == album).first()

        if _:
            message = "Альбом {} {} уже есть в базе данных".format(album, artist)
            return HTTPError(409, message)
        else:
            addAlbums(year, artist, genre, album)    

def addAlbums(year, artist, genre, album): 
    """
    Добавляет альбом в базу данных
    """
    session = connect_db()

    _ = Album(year=year, artist=artist, genre=genre, album=album)
    session.add(_)
    session.commit()

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)

# test data
# http -f POST localhost:8080/albums/ year=1966 artist=Beatles genre=pop album=Revolver This request causes an error 409
# http -f POST localhost:8080/albums/ year=1966 artist=Beatles genre=pop album="Guns and Roses" This request does not cause an error
# http -f POST localhost:8080/albums/ year=2020 artist=ChikiBricki genre=garbagepop album="My dictrict" This request does not cause an error
# http -f POST localhost:8080/albums/ year=2019 artist=ChikiBricki genre=garbagepop album="My girlfriend likes beer" This request does not cause an error
