import datetime


def log(database, header, data):
    database.sql(
        sql="insert into logs (header, data, datetime) VALUES (%s, %s, %s)",
        args=(header, data, str(datetime.datetime.now()))
    )
