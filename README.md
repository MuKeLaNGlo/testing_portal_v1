# testing_portal_v1
Учебный портал для тестирования студентов

## Установка
```sh
git clone https://github.com/MuKeLaNGlo/testing_portal_v1.git
```
Затем нужно установить зависимости в виртуальное окружение, выполнив следующие команды в каталоге проекта:
```sh
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
cd django-app
```
Обязательно примените миграции
```sh
python manage.py migrate
```
По желанию примените фикстуры
```sh
python manage.py loaddata data_fixture.json
```


Есть фикстуры, чтобы их можно применить нужно переместить файл ```db.json``` в папку ```blogicum``` и выполнить команду:
```sh
python manage.py loaddata dj.json
```
## Запуск проекта
Чтобы запустить проект, вы можете использовать следующую команду в каталоге проекта:
```sh
python manage.py runserver
```
Это запустит сервер разработки на порту 8000. После этого вы сможете получить доступ к проекту по адресу http://localhost:8000/.
