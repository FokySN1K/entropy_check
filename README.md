# Entropy_check


## Предварительная подготовка

1. Склонируйте репозиторий:
```git
  git clone https://github.com/FokySN1K/entropy_check.git
```
2. Создайте файл .env в директории, где расположен файл env_example entropy_check/backend
/app/env_example с заданными параметрами из него же:
```git
  UPLOAD_FOLDER=./app/static/USERS_FILE/
  SECRET_KEY=example_key
```  
  
## Загрузка
Чтобы поднять сайт на своём компьютер
```docker
  docker-compose up
```  

## Проблемы
  Если у вас занят порт, то измените его
```docker
      ports:
      - "5000:5000"
```  
на: 
```docker
      ports:
      - "your_port:5000"
```  
