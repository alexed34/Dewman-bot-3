### Чат-бот для telegram и vkontakt с автответами.
Скрипт может самостоятельно отвечать на вопросы пользователей.

Для этого вопросы пользователей обрабатываются через сервис [dialogflow](https://dialogflow.cloud.google.com/).
Для корректной работы надо настроить в dialogflow список вопросов и ответов.

Скрипт работаетс с telegram и vkontakt. При работе в telegram на незнакомый вопрос скрипт отвечает 'Я не понимаю о чём речь', в vkontakt на незнакомый вопрос скрипт ничего не отвечает, дает возможность ответить техпотдержке.

### Пример работы
Протестировать работу скрипта здесь:

telegram - @DevmanAlexBot

vkontakt - https://vk.com/public189760742

![Пример работы](telegram.gif)


### Требования к окружению
Python 3

### Описание файлов
`telegram_bot.py` - для ответов в telegram

`vk_bot.py` - для ответов в vkontakt

`create_intents.py` - заполняет тренировочные фразы в dialogflow, фразы берутся из `questions.json` 

`questions.json` - список вопросов и ответов для заполнения в dialogflow

`loger.py` - файл настройки логгирования

`Procfile` - файл настройки для сервиса heroku.com, нужен если скрипт выкладывается на хостинге heroku.com

### Как установить
Создайте группу в telegram.

Создайте сообщество в vkontakte

Зарегестрируйтесь в dialogflow.

Получите файл с ключами json от dialogflow.

Запишите в файл .env данные 

TOKEN=токен чата в telegram, получить у BotFather 

GOOGLE_APPLICATION_CREDENTIALS= путь до файла с ключами в dialogflow

VK_TOKEN=ключь в вконтакте

CHAT_ID= чат телеграм канала

Python 3 должен быть уже установлен. Затем используйте pip(или pip3, если есть конфликт с Python2) для установки зависимостей:

`pip install -r requirements.txt`