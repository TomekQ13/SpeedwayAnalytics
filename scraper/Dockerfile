FROM python:3.8
RUN pip install pipenv

ENV PROJECT_DIR /interface_api
ENV FLASK_APP run.py
ENV DATABASE postgres-database
COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
WORKDIR ${PROJECT_DIR}/
RUN pipenv install --system --deploy
COPY . .

RUN chmod a+x chromedriver

CMD ["python", "run.py"]