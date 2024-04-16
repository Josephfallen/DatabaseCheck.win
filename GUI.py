import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import mysql.connector
import sqlite3
import psycopg2
import ctypes
import os
import sys
from tkinter import filedialog
import pyodbc
import cx_Oracle


def run_with_admin():
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        # If not running as admin, relaunch the app with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def check_status():
    tab = notebook.select()
    tab_name = notebook.tab(notebook.select(), "text")
    status = ""

    if tab_name == "MongoDB":
        connection_string = mongodb_connection_entry.get()
        if not connection_string:
            status = "Error: Connection string cannot be empty."
        else:
            try:
                client = MongoClient(connection_string)
                db = client.get_default_database()
                collection_names = db.list_collection_names()
                client.close()
                status = f"MongoDB is online. Available collections: {collection_names}"
            except Exception as e:
                status = f"Error: {e}"

    elif tab_name == "MySQL":
        host = mysql_host_entry.get()
        port = mysql_port_entry.get()
        dbname = mysql_dbname_entry.get()
        username = mysql_username_entry.get()
        password = mysql_password_entry.get()
        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=dbname
            )
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            conn.close()
            status = f"MySQL is online. Available tables: {tables}"
        except Exception as e:
            status = f"Error: {e}"

    elif tab_name == "PostgreSQL":
        host = postgresql_host_entry.get()
        port = postgresql_port_entry.get()
        dbname = postgresql_dbname_entry.get()
        username = postgresql_username_entry.get()
        password = postgresql_password_entry.get()
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=username,
                password=password
            )
            cursor = conn.cursor()
            cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
            tables = cursor.fetchall()
            conn.close()
            status = f"PostgreSQL is online. Available tables: {tables}"
        except Exception as e:
            status = f"Error: {e}"

    elif tab_name == "MariaDB":
        host = mariadb_host_entry.get()
        port = mariadb_port_entry.get()
        dbname = mariadb_dbname_entry.get()
        username = mariadb_username_entry.get()
        password = mariadb_password_entry.get()
        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=dbname
            )
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            conn.close()
            status = f"MariaDB is online. Available tables: {tables}"
        except Exception as e:
            status = f"Error: {e}"

    elif tab_name == "SQLite":
        file_path = sqlite_file_entry.get()
        
        if not file_path:
            status = "Error: Please upload a .db file."
        else:
            try:
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                conn.close()
                status = f"SQLite is online. Available tables: {tables}"
                display_message(status, "success")
            except Exception as e:
                status = f"Error: {e}"
                display_message(status)
    elif tab_name == "MS SQL":
        server = mssql_server_entry.get()
        database = mssql_dbname_entry.get()
        username = mssql_username_entry.get()
        password = mssql_password_entry.get()
        
        if not server or not database:
            status = "Error: Server and Database name are required."
        else:
            try:
                conn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}")
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sys.tables;")
                tables = cursor.fetchall()
                conn.close()
                status = f"MS SQL is online. Available tables: {tables}"
            except Exception as e:
                status = f"Error: {e}"
    elif tab_name == "Oracle":
        host = oracle_host_entry.get()
        port = oracle_port_entry.get()
        sid = oracle_sid_entry.get()
        username = oracle_username_entry.get()
        password = oracle_password_entry.get()
        status = check_oracle_status(host, port, sid, username, password)

    status_label.config(text=status)

#Oracle Check
def check_oracle_status(host, port, sid, username, password):
    try:
        dsn = cx_Oracle.makedsn(host, port, sid)
        connection = cx_Oracle.connect(username, password, dsn)
        cursor = connection.cursor()
        
        # Check if the connection is successful
        cursor.execute("SELECT 'Connected' FROM dual")
        result = cursor.fetchone()[0]
        
        connection.close()
        
        return f"Oracle is online. Status: {result}"
        
    except Exception as e:
        return f"Error: {e}"
    
def toggle_dark_mode():
    if dark_mode_var.get() == 1:
        # Apply dark theme
        style.theme_use('clam')  
        root.config(bg='black')
        notebook.config(bg='dark grey')
        for widget in root.winfo_children():
            widget.config(bg='dark grey', fg='white')
    else:
        # Apply default theme
        style.theme_use('default')
        root.config(bg='')
        notebook.config(bg='')
        for widget in root.winfo_children():
            widget.config(bg='', fg='')

def check_mysql_status(host, port, dbname, username, password):
    # Implement MySQL connection and status check here
    pass

def upload_db_file():
    file_path = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db")])
    sqlite_file_entry.delete(0, tk.END)
    sqlite_file_entry.insert(0, file_path)

# Create main window
root = tk.Tk()
root.title("Database Checker")
root.geometry("500x450")

# Create style for dark mode
style = ttk.Style(root)
style.theme_use('default')

