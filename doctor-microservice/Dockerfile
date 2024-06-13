FROM python:3.12-slim
WORKDIR /app
RUN pip install pipenv
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy
COPY . /app

CMD gunicorn -b 0.0.0.0:5002 run:app