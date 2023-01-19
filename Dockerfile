FROM python:3
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