# Create notebook
notebook = ttk.Notebook(root)
notebook.pack(padx=20, pady=20, fill="both", expand=True)

# MongoDB tab
mongodb_frame = ttk.Frame(notebook)
notebook.add(mongodb_frame, text="MongoDB")

# Connection String
mongodb_connection_label = ttk.Label(mongodb_frame, text="Connection String:")
mongodb_connection_label.grid(row=0, column=0, padx=10, pady=5)
mongodb_connection_entry = ttk.Entry(mongodb_frame, width=50)  # Adjusted width here
mongodb_connection_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=2)

# MySQL tab
mysql_frame = ttk.Frame(notebook)
notebook.add(mysql_frame, text="MySQL")

mysql_host_label = ttk.Label(mysql_frame, text="Host:")
mysql_host_label.grid(row=0, column=0, padx=10, pady=5)
mysql_host_entry = ttk.Entry(mysql_frame)
mysql_host_entry.grid(row=0, column=1, padx=10, pady=5)

mysql_port_label = ttk.Label(mysql_frame, text="Port:")
mysql_port_label.grid(row=1, column=0, padx=10, pady=5)
mysql_port_entry = ttk.Entry(mysql_frame)
mysql_port_entry.grid(row=1, column=1, padx=10, pady=5)

mysql_dbname_label = ttk.Label(mysql_frame, text="Database Name:")
mysql_dbname_label.grid(row=2, column=0, padx=10, pady=5)
mysql_dbname_entry = ttk.Entry(mysql_frame)
mysql_dbname_entry.grid(row=2, column=1, padx=10, pady=5)

mysql_username_label = ttk.Label(mysql_frame, text="Username:")
mysql_username_label.grid(row=3, column=0, padx=10, pady=5)
mysql_username_entry = ttk.Entry(mysql_frame)
mysql_username_entry.grid(row=3, column=1, padx=10, pady=5)

mysql_password_label = ttk.Label(mysql_frame, text="Password:")
mysql_password_label.grid(row=4, column=0, padx=10, pady=5)
mysql_password_entry = ttk.Entry(mysql_frame, show="*")
mysql_password_entry.grid(row=4, column=1, padx=10, pady=5)

# SQLite tab
sqlite_frame = ttk.Frame(notebook)
notebook.add(sqlite_frame, text="SQLite")

sqlite_file_label = ttk.Label(sqlite_frame, text="Upload .db File:")
sqlite_file_label.grid(row=0, column=0, padx=10, pady=5)
sqlite_file_entry = ttk.Entry(sqlite_frame)
sqlite_file_entry.grid(row=0, column=1, padx=10, pady=5)

upload_button = ttk.Button(sqlite_frame, text="Upload", command=upload_db_file)
upload_button.grid(row=0, column=2, padx=10, pady=5)

# MS SQL tab
mssql_frame = ttk.Frame(notebook)
notebook.add(mssql_frame, text="MS SQL")

mssql_server_label = ttk.Label(mssql_frame, text="Server:")
mssql_server_label.grid(row=0, column=0, padx=10, pady=5)
mssql_server_entry = ttk.Entry(mssql_frame)
mssql_server_entry.grid(row=0, column=1, padx=10, pady=5)

mssql_dbname_label = ttk.Label(mssql_frame, text="Database Name:")
mssql_dbname_label.grid(row=1, column=0, padx=10, pady=5)
mssql_dbname_entry = ttk.Entry(mssql_frame)
mssql_dbname_entry.grid(row=1, column=1, padx=10, pady=5)

mssql_username_label = ttk.Label(mssql_frame, text="Username:")
mssql_username_label.grid(row=2, column=0, padx=10, pady=5)
mssql_username_entry = ttk.Entry(mssql_frame)
mssql_username_entry.grid(row=2, column=1, padx=10, pady=5)

mssql_password_label = ttk.Label(mssql_frame, text="Password:")
mssql_password_label.grid(row=3, column=0, padx=10, pady=5)
mssql_password_entry = ttk.Entry(mssql_frame, show="*")
mssql_password_entry.grid(row=3, column=1, padx=10, pady=5)

# Oracle tab
oracle_frame = ttk.Frame(notebook)
notebook.add(oracle_frame, text="Oracle")

oracle_host_label = ttk.Label(oracle_frame, text="Host:")
oracle_host_label.grid(row=0, column=0, padx=10, pady=5)
oracle_host_entry = ttk.Entry(oracle_frame)
oracle_host_entry.grid(row=0, column=1, padx=10, pady=5)

oracle_port_label = ttk.Label(oracle_frame, text="Port:")
oracle_port_label.grid(row=1, column=0, padx=10, pady=5)
oracle_port_entry = ttk.Entry(oracle_frame)
oracle_port_entry.grid(row=1, column=1, padx=10, pady=5)

