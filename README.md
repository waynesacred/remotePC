# remotePC
Cкрипт, созданный на основе библиотек telebot - библиотека для управления через бота телеграмм; OS - библиотека для управления операционной системой и др.
#Функции:
_📷Быстрый скриншот_ - отправляет скриншот экрана
_🖼Полный скриншот_ - отправляет скриншот экрана без сжатия
_❇️Дополнительно_ - переходит в меню с доп. функциями
_📩Отправка уведомления_ - пришлет на ПК окно с сообщением(msgbox)
_⏪Назад⏪_ - возвращает в главное меню
_✅Выполнить команду_ - выполняет в cmd любую указанную команду
_⛔️Выключить компьютер_ - моментально выключает компьютер
_♻️Перезагрузить компьютер_ - моментально перезагружает компьютер
_❌Закрыть процесс_ - завершает любой процесс
_✔️Запустить_ - запуск приложений(в том числе и exe)
#Установка и запуск:
1. В боте @BotFather создать нового бота;
2. Запустить консоль "win+r > cmd"
3. Прописать команду - pip install -r путь до файла install.txt
4. После получения токена бота "121313131:qwerty" вставить в коде в строку "bot_token=";
5. В строку "my_ID = " вставить Ваш ID Telegram;
6. Сохранить файл
7. Открыть консоль, прописать команду- cd путь до директории где лежит файл RemotePC.py. Пример: (cd C:\download)
8. Прописать в консоли в консоли pyinstaller -w -F RemotePC.py
9. После компиляции exe файла в папке dist, добавить в автозапуск : win+r > sell:startup.
