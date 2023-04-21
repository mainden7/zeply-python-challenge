# Zeply Python Challenge

## A simple web app to generate crypto wallets 

Tested on ubuntu 22.04

### Installation

#### Prerequisites

Project requires >=python3.10, postgres >= 12

#### Project install

```bash
$ git clone https://github.com/mainden7/zeply-python-challenge.git
$ cd zeply-python-challenge
$ poetry install
```

Rename and modify `alembic.example.ini` to `alembic.ini`

Go to `zeply_python_challenge` dir and copy `.env.example` to `.env` and modify its content, i.e. set postgres connection

```
POSTGRES_SERVER=0.0.0.0
POSTGRES_USER=test
POSTGRES_PASSWORD=test
POSTGRES_PORT=5432
POSTGRES_DB=zeply
```
### Run app

First apply migrations. Assumed that you've already have up and running postgres database and alembic.ini is properly configured

```bash
$ alembic upgrade head
```

To run app use install uvicorn as a development server

```bash
$ uvicorn zeply_python_challenge.main:app
```

[Swagger](localhost:8000/api/v1/docs) can be found here

### Run tests

```bash
$ pytest .
```

### TODO

This app is a simplified 4-5 hours of working project. In order to make it production ready need to improve some parts
1. Align with HTTP errors returned and define a spec for error codes and messages
2. Add better encryption
3. To allow better user experience there should be some kind of auth with master key password encryption of returned user data
4. Pagination with `next_url` would be a better choice
5. Add specific interfaces for each crypto, rather than checking allowance in constants and relay on third-party
6. To avoid security issues and leaks, define own lib to control and manipulate of crypto keys and others

P.S. 
Yeah I know postgres DB seems overkill here, but using async with sqlite3 or similar with single-threaded transaction engine isn't a better option. Also it may be better for `future` improvements, i.e. transactions, users, etc

