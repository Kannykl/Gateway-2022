#!/bin/sh


curl -X POST -H 'Content-Type: application/json' --data '{
   "user": {
    "email": "admin@mail.ru",
    "password": "adminpassword",
    "password2": "adminpassword",
    "is_admin": true
   }
}' "http://localhost:8000/db/create_user/"

