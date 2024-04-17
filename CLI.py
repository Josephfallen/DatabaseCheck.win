from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import mysql.connector
import sqlite3
import psycopg2
import pyodbc
import cx_Oracle
import os
import sys

def check_mongodb_service_status():
    try:
        result = os.system("systemctl is-active mongod")
        if result == 0:
            print("MongoDB service is running.")
            return True
        else:
            print("MongoDB service is not running.")
            return False
    except Exception as e:
        print(f"Error checking MongoDB service status: {e}")
        return False

def check_database_status(host, port, dbname, username, password, db_type):
    if db_type == "mongodb" and not check_mongodb_service_status():
        return

    try:
        if db_type == "mongodb":
            uri = f"mongodb://{username}:{password}@{host}:{port}/{dbname}"
            client = MongoClient(uri)
            db = client[dbname]
            collection_names = db.list_collection_names()
            print(f"Database is online. Available collections: {collection_names}")
            client.close()
        elif db_type == "mssql":
            conn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={host};DATABASE={dbname};UID={username};PWD={password}")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sys.tables;")
            tables = cursor.fetchall()
            conn.close()
            print(f"MS SQL is online. Available tables: {tables}")
        elif db_type == "oracle":
            dsn = cx_Oracle.makedsn(host, port, dbname)
            connection = cx_Oracle.connect(username, password, dsn)
            cursor = connection.cursor()
            cursor.execute("SELECT 'Connected' FROM dual")
            result = cursor.fetchone()[0]
            connection.close()
            print(f"Oracle is online. Status: {result}")
        elif db_type == "mysql" or db_type == "mariadb":
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=dbname
            )
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            conn.close()
            print(f"{db_type.capitalize()} is online. Available tables: {tables}")
        elif db_type == "postgresql":
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=username,
                password=password
            )
            cursor = conn.cursor()
            cursor.execute("SELECT 'Connected';")
            result = cursor.fetchone()[0]
            conn.close()
            print(f"PostgreSQL is online. Status: {result}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Database Checker CLI")
    print("--------------------")

    db_type = input("Enter the database type (mongodb, mssql, oracle, mysql, mariadb, postgresql, sqlite): ").lower()

    host = input("Enter the host (default is localhost): ") or "localhost"
    port = input("Enter the port: ")
    dbname = input("Enter the database name: ")
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    check_database_status(host, port, dbname, username, password, db_type)

if __name__ == "__main__":
    main()
