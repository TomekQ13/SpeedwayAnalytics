FROM python:3.8
RUN pip install pipenv

ENV PROJECT_DIR /interface_api
ENV FLASK_APP run.py
ENV DATABASE_URI postgres://postgres:5432
COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
WORKDIR ${PROJECT_DIR}/
RUN pipenv install --system --deploy
COPY . .

CMD gunicorn -w 3 run:app