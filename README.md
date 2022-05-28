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

**Документация находится по адресу**  **http://127.0.0.1:8000/docs** 

### Запуск тестов

**Контейнер с приложением должен быть запущен!!**

```bash
docker exec -it gateway_web_1 pytest
docker exec -it gateway_web_1 pytest --cov=. # c измерением покрытия
```

### Инициализация бд

```
docker exec -it gateway_web_1 sh init_system.sh
```

