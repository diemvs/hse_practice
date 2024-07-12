# HSE practice

## Установка библиотек

```sh
pip install -r requirements.txt
```

Создание конфигурационного файла (pyway.conf) для pyway.

```sh
database_type: postgres 
database_username: postgres
database_password: 123456
database_host: localhost
database_port: 5432
database_name: hse_practice
database_migration_dir: resources/migrations
database_table: public.pyway
```

Создание переменных окружения (.env).
```sh
DATABASE_NAME=hse_practice
DATABASE_PASSWORD=12345678
DATABASE_USER=postgres
DATABASE_MIGRATION_DIR=resources/migrations
DATABASE_HOST=localhost
DATABASE_TYPE=postgres
```

## Запуск
```sh
./start.sh
```
