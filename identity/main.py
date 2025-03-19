# auth_backend.py

from gmssl import sm3, func
import sqlite3
import uuid
import re

DB_NAME = 'users.db'

def init_db():
    """初始化数据库，创建用户表（如果不存在）"""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"数据库初始化失败: {e}")

def register_user(username, password):
    """
    注册新用户
    :param username: 用户名
    :param password: 密码
    :return: (boolean, message) 注册是否成功及信息
    """
    if not username or not password:
        return False, '用户名和密码不能为空！'

    if not is_valid_password(password):
        return False, '密码强度不足，需包含字母和数字，长度至少8位！'

    if user_exists(username):
        return False, '用户名已存在！'

    # 生成随机盐值
    salt = uuid.uuid4().hex
    password_hash = hash_password(password, salt)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # 存储新用户
            cursor.execute('INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)', (username, password_hash, salt))
            conn.commit()
        return True, '注册成功！'
    except sqlite3.Error as e:
        return False, f'注册失败，数据库错误: {e}'

def login_user(username, password):
    """
    用户登录验证
    :param username: 用户名
    :param password: 密码
    :return: (boolean, message) 登录是否成功及信息
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # 获取存储的密码哈希和盐值
            cursor.execute('SELECT password_hash, salt FROM users WHERE username=?', (username,))
            result = cursor.fetchone()

        if result:
            stored_password_hash, salt = result
            password_hash_input = hash_password(password, salt)
            if password_hash_input == stored_password_hash:
                return True, '登录成功！'
            else:
                return False, '密码错误！'
        else:
            return False, '用户不存在！'
    except sqlite3.Error as e:
        return False, f'登录失败，数据库错误: {e}'

def change_password(username, new_password):
    """
    修改指定用户名的密码
    :param username: 用户名
    :param new_password: 新密码
    :return: (boolean, message) 修改操作是否成功及信息
    """
    if not username or not new_password:
        return False, '用户名和新密码不能为空！'

    if not is_valid_password(new_password):
        return False, '新密码强度不足，需包含字母和数字，长度至少8位！'

    if not user_exists(username):
        return False, '用户不存在！'

    # 生成新的盐值并哈希密码
    new_salt = uuid.uuid4().hex
    new_password_hash = hash_password(new_password, new_salt)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # 更新密码哈希和盐值
            cursor.execute('UPDATE users SET password_hash=?, salt=? WHERE username=?', (new_password_hash, new_salt, username))
            conn.commit()
        return True, '密码修改成功！'
    except sqlite3.Error as e:
        return False, f'修改密码失败，数据库错误: {e}'

def user_exists(username):
    """
    检查用户名是否已存在
    :param username: 用户名
    :return: True or False
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM users WHERE username=?', (username,))
            return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"数据库查询失败: {e}")
        return False

def hash_password(password, salt):
    """
    使用SM3算法和盐值对密码进行哈希处理
    :param password: 明文密码
    :param salt: 盐值
    :return: 哈希值
    """
    # 将密码和盐值组合
    combined = password + salt
    hash_bytes = combined.encode('utf-8')
    hash_hex = sm3.sm3_hash(func.bytes_to_list(hash_bytes))
    return hash_hex

def is_valid_password(password):
    """
    检查密码强度，要求至少8位，包含字母和数字
    :param password: 密码
    :return: True or False
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

# 初始化数据库
init_db()