# import cx_Oracle
# import os
# from dotenv import load_dotenv

# load_dotenv()
# username = os.getenv('Oracle_Username')
# password = os.getenv('Oracle_PW')
# host = os.getenv("Oracle_Host")
# port = os.getenv("Oracle_Port")
# service_name = os.getenv("Oracle_SN")

# # create a database connection
# def get_connection():
#     dsn = cx_Oracle.makedsn('host', 'port', service_name='service_name')
#     conn = cx_Oracle.connect('username', 'password', dsn)
#     return conn

# #close connection 
# def close_db_connection(connection):
#     connection.close()


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

