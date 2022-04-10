# Gateway

### Этот репозиторий содержит код шлюза для приложения stat-inc

#### Шлюз реализует следующий функционал:

- авторизация и регистрация пользователей;
- прокси к базе данных.

------

#### Стек технологий:

- python 3.10
- FastAPI 0.75.1
- docker
- docker-compose



### Запуск проекта

```
git clone https://gitlab.com/stat-inc/gateway.git
cd gateway
docker-compose up -d --build
```

**Документация находится по адресу**  **http://127.0.0.1:8002/docs** 