oracle_sid_label = ttk.Label(oracle_frame, text="SID:")
oracle_sid_label.grid(row=2, column=0, padx=10, pady=5)
oracle_sid_entry = ttk.Entry(oracle_frame)
oracle_sid_entry.grid(row=2, column=1, padx=10, pady=5)

oracle_username_label = ttk.Label(oracle_frame, text="Username:")
oracle_username_label.grid(row=3, column=0, padx=10, pady=5)
oracle_username_entry = ttk.Entry(oracle_frame)
oracle_username_entry.grid(row=3, column=1, padx=10, pady=5)

oracle_password_label = ttk.Label(oracle_frame, text="Password:")
oracle_password_label.grid(row=4, column=0, padx=10, pady=5)
oracle_password_entry = ttk.Entry(oracle_frame, show="*")
oracle_password_entry.grid(row=4, column=1, padx=10, pady=5)

# PostgreSQL tab
postgresql_frame = ttk.Frame(notebook)
notebook.add(postgresql_frame, text="PostgreSQL")

postgresql_host_label = ttk.Label(postgresql_frame, text="Host:")
postgresql_host_label.grid(row=0, column=0, padx=10, pady=5)
postgresql_host_entry = ttk.Entry(postgresql_frame)
postgresql_host_entry.grid(row=0, column=1, padx=10, pady=5)

postgresql_port_label = ttk.Label(postgresql_frame, text="Port:")
postgresql_port_label.grid(row=1, column=0, padx=10, pady=5)
postgresql_port_entry = ttk.Entry(postgresql_frame)
postgresql_port_entry.grid(row=1, column=1, padx=10, pady=5)

postgresql_dbname_label = ttk.Label(postgresql_frame, text="Database Name:")
postgresql_dbname_label.grid(row=2, column=0, padx=10, pady=5)
postgresql_dbname_entry = ttk.Entry(postgresql_frame)
postgresql_dbname_entry.grid(row=2, column=1, padx=10, pady=5)

postgresql_username_label = ttk.Label(postgresql_frame, text="Username:")
postgresql_username_label.grid(row=3, column=0, padx=10, pady=5)
postgresql_username_entry = ttk.Entry(postgresql_frame)
postgresql_username_entry.grid(row=3, column=1, padx=10, pady=5)

postgresql_password_label = ttk.Label(postgresql_frame, text="Password:")
postgresql_password_label.grid(row=4, column=0, padx=10, pady=5)
postgresql_password_entry = ttk.Entry(postgresql_frame, show="*")
postgresql_password_entry.grid(row=4, column=1, padx=10, pady=5)

# MariaDB tab
mariadb_frame = ttk.Frame(notebook)
notebook.add(mariadb_frame, text="MariaDB")

mariadb_host_label = ttk.Label(mariadb_frame, text="Host:")
mariadb_host_label.grid(row=0, column=0, padx=10, pady=5)
mariadb_host_entry = ttk.Entry(mariadb_frame)
mariadb_host_entry.grid(row=0, column=1, padx=10, pady=5)

mariadb_port_label = ttk.Label(mariadb_frame, text="Port:")
mariadb_port_label.grid(row=1, column=0, padx=10, pady=5)
mariadb_port_entry = ttk.Entry(mariadb_frame)
mariadb_port_entry.grid(row=1, column=1, padx=10, pady=5)

mariadb_dbname_label = ttk.Label(mariadb_frame, text="Database Name:")
mariadb_dbname_label.grid(row=2, column=0, padx=10, pady=5)
mariadb_dbname_entry = ttk.Entry(mariadb_frame)
mariadb_dbname_entry.grid(row=2, column=1, padx=10, pady=5)

mariadb_username_label = ttk.Label(mariadb_frame, text="Username:")
mariadb_username_label.grid(row=3, column=0, padx=10, pady=5)
mariadb_username_entry = ttk.Entry(mariadb_frame)
mariadb_username_entry.grid(row=3, column=1, padx=10, pady=5)

mariadb_password_label = ttk.Label(mariadb_frame, text="Password:")
mariadb_password_label.grid(row=4, column=0, padx=10, pady=5)
mariadb_password_entry = ttk.Entry(mariadb_frame, show="*")
mariadb_password_entry.grid(row=4, column=1, padx=10, pady=5)



# Settings tab
settings_frame = ttk.Frame(notebook)
notebook.add(settings_frame, text="Settings")

# Button to run the app as admin
admin_button = ttk.Button(settings_frame, text="Run as Admin", command=run_with_admin)
admin_button.pack(pady=10)

# Status label
check_button = ttk.Button(root, text="Check Status", command=check_status)
check_button.pack(pady=10)


status_label = ttk.Label( text="", anchor="center")
status_label.pack(padx=20, pady=20, fill="both")


root.mainloop()
