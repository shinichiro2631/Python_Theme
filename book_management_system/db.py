import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits
    
    salt = ''.join(random.choices(charset, k=32))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha512', b_pw, b_salt, 1246).hex()
    return hashed_password

def insert_user(user_name, mail, password):
    sql = 'INSERT INTO book_user VALUES (default, %s, %s, %s, %s)'
    
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_name, mail, hashed_password, salt))
        count = cursor.rowcount
        connection.commit()
        
    except psycopg2.DatabaseError :
        count = 0
        
    finally :
        cursor.close()
        connection.close()
        
    return count

def login(mail, password):
    sql = 'SELECT id, name, mail, hashed_password, salt FROM book_user WHERE mail = %s'
    flg = False
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail,))
        user = cursor.fetchone()
        if user != None:
            salt = user[4]
            hashed_password = get_hash(password, salt)
            if hashed_password == user[3]:
                flg = True
        else:
            flg = False
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
    return flg

def get_salt():
    charset = string.ascii_letters + string.digits
    salt = ''.join(random.choices(charset, k=32))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, "utf-8")
    b_salt = bytes(salt, "utf-8")
    hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
    return hashed_password

def register_list():
    sql = 'SELECT * FROM book_library;'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,)
        register_list = []
        rows = cursor.fetchall()
        for row in rows :
            register_list.append(row)    
    except psycopg2.DatabaseError:
        count = 0    
    finally:
        cursor.close()
        connection.close()
    return register_list

def insert_book(book_name, book_author, ISBN):
    sql = 'INSERT INTO book_library VALUES (default, %s, %s, %s)'
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (book_name, book_author, ISBN))
        count = cursor.rowcount
        connection.commit()
        
    except psycopg2.DatabaseError :
        count = 0
        
    finally :
        cursor.close()
        connection.close()
        
    return count

def get_books_by_name(key):
    sql='SELECT book_id, book_name, book_author, ISBN FROM book_library WHERE book_name LIKE %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        key='%'+key+'%'
        cursor.execute(sql, (key,))
        rows=cursor.fetchall()
        return rows
    finally :
        cursor.close()
        connection.close()