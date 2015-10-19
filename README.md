# Bagslash URL Redirect - For Education First

A programming challenge for Education First.
The app can be viewed at http://bagslash.com (This is an unused domain name of mine that I have repurposed for this project).
The project can be built either using a virtualenv or docker

## Virtualenv Build

### Prerequisits

 - Python 3
 - Pip
 - Virtualenv
 - Postgresql

### Getting Started

First, create and activate an env:
```
virtualenv env
source env/bin/activate
```

The project configuration relies on environment variables, it is therefore necessary to set the following variables within your env:

```
export DEBUG=False
export DB_NAME=postgres
export DB_USER=postgres
export DB_PASS=postgres
export DB_SERVICE=192.168.99.100
export DB_PORT=5432
export SECRET_KEY=insecure_key
export TWITTER_CONSUMER_KEY=bxoaJl4m7TsaBxBpo7oVywp2h
export TWITTER_CONSUMER_SECRET=uOJaZhdT7fE8VhMNq8ZPafdMP4nbnN2ydc6P9USUX0PPLeMsO1
```

Next, install Python requirements:
```
pip install -r requirements.txt
```

The project uses alembic to manage migrations. View the SQL of all migrations with:
```
alembic upgrade head --sql
```

Apply the migrations with:
```
alembic upgrade head
```

Nosetests is used for running tests:
```
nosetests --logging-level=INFO --logging-clear
```

Finally, run the app locally with:
```
python web/app.py
```

## Docker Build

### Prerequisits

 - Docker Compose
 - Docker Machine

### Getting Started

Create a virtual machine for development:

```
docker-machine create -d virtualbox bagslash-dev;
```

Point Docker at the dev machine:
```
eval "$(docker-machine env bagslash-dev)"
```

View currently running machines:
```
docker-machine ls
```
Build the app using Docker Compose:
```
docker-compose build
docker-compose up -d

```

View the SQL of all migrations with:
```
docker-compose run web alembic upgrade head --sql
```

Apply the migrations with:
```
docker-compose run web alembic upgrade head
```

## PSQL

The PSQL password can be found in the .env file, access the shell with:
```
psql -h 192.168.99.100 -p 5432 -U postgres --password
```

## Deployment
The app is deployed to DigitalOcean using Docker Compose. To create a new droplet:
```
docker-machine create \
-d digitalocean \
--digitalocean-access-token=ADD_YOUR_TOKEN_HERE \
bagslash-prod
```

To add the existing droplet to Docker Machine, your SSH key will need to be added to DigitalOcean, followed by the following command run:
```
docker-machine create -d generic \
--generic-ssh-user ubuntu \
--generic-ssh-key ~/.ssh/id_rsa.pub \
--generic-ip-address 159.203.70.17 \
bagslash-prod
```

## Known Bugs

 - Twitter callback breaks on production

## Further Work

Due to the slim time frame, the project had much of its scope cut. With more time, the following work remains:

 - Fix Twitter callback on prod
 - Load testing. This would be done using Locust.io and would be set up to hit all endpoints with varying frequency.
 - Auth with more than Twitter (ie Facebook, Google+ and Email)
 - Configure Postgres roles
 - Run tests and migrations as part of Docker build.
 - Higher test coverage, areas include Redirects admin view and authentication
 - Refactor and rearrange code.