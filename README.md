# Логистический сервис API

## Тестовое задание от компании WelbeX:

- Реализовать API на одном из фрэймворков на выбор (<u>Django REST Framework</u> / FastAPI)
- База данных стандартная - PostgreSQL
- Сервисы должны запускаться через docker-compose

### Детали:

- Модель груза (Cargo) должна содержать следующие поля:
    - локация pick-up;
    - локация delivery;
    - вес (1-1000);
    - описание;

- Модель транспорта (Transport) должна содержать следующие поля:
  - уникальный номер (номер от 1000 до 9999, затем любая заглавная буква английского алфавита: 1234А, 5678В и т.п);
  - текущая локация;
  - грузоподъемность (1-1000);

- Модель локации (Location) должна содержать следующие поля:
  - город;
  - штат;
  - почтовый индекс (zip);
  - широта;
  - долгота;

### Функционал:

- Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду);
- Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза (=< 450 миль));
- Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза);
- Редактирование машины по ID (локация (определяется по введенному zip-коду));
- Редактирование груза по ID (вес, описание);
- Удаление груза по ID.
- Фильтр списка грузов (вес, мили ближайших машин до грузов);
- Автоматическое обновление локаций всех машин раз в 3 минуты (локация меняется на другую случайную);


## Запуск сервиса:

Скопируйте на сервер проект
```shell
git clone https://github.com/Lookin44/logistics-service.git
```

перейдите внутрь проекта
```shell
cd logistics-service
```

создайте внутри файл .env с содержимым
```dotenv
# Переменные для базы данных
PSQL_HOST=db
PSQL_ENGINE=django.db.backends.postgresql_psycopg2
PSQL_DATABASE=downtime_db
PSQL_USER=bot_vizer
PSQL_PASSWORD=bd8e7f93-ed502084
PSQL_PORT=5432

# Пременные для Django
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# Переменные для Celery elery
CELERY_BROKER_URL=redis://redis:6379
```

Запустите проект через docker-compose
```shell
docker-compose up -d
```

### Доступные эндпоинты API-сервиса:

```
api/v1/cargos/ (POST)
api/v1/cargos/ (GET)
api/v1/cargos/?weight__lte={значение для фильтрации по весу} (GET)
api/v1/cargos/?distance={значение для фильтрации по расстоянию транспорта до грузов в милях} (GET)
api/v1/cargos/{id}/ (GET)
api/v1/cargos/{id}/ (PATCH)
api/v1/cargos/{id}/ (DELETE)

api/v1/transport/{id}/ {PATCH}
```

### Работа с API:

В корне каталога содержится набор запросов для Postman: WelbeX.postman_collection.json

POST запрос для создания груза на адрес http://127.0.0.1:8000/api/v1/cargos/:

ВНИМАНИЕ: параметры location_up и location_delivery принимают почтовый индекс (zip)

```json
{
    "location_up": "1743",
    "location_delivery": "20322",
    "description": "Гвозди",
    "weight": 500
}
```

PATCH - запрос на изменение груза на адрес http://127.0.0.1:8000/api/v1/cargos/{id-груза}/:

```json
{
    "location_up": "20322",
    "location_delivery": "1743",
    "description": "Гвозди",
    "weight": 100
}
```

PATCH - запрос на изменение транспорта на адрес http://127.0.0.1:8000/api/v1/transport/{id-транспорта}/

ВНИМАНИЕ: параметр current_location принимает почтовый индекс (zip)
```json
{
    "pk": 1,
    "current_location": "1542",
    "number": "2442Z",
    "tonnage": 522
}
```
