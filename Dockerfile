# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.12.7
# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /entropy_site/backend
COPY /backend/requirements.txt /entropy_site/backend
RUN pip install -r requirements.txt

COPY ./backend/ /entropy_site/backend
ENV PYTHONPATH = /entropy_site

EXPOSE 5000
CMD python /entropy_site/backend/run.py