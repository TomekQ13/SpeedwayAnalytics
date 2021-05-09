FROM python:3.8

# install dependencies
RUN echo "deb http://security.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list                                                   
RUN mkdir -p /usr/share/man/man1 && \
    apt-get update -y && \
    apt-get install -y unzip openjdk-8-jre xvfb libxi6 libgconf-2-4

RUN pip install pipenv
ENV PROJECT_DIR /scraper
ENV FLASK_APP run.py
ENV DATABASE postgres-database
COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
WORKDIR ${PROJECT_DIR}/
RUN pipenv install --system --deploy
COPY . .


CMD ["python", "run.py"]