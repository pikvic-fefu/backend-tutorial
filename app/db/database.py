from app.db.query import * 
import os.path
import sqlite3

class Database:
    
    def __init__(self, database_name):
        self.database_name = database_name

    def get_db_connection(self):
        conn = sqlite3.connect(self.database_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create_db(self):
        with self.get_db_connection() as conn:
            conn.execute(CREATE_QUERY_POSTS)
            conn.execute(CREATE_QUERY_TAGS)
            conn.execute(CREATE_QUERY_POSTS_TAGS)

    def init_db(self):
        if not os.path.exists(self.database_name):
            self.create_db()
            with self.get_db_connection() as conn:
                conn.execute(INSERT_QUERY)
                conn.commit()

    def get_posts(self):
        with self.get_db_connection() as conn:
            posts = conn.execute(POSTS_QUERY).fetchall()
        return posts

    def get_post(self, id):
        with self.get_db_connection() as conn:
            post = conn.execute(POST_QUERY, [id]).fetchone()
        return post

    def insert_post(self, post):
        with self.get_db_connection() as conn:
            parameters = [post['title'], post['text'], post['author'], post['date']]
            cur = conn.cursor()
            cur.execute(INSERT_POST_QUERY, parameters)
            lastrowid = cur.lastrowid
            conn.commit()
        return lastrowid

    def insert_tag(self, tag):
        with self.get_db_connection() as conn:
            parameters = [tag]
            cur = conn.cursor()
            tag = cur.execute('SELECT * FROM tags WHERE title = ?', parameters).fetchone()
            if tag:
                lastrowid = tag['id']            
            else:
                cur.execute(INSERT_TAG_QUERY, parameters)
                lastrowid = cur.lastrowid
                conn.commit()
        return lastrowid

    def insert_post_tag(self, post_id, tag_id):
        with self.get_db_connection() as conn:
            parameters = [post_id, tag_id]
            conn.execute(INSERT_POST_TAG_QUERY, parameters)
            conn.commit()

    def get_max_id(self, table):
        with self.get_db_connection() as conn:
            max_id = conn.execute(f"SELECT MAX(id) as id FROM {table}").fetchone()
        return max_id["id"]

    def select_tags_for_post(self, post_id):
        with self.get_db_connection() as conn:
            parameters = [post_id]
            tags = conn.execute(TAGS_FOR_POST, parameters).fetchall()
        tags = [dict(tag) for tag in tags]
        return tags

    def select_count_for_tags(self):
        with self.get_db_connection() as conn:
            tags = conn.execute(SELECT_COUNT_POSTS_FOR_TAGS).fetchall()
        tags = [dict(tag) for tag in tags]
        return tags