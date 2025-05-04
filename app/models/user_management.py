from app.models.user import get_db_connection
from werkzeug.security import generate_password_hash
import pymysql

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT id, name, email, role, created_at FROM users ORDER BY name')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def get_user_by_username(name):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE name = %s', (name,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def create_user(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = generate_password_hash(data['password'])
    cursor.execute('''
        INSERT INTO users (name, email, password, role)
        VALUES (%s, %s, %s, %s)
    ''', (data['name'], data['email'], hashed_password, data['role']))
    conn.commit()
    cursor.close()
    conn.close()

def update_user(user_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if data.get('password'):
        hashed_password = generate_password_hash(data['password'])
        cursor.execute('''
            UPDATE users 
            SET name = %s, email = %s, password = %s, role = %s
            WHERE id = %s
        ''', (data['name'], data['email'], hashed_password, data['role'], user_id))
    else:
        cursor.execute('''
            UPDATE users 
            SET name = %s, email = %s, role = %s
            WHERE id = %s
        ''', (data['name'], data['email'], data['role'], user_id))
    
    conn.commit()
    cursor.close()
    conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT id, name, email, role FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user 