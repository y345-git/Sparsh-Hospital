import pymysql
from flask import current_app, g
import socket

def get_db():
    if 'db' not in g:
        try:
            connection_params = {
                'host': current_app.config['MYSQL_HOST'],
                'port': int(current_app.config['MYSQL_PORT']),
                'user': current_app.config['MYSQL_USER'],
                'password': current_app.config['MYSQL_PASSWORD'],
                'database': current_app.config['MYSQL_DB'],
                'connect_timeout': 10,
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor,
                'unix_socket': None,
                'ssl': None,
                'read_timeout': 10,
                'write_timeout': 10,
                'use_unicode': True,
                'client_flag': 0
            }
            g.db = pymysql.connect(**connection_params)
        except Exception as e:
            print(f"Error connecting to MySQL Database: {e}")
            raise e
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close() 