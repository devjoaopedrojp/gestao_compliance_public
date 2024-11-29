FROM python:3.11-slim

WORKDIR /todos

COPY requirements.txt /todos/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /todos/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
