FROM python:3.8
RUN pip install pipenv

ENV PROJECT_DIR /interface_api

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
WORKDIR ${PROJECT_DIR}/
RUN pipenv install --system --deploy
COPY . .

CMD flask run --host=0.0.0.0