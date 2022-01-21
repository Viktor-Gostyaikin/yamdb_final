# yamdb_final
![example workflow](https://github.com/Viktor-Gostyaikin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
### Описание проетка

#### Docker-compose сервис включающий в себя
- приложение YaMDb, которое собирает отзывы пользователей на различные произведения
- сервер nginx
- база данных PostgreSQL
#### В проекте реализованы
- автоматический запуск тестов,
- обновление образов на Docker Hub,
- автоматический деплой на боевой сервер при пуше в главную ветку main.

### Stack
- python 3.7-slim
- Django 2.2
- gunicorn 20.0.4
- nginx 1.18.0
- docker-compose 3.0

### Как запустить проект:

Настроить .env. В этом файле уже предустановлены значения.

```  
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Клонировать репозиторий и перейти в локальную директорию /infra в командной строке:

```
$ git clone https://github.com/Viktor-Gostyaikin/infra_sp2.git
```

```
$ cd ~/infra_sp2/infra
```

Запустить docker-compose:

```
$ sudo docker-compose up -d --build
```

Выполнить миграции, создать суперпользователя, собрать статику.

```
$ sudo docker-compose exec web python manage.py migrate
$ sudo docker-compose exec web python manage.py createsuperuser
$ sudo docker-compose exec web python manage.py collectstatic --no-input 
```

Проект доступен по url http://localhost/

### Алгоритм регистрации пользователей

Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
YaMDB отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес `email`.
Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).
При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

### Пользовательские роли

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (`user`) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (`moderator`) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django должен всегда обладать правами администратора, пользователя с правами `admin`. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.


### Самостоятельная регистрация новых пользователей

Пользователь отправляет POST-запрос с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
Сервис YaMDB отправляет письмо с кодом подтверждения (`confirmation_code`) на указанный адрес `email`.
Пользователь отправляет POST-запрос с параметрами username и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).
В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле (описание полей — в документации).

### Создание пользователя администратором

Пользователя может создать администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт `api/v1/users/` (описание полей запроса для этого случая — в документации). В этот момент письмо с кодом подтверждения пользователю отправлять не нужно.
После этого пользователь должен самостоятельно отправить свой `email` и username на эндпоинт `/api/v1/auth/signup/` , в ответ ему должно прийти письмо с кодом подтверждения.
Далее пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен), как и при самостоятельной регистрации.

### Ресурсы API YaMDb

- Ресурс `auth`: аутентификация.
- Ресурс `users`: пользователи.
- Ресурс `titles`: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс `categories`: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс `genres`: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс `reviews`: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс `comments`: комментарии к отзывам. Комментарий привязан к определённому отзыву.
Каждый ресурс описан в документации Redoc: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.

### Authentication
#### jwt-token
Используется аутентификация с использованием JWT-токенов

| Security Scheme Type   | API Key |
|------------------------|--------:|
| Header parameter name  |Bearer   |
### Проект доступен по адрессу
http://www.gostyaikin.ga
### Автор
Виктор Гостяйкин
https://github.com/Viktor-Gostyaikin/
