import os
import hashlib
import logging
import sqlite3



def get_database_connection():
   '''
       Creates a connection between selected database
   '''
   sqlite_file = 'user.db'
   file_exists = os.path.isfile(sqlite_file)
   conn = sqlite3.connect(sqlite_file)
   if not file_exists:
       create_sqlite_tables(conn)
   if os.stat(sqlite_file).st_size == 0:
       create_sqlite_tables(conn)
   return conn


def create_sqlite_tables(conn):
   '''
       Creates a sqlite table as specified in schema_sqlite.sql file
   '''
   cursor = conn.cursor()
   with open('schema_sqlite.sql', 'r') as schema_file:
       cursor.executescript(schema_file.read())
   conn.commit()


def get_user_count():
   '''
       Checks whether a user exists with the specified username and password
   '''
   conn = get_database_connection()
   try:
       cursor = conn.cursor()
       cursor.execute('SELECT COUNT(*) FROM users')
       result = cursor.fetchone()
       if result:
           return result[0]
   except:
       return False


def check_user_exists(username, password):
   '''
       Checks whether a user exists with the specified username and password
   '''
   conn = get_database_connection()
   try:
       cursor = conn.cursor()
       cursor.execute(
           'SELECT * FROM users WHERE username=? AND password=?', (username, password))
       result = cursor.fetchone()
       if result:
           return result[0]
   except:
       return False


def store_last_login(user_id):
   '''
       Checks whether a user exists with the specified username and password
   '''
   conn = get_database_connection()
   try:
       cursor = conn.cursor()
       cursor.execute(
           "UPDATE users SET last_login=(strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) WHERE id=?", (user_id, ))
       conn.commit()
       cursor.close()
   except:
       cursor.close()


def check_username(username):
   '''
       Checks whether a username is already taken or not
   '''
   conn = get_database_connection()
   try:
       cursor = conn.cursor()
       cursor.execute('SELECT * FROM users WHERE username=?', (username, ))
       if cursor.fetchone():
           return True
   except:
       return False


def signup_user(username, password, email):
   '''
       Function for storing the details of a user into the database
       while registering
   '''
   conn = get_database_connection()
   try:
       cursor = conn.cursor()
       cursor.execute("INSERT INTO users(username, password, email) VALUES (?, ?, ?)", (username, password, email))
       conn.commit()
       cursor.close()
       return
   except:
       cursor.close()



def generate_password_hash(password):
   '''
       Function for generating a password hash
   '''
   hashed_value = hashlib.md5(password.encode())
   return hashed_value.hexdigest()
