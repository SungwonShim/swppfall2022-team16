[![Build Status](https://app.travis-ci.com/swsnu/swppfall2022-team16.svg?branch=main)](https://travis-ci.com/swsnu/swppfall2022-team16)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=swsnu_swppfall2022-team16&metric=alert_status)](https://sonarcloud.io/dashboard?id=swsnu_swppfall2022-team16)

[![Coverage Status](https://coveralls.io/repos/github/swsnu/swppfall2022-team16/badge.svg?branch=main&kill_cache=1)](https://coveralls.io/github/swsnu/swppfall2022-team16?branch=main)
# swppfall2022-team16

## How to run the application

### Backend

```
$ cd backend
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

### Frontend

```
$ cd frontend
$ yarn install
$ yarn start
```

## How to test the application

### Backend

```
$ cd backend
$ coverage run --source='./bridgeUS' manage.py test
```

### Frontend

```
$ cd frontend
$ yarn test --coverage --watchAll=false
```