FROM python:3.11.1-bullseye

RUN groupadd -r -g 999 dmoj && useradd -m -r -g dmoj -u 999 dmoj

RUN mkdir -p /assets \
    && chown -R dmoj:dmoj /assets \
    && mkdir -p /pdfcache \
    && chown -R dmoj:dmoj /pdfcache \
    && mkdir -p /datacache \
    && chown -R dmoj:dmoj /datacache \
    && mkdir -p /cache \
    && chown -R dmoj:dmoj /cache

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get update \
    && apt-get install -y \
        git gcc g++ make python3-dev python3-pip libxml2-dev \
        libxslt1-dev zlib1g-dev gettext curl redis-server mariadb-server \
        default-libmysqlclient-dev supervisor nginx nodejs \
        unzip xvfb libxi6 libgconf-2-4 google-chrome-stable nodejs \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g sass postcss-cli postcss autoprefixer
RUN pip install pymysql mysqlclient websocket-client uwsgi django-redis redis selenium tqdm

RUN wget https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver_linux64.zip

COPY --chown=dmoj:dmoj dmoj /site/
COPY --chown=dmoj:dmoj local_settings.py /site/dmoj/
COPY --chown=dmoj:dmoj .docker/base/generate_exam_users.py /site/judge/management/commands/

WORKDIR /site/

RUN pip install -r requirements.txt

RUN pip install python-jose # bug see https://github.com/python-social-auth/social-app-django/issues/427

USER dmoj
