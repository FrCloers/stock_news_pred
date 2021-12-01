import os
from flask import Flask, render_template, request, Response
import sqlalchemy
from dotenv import load_dotenv
import pandas as pd

#load environment variable
load_dotenv()

def container_connect_bd():
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]

    # Extract port from db_host if present,
    # otherwise use DB_PORT environment variable.
    host_args = db_host.split(":")
    if len(host_args) == 1:
        db_hostname = db_host
        db_port = os.environ["DB_PORT"]
    elif len(host_args) == 2:
        db_hostname, db_port = host_args[0], int(host_args[1])

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            database=db_name,  # e.g. "my-database-name"
        )
    )
    return pool

if __name__ == "__main__":
    pool = container_connect_bd()
    connection = pool.connect()

    sql = "SELECT ticker, `date`, stock_price FROM stocksprice WHERE ticker = %s"
    values = ('AMZN', )

    tpm=pd.DataFrame(connection.execute(sql, values).fetchall(), columns=['ticker', 'date', 'stock_price'])

    print(tpm.head(5))