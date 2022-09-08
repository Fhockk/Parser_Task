## About
- This application was created as a result of a test task
- The purpose of the application is to collect all ads from the site

## Technical Requirements
- Sending requests to the website: requests python library
- As ORM: SQLAlchemy
- Database for storing, parse data: PostgreSQL

## First:
```shell
pip install -r requirements.txt
```

## To connect to db you need to configure db_settings.py:
>- pguser - username postgress
>- pgpasswd - password to pg account
>- pghost - server host (localhost)
>- pgport - port (postgresql: 5432)
>- pgdb - name of db

## Database Restore:
```shell
psql -d dataox -f dataox.sql
```

## Run main.py

## Google Spreadsheet: [Link](https://docs.google.com/spreadsheets/d/1NhzdRDzb0g7ojlAzMefNzXojgAuyPrtXdZ2EWWqSti8/edit#gid=0)





