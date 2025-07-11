FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "yatube_project.wsgi:application", "--bind", "0.0.0.0:8000"]
