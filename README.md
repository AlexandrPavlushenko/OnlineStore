# Домашняя работа

<i>Это Django-проект онлайн-магазина SkyStore</i>

## Описание проекта

## Установка:

1. Клонируйте репозиторий:

```
https://github.com/AlexandrPavlushenko/OnlineStore.git
```

2. Установите зависимости:

```
pip install -r requirements.txt
```

3. Создайте и заполните данными файл <b>.env</b> по шаблону <b>.env.sample</b>, который находится в корне проекта

4. Выполните миграции в БД
```
python manage.py migrate
```

5.Заполните данными  БД из файлов-фикстур, командами:

```
   python manage.py loaddata category_fixture.json --format json
   python manage.py loaddata product_fixture.json --format json
```
## Использование:
a) Запустите redis-server<br>
б) В терминале введите команду запуска сервера: <b><i>python manage.py runserver</i></b>