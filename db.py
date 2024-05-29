import pymysql
from flask import jsonify

DB_HOST = '192.168.1.142'
DB_USER = 'ama'
DB_PASSWORD = ''
DB_DATABASE = 'wk24todo_db'


def connect_db():
    conn = pymysql.connect(host=DB_HOST,
                           user=DB_USER,
                           port=3306,
                           password=DB_PASSWORD,
                           database=DB_DATABASE,
                           cursorclass=pymysql.cursors.DictCursor)
    return conn


def execute(query, *args):
    conn = connect_db()
    with conn.cursor() as cur:
        try:
            cur.execute(query, args)
            return cur.fetchall()
        finally:
            conn.close()


def validate_key(api_key_usr):
    temp = execute("select id, username from users where api_key = %s", api_key_usr)
    return temp[0]


def validate_key(api_key_usr):
    conn = connect_db()
    with conn.cursor() as cur:
        try:
            sql = """
                select id, username from users where api_key = %s
                """

            cur.execute(sql, [api_key_usr])
            temp = cur.fetchall()
            return temp[0]
        finally:
            conn.close()


def get_tasks(*args):
    conn = connect_db()
    with conn.cursor() as cur:
        try:
            sql = """
                select ToDo.id, ToDo.title, ToDo.done, ToDo.due, ToDo.created_at, ToDo.updated_at, category.category_name
                from ToDo left join category on ToDo.category_id = category.id where ToDo.user_id = %s
                """
            cur.execute(sql, [*args])
            return cur.fetchall()
        finally:
            conn.close()


def create_task(*args):
    conn = connect_db()
    with conn.cursor() as cur:
        try:
            sql = """
               insert into ToDo (user_id, category_id, title, done, due)
               values (%s, %s, %s, %s, %s)
               """
            cur.execute(sql, [*args])
            conn.commit()
            return jsonify({"Success": "Task created successfully"}), 200
        finally:
            conn.close()


def create_category(*args):
    conn = connect_db()
    with conn.cursor() as cur:
        try:
            sql = """
                insert into category (category_name)
                values (%s)
                """
            cur.execute(sql, [*args])
            conn.commit()
            return jsonify({"Success": "Category created successfully"}), 200
        finally:
            conn.close()


def attach_category(*args):
    conn = connect_db()
    with conn.cursor() as cur:
        try:
            sql = """
                    update ToDo 
                    set category_id = %s
                    where id = %s and user_id = %s
                    """
            cur.execute(sql, [*args])
            conn.commit()
            return jsonify({"Success": "Task updated successfully"}), 200
        finally:
            conn.close()


def get_categories():
    conn = connect_db()
    with conn.cursor() as cur:
        try:
            sql = """
                    select * from category
                    """
            cur.execute(sql)
            temp = cur.fetchall()
            return temp
        finally:
            conn.close()


def delete_category(cat_id):
    conn = connect_db()
    with conn.cursor() as cur:
        try:
            sql = """
                    delete from category where id = %s
                    """
            cur.execute(sql, [cat_id])
            conn.commit()
            return jsonify({"Success": "Category deleted successfully"}), 200
        finally:
            conn.close()


def delete_task(*args):
    conn = connect_db()
    with conn.cursor() as cur:
        try:
            sql = """
                delete from ToDo where user_id = %s and id = %s
                """
            cur.execute(sql, [*args])
            conn.commit()
            return jsonify({"Success": "Task deleted successfully"}), 200
        finally:
            conn.close()


def update_tasks(*args):
    conn = connect_db()
    with conn.cursor() as cur:
        try:
            sql = """
                update ToDo 
                set title = %s, done = %s, due = %s
                where id = %s and user_id = %s
                """
            cur.execute(sql, [*args])
            conn.commit()
            return jsonify({"Success": "Task updated successfully"}), 200
        finally:
            conn.close()
