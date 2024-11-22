# Entropy_check

## Что за программа
При запуске поднимается сайт, с помошью которого можно рассчитать энтропию файла ***обраватывается только txt  формат, но засунуть dump.txt никто не мешает***



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
Чтобы поднять сайт на своём компьютере
```docker
  docker-compose up
```
Затем перейдите на выведенный в командной строке адрес 

## Проблемы
  Если у вас занят порт, то измените порт в файле docker-compose.yml
```docker
      ports:
      - "5000:5000"
```  
на: 
```docker
      ports:
      - "your_port:5000"
```  
