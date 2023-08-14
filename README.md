# Myfasapiproject

This is a sample project created for demonstration purposes.

## Установка

1. Клонировать репозиторий.
2. Убедитесь, что у вас установлены Docker и Docker Compose. Вы можете установить Docker Desktop, который включает в себя Docker Compose, с официального сайта Docker.
3. Прописать 'docker-compose build', из директории, где находится файл docker-compose
4. Дождаться build'а проекта

## Запуск
1. После установки прописать docker-compose up -d
2. После старта открыть docker desktop
3. просмотреть контейнеры, контейнер с API называется api-1, с БД database-1, с тестами tests-1
4. Информация о прохождении тестов находится в логах tests-1 контейнера
5. Можно зайти в апи ui после запуска по адресу http://localhost:8000/docs
6. Менять эксель файл нужно в апи контейнере
## Запуск без докера
1. Установить необходимые пакеты из requirements.txt
2. Изменить данные в .env на ваши данные для вашей БД
3. Из директории testproject/ прописать uvicorn main_app.main:app --host 0.0.0.0 --port 8000
4. Из директории testproject/ прописать pytest
