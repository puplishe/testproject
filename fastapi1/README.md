# Myfasapiproject

This is a sample project created for demonstration purposes.

## Установка

1. Клонировать репозиторий.
2. Прописать  `pip install -r requirements.txt`.
3. Настроить postgres(создать юзера и пустую бд)
4. в файле .env в SQL_ALCHEMY_DATABASE_URL вставить свою бд(по принципу:   postgresql://юзер_бд:пароль@localhost/имя_бд)

## Запуск
working directory должен быть по пути fastapi
Прописать следующую команду(либо можно ранить main.py): uvicorn main:app --reload 
