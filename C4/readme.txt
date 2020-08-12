#Для работы с Vue надо установить пакет Vue CLI:#
$sudo npm install -g @vue/cli@3.9.3
Флаг -g означает «установить глобально в систему»

#config client#
$vue create client

Settings:
Vue CLI v3.9.3
? Please pick a preset: Manually select features
? Check the features needed for your project: Babel, Router, Linter
? Use history mode for router? Yes
? Pick a linter / formatter config: Airbnb
? Pick additional lint features: Lint on save
? Where do you prefer placing config for Babel, PostCSS, ESLint, etc.? In package.json
? Save this as a preset for future projects? (y/N) No

#Run client and create project#
$ cd client
$ npm run serve

Comments: The page is available at http://localhost:8080/
В public/index.html только строчка <div id="app"></div> внутри body. Эта строчка — основная точка, к которой Vue будет цепляться своим содержимым. Vue парсит код и создаёт виртуальный DOM, который потом преобразуется в "реальный" DOM.
В папке src несколько важных файлов:
    main.js содержит код, который обработает и создаст собственно Vue-приложение;
    App.vue — основной компонент приложения.
    src/components находятся "компоненты",
    views/ содержит элементы интерфейса.
    assets/ содержит все статические файлы
    router.js — файл, где различные ссылки привязываются к конкретным компонентам.

#Creating components#
1. Create file *.vue in /components

2. In file client/src/router/index.js add:
    import Fetch from '../components/Fetch.vue';
    and in const routes:
    {
      path: '/fetch',
      name: 'fetch',
      component: Fetch,
    }

#For Make http requests from server install axios#
$cd client
$npm install axios@0.18.0

Comments: Чтобы использовать axios внутри <script>, надо ее импортировать: import axios from 'axios';
Структура get-запроса:
axios.get('/user?ID=12345')
    .then(function (response) {
        // успешная часть
    })
    .catch(function (error) {
        // код, который выполняется если была ошибка доступа
    })
    .finally(function () {
        // код, который будет выполнен всегда
    });
finally и catch можно не использовать, а сами функции тоже определить как отдельные элементы
    function successProcessing(response) {
    console.log(response);
}

axios.get('/user', {params: {ID: 12345}}).then(successProcessing);

Структура post-запроса:
    axios.post('/user', {
        firstName: 'Пиотрек',
        lastName: 'Кржымпштновский'
    })
    .then(function (response) {
        console.log(response);
    })
    .catch(function (error) {
        console.log(error);
    });

Comments: Метод created() определяет поведение компонента при загрузке

#Написание своего backend'a с заглушкой вместо базы данных на bottle#
В той же папке, где создана папка для фронтенда с client, нужно создать виртуальное окружение, установить в него bottle и запустить наш сервер (server.py)
Создайте окружение:
$python3 -m venv backend_venv

Активируйте созданное окружение:
$source backend_venv/bin/activate

Установите в нём bottle:
$pip install bottle

Запустить сервер:
$python3 server.py

Comments: декораторы bottle: @bottle.route("/api/tasks/")

#server#
Так как клиент крутится на порту 8080, надо указать явно какой-то порт, не совпадающий с ним, когда мы запускаем сервер: bottle.run(host="localhost", port=5000)
В качестве базы данных выступает словарик tasks_db с объектами TodoItem, где ключом являются ID этих задач.
Мы хотим возвращать в соответствующем обработчике JSON, и поэтому надо доопределить метод to_dict ❺, который будет преобразовывать наши объекты TodoItem в словари.
 Мы будем использовать их для генерации ответа обработчику по пути /api/tasks/.

#Соединяем back и front#
Надо указать путь получения данных: const dataURL = 'http://localhost:5000/api/tasks/';

Comments: Для разрешения некорректных CORS-заголовков надо, либо разрешить все заголовки: bottle.response.headers['Access-Control-Allow-Origin'] = '*', либо разрешить ходить с определенного адреса: bottle.response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'

Для правильной работы с CORS-заголовками надо поставить пакет bottle-cors (https://pypi.org/project/bottle-cors/):
$pip install bottle-cors

импортировать его в сервер:
from truckpad.bottle.cors import CorsPlugin, enable_cors

И добавить декоратор @enable_cors к:
@app.route("/api/tasks/")
def index():
    tasks = [task.to_dict() for task in tasks_db.values()]
    return {"tasks": tasks}

настроить источники, с которых этим ресурсом можно пользоваться:
app.install(CorsPlugin(origins=['http://localhost:8000']))

Причём специфика сервера bottle такова, что нам понадобилось создать экземпляр объекта Bottle, чтобы это сделать:
app = bottle.Bottle()

Это привело также к тому, что мы используем его теперь не только для установки плагина, но и в декораторах пути:
@app.route("/api/tasks/")

и при запуске самого сервера:
bottle.run(app, host="localhost", port=5000)

#Подключение bootstrap#
$cd client
$npm install bootstrap@4.3.1

Корректируем файл src/main.js, добавив в заголовок одну строчку с импортом css:
import 'bootstrap/dist/css/bootstrap.css';

#Установка bootstrap-vue#
Comments: Нужно для рабоы с модальными окнами
$cd client
$npm install bootstrap-vue@2.0.0-rc.27

Подключить его в src/main.js: import BootstrapVue from 'bootstrap-vue';
и:
Vue.use(BootstrapVue);

#Создание дочерних компонентов#
Импортировать нужный компонент в блоке <script>:
import Confirmation from './Confirmation.vue';

В блок <script> => export default нужно добавить:
components: {
    confirmation: Confirmation,
  },
В нужное место блока <template> добавить:
<confirmation></confirmation>

Comments: Данные из родительского компонента получаются с помощью:
export default {
  props: ['message'],
};

Сообщение отправляет элемент родительского компонента: <confirmation message="Работает!"></confirmation>