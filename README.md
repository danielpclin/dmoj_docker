DMOJ Docker
=====

This repository contains the Docker files to run a clone of the [DMOJ site](https://github.com/DMOJ/online-judge). It configures some additional services, such as mathoid and texoid.

## Installation

First, [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) must be installed. Installation instructions can be found on their respective websites.

Clone the repository:
```sh
cd ~
git clone https://git.epl.tw/DanielLin/dmoj_docker.git dmoj_docker
cd dmoj_docker
git submodule update --init --recursive
cp .env.example .env
```

Configure the environment variables in the files in `.env`. In particular, set the `MYSQL_PASSWORD` and `MYSQL_ROOT_PASSWORD`, `DOMAIN` and `SECRET_KEY`. Also, configure the `server_name` directive in `.docker/nginx/nginx.conf`.
Remember to configure `local_settings.py` (email). 

Initialize the setup by moving the configuration files into the submodule and by creating the necessary directories:
```sh
mkdir -m777 problems media
```

Create dmoj_judge network
```shell
sudo docker network create dmoj_judge
```

Next, build the images:
```sh
sudo docker compose build
```

Start up the site, so you can perform the initial migrations and generate the static files:
```sh
sudo docker compose up -d uwsgi
```

Wait a few seconds to let the database initialize.
You will need to generate the schema for the database, since it is currently empty:
```sh
sudo docker compose exec uwsgi python3 manage.py migrate
```

You will also need to generate the static files:
```sh
sudo docker compose exec uwsgi bash
./make_style.sh
cp -r resources/ /assets/
cp 502.html /assets/
cp logo.png /assets/
cp robots.txt /assets/
python3 manage.py collectstatic --noinput
python3 manage.py compilemessages
python3 manage.py compilejsi18n
exit
```

Finally, the DMOJ comes with fixtures so that the initial install is not blank. They can be loaded with the following commands:
```sh
sudo docker compose exec uwsgi python3 manage.py loaddata navbar
sudo docker compose exec uwsgi python3 manage.py loaddata language_all # language_small
#sudo docker compose exec uwsgi python3 manage.py loaddata demo
```

Start all containers with
```sh
sudo docker compose up -d
```


## Usage
```sh
sudo docker compose up -d
```

## Notes

### Add judges
Add judge and generate token in admin site
Build judge docker images
```shell
sudo apt-get install -y make
cd ~
git clone --recursive https://github.com/DMOJ/judge.git
cd judge/.docker
sudo make judge-tier3
```

Run judge container, if you need to access the judge though api, you need to bind port 9998.
```shell
# e.g. -p "$(ip addr show dev eth0 | perl -ne 'm@inet (.*)/.*@ and print$1 and exit')":9998:9998
sudo docker run \
    --name $JUDGE_NAME \
    -v ~/dmoj_docker/problems:/problems \
    --cap-add=SYS_PTRACE \
    -d \
    --restart=always \
    dmoj/judge-tier3:latest \
    run -p "9999" \
    "dmoj_bridged" "$JUDGE_NAME" "$JUDGE_AUTHENTICATION_KEY"
```

See if judge is running correctly
```shell
sudo docker ps -a
sudo docker logs judge1
```

### Add super user
```shell
sudo docker compose exec uwsgi python3 manage.py adduser --staff --superuser account email password
sudo docker compose exec uwsgi python3 manage.py createsuperuser # if you use this command, you need to restart uwsgi to generate user profile
```

### Add user
```shell
sudo docker compose exec uwsgi python3 manage.py adduser account email password
```


### Migrating
As the DMOJ site is a Django app, you may need to migrate whenever you update. Assuming the site container is running, running the following command should suffice:
```sh
sudo docker compose exec uwsgi python3 manage.py migrate
```

### Managing Static Files
If your static files ever change, you will need to rebuild them:
```sh
sudo docker compose exec uwsgi bash
./make_style.sh
python3 manage.py collectstatic --noinput
python3 manage.py compilemessages
python3 manage.py compilejsi18n
cp -r resources/ /assets/
cp 502.html /assets/
cp logo.png /assets/
cp robots.txt /assets/
exit
```

### Updating submodules
```sh
git submodule update --remote dmoj
git add dmoj
git commit -m "update submodule"
```

### Updating The Site
Updating various sections of the site requires different images to be rebuilt.

If any prerequisites were modified, you will need to rebuild most of the images:
```sh
git reset --hard origin/master
git submodule foreach --recursive git reset --hard
git submodule update --init --recursive
sudo docker compose build
sudo docker compose up -d
```
If the static files are modified, read the section on [Managing Static Files](#managing-static-files).

If only the source code is modified, a restart is sufficient:
```sh
sudo docker compose restart site celery bridged wsevent
```

### Updating the repository
```sh
git reset --hard origin/master
git submodule foreach --recursive git reset --hard
git submodule update --remote
git add .
git commit -m "git submodule updated"
git push origin
```



### Multiple Nginx Instances

The `docker-compose.yml` configures Nginx to publish to port 80. If you have another Nginx instance on your host machine, you may want to change the port and proxy pass instead.

For example, a possible Nginx configuration file on your host machine would be:
```
server {
    listen 80;
    listen [::]:80;

    add_header X-UA-Compatible "IE=Edge,chrome=1";
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    location / {
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Host $http_host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_pass http://127.0.0.1:8080/;
    }
}
```
In this case, the port that the Nginx instance in the Docker container is published to would need to be modified to `10080`.

## Common Errors
### 502 Bad Gateway
Ensure that you also restart the Nginx container if you restart the site container as Nginx caches DNS queries. Otherwise, Nginx will try to hit the old IP, causing a 502 Bad Gateway. See [this issue](https://github.com/docker/compose/issues/3314) for more information.
### 413 – Request Entity Too Large
Add a line in the http section of nginx.conf (/etc/nginx/nginx.conf) `client_max_body_size 100M;` and reload nginx
