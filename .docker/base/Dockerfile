FROM python:3.11.1-bullseye

RUN groupadd -r -g 999 dmoj && useradd -m -r -g dmoj -u 999 dmoj

RUN mkdir -p /assets && \
    chown -R dmoj:dmoj /assets && \
    mkdir -p /pdfcache && \
    chown -R dmoj:dmoj /pdfcache && \
    mkdir -p /datacache && \
    chown -R dmoj:dmoj /datacache && \
    mkdir -p /cache && \
    chown -R dmoj:dmoj /cache

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get update && \
    apt-get install -y \
        git gcc g++ make python3-dev python3-pip libxml2-dev \
        libxslt1-dev zlib1g-dev gettext curl redis-server mariadb-server \
        default-libmysqlclient-dev supervisor nginx nodejs \
        unzip xvfb libxi6 libgconf-2-4 google-chrome-stable nodejs && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN npm install -g sass postcss-cli postcss autoprefixer
RUN pip install pymysql mysqlclient websocket-client uwsgi django-redis redis selenium tqdm

RUN wget https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver_linux64.zip

COPY --chown=dmoj:dmoj dmoj /site/
COPY --chown=dmoj:dmoj local_settings.py /site/dmoj/
COPY --chown=dmoj:dmoj .docker/base/generate_exam_users.py /site/judge/management/commands/

# serve ace, mathjax, jquery, select2, lato.css, profile images locally
COPY --chown=dmoj:dmoj .docker/base/ace /site/resources/ace/
COPY --chown=dmoj:dmoj .docker/base/mathjax /site/resources/mathjax/
COPY --chown=dmoj:dmoj .docker/base/jquery.min.js /site/resources/
COPY --chown=dmoj:dmoj .docker/base/select2.min.js /site/resources/
COPY --chown=dmoj:dmoj .docker/base/select2.min.css /site/resources/
COPY --chown=dmoj:dmoj .docker/base/lato.css /site/resources/
COPY --chown=dmoj:dmoj .docker/base/profile.png /site/resources/
COPY --chown=dmoj:dmoj .docker/base/mathjax_config.js /site/resources/

# hostless websocket
RUN sed -i "s+this.websocket = new WebSocket(websocket);+this.websocket = new WebSocket(websocket.replace(new RegExp('(wss|ws):///event/'),\`\$1://\${location.host}/event/\`));+" /site/resources/event.js

# serve mathjax locally
RUN sed -i "s+https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-chtml.min.js+/mathjax/tex-chtml.js+" /site/judge/widgets/pagedown.py
RUN sed -i "s+'https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-chtml.min.js'+window.location.protocol \+ '//' \+ window.location.host \+ '/static/mathjax/tex-chtml.js'+" /site/resources/dmmd-preview.js
RUN sed -i "s+'https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-chtml.min.js'+window.location.protocol \+ '//' \+ window.location.host \+ '/static/mathjax/tex-chtml.js'+" /site/resources/martor-mathjax.js
RUN sed -i "s+https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-chtml.min.js+{{ static('mathjax/tex-chtml.js') }}+" /site/templates/mathjax-load.html
RUN sed -i "s+https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-chtml.min.js+mathjax/tex-chtml.js+" /site/templates/problem/raw.html
RUN sed -i "s+maker.make()+shutil.copytree(os.path.join(settings.DMOJ_RESOURCES, 'mathjax'), os.path.join(maker.dir, 'mathjax')); maker.make()+" /site/judge/views/problem.py
RUN sed -i "s+maker.make(debug=True)+shutil.copytree(os.path.join(settings.DMOJ_RESOURCES, 'mathjax'), os.path.join(maker.dir, 'mathjax')); maker.make(debug=True)+" /site/judge/management/commands/render_pdf.py

# remove gravatar
RUN sed -i "s+return gravatar_url+return '/static/profile.png'+" /site/judge/jinja2/gravatar.py

# remove websocket reconnect banner
RUN sed -i "s+\$('.ws-closed').show()+if(false) \$('.ws-closed').show()+" /site/templates/submission/list.html

WORKDIR /site/

RUN pip install -r requirements.txt

# serve lato.css locally
RUN sed -i "s+https://fonts.googleapis.com/css?family=Lato:400,700,400italic,700italic&subset=latin+/static/lato.css+" /usr/local/lib/python3.11/site-packages/martor/static/plugins/css/semantic.css

USER dmoj
