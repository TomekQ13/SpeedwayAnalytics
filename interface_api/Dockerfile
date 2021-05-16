FROM python:3.8
RUN pip install pipenv

ENV PROJECT_DIR /interface_api
ENV FLASK_APP run.py
ENV DATABASE_USER postgres
ENV DATABASE_PASSWORD ilikepostgresalot!@#$
ENV DATABASE_HOST postgres
ENV DATABASE_PORT 5432
ENV DATABASE_DATABASE postgres

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
WORKDIR ${PROJECT_DIR}/
RUN pipenv install --system --deploy
COPY . .

CMD flask run --host=0.0.0.0