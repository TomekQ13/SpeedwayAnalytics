FROM python:3.8

# install dependencies
RUN echo "deb http://security.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list                                                   
RUN mkdir -p /usr/share/man/man1 && \
    apt-get update -y && \
    apt-get install -y unzip openjdk-8-jre xvfb libxi6 libgconf-2-4

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable


RUN pip install pipenv
ENV PROJECT_DIR /scraper
ENV FLASK_APP run.py
ENV DATABASE postgres-database
COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
WORKDIR ${PROJECT_DIR}/
RUN pipenv install --system --deploy
COPY . .

RUN wget -N https://chromedriver.storage.googleapis.com/91.0.4472.19/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN mv -f ~/chromedriver /scraper/chromedriver
RUN rm /scraper/chromedriver.exe
RUN mv /scraper/chromedriver /scraper/chromedriver.exe
RUN chown root:root /scraper/chromedriver.exe
RUN chmod 0755 /scraper/chromedriver.exe


CMD ["python", "run.py"]