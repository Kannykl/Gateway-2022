#!/bin/sh

curl -X POST -H 'Content-Type: application/json' --data '{
  "user": {
    "email": "user1@mail.ru",
    "password": "user1password",
    "password2": "user1password"
  }
}' "http://localhost:8000/db/create_user/"

curl -X POST -H 'Content-Type: application/json' --data '{
  "user": {
    "email": "user2@mail.ru",
    "password": "user2password",
    "password2": "user2password"
  }
}' "http://localhost:8000/db/create_user/"

curl -X POST -H 'Content-Type: application/json' --data '{
  "user": {
    "email": "user3@mail.ru",
    "password": "user3password",
    "password2": "user3password"
  }
}' "http://localhost:8000/db/create_user/"


curl -X POST -H 'Content-Type: application/json' --data '{
  "bot": {
    "username": "9616924291",
    "password": "verylongpassword"
  }
}' "http://localhost:8000/db/create_bot/"

curl -X POST -H 'Content-Type: application/json' --data '{
  "bot": {
    "username": "9190887716",
    "password": "verylongpassword"
  }
}' "http://localhost:8000/db/create_bot/"

curl -X POST -H 'Content-Type: application/json' --data '{
   "user": {
    "email": "admin@mail.ru",
    "password": "adminpassword",
    "password2": "adminpassword",
    "is_admin": true
   }
}' "http://localhost:8000/db/create_user/"
