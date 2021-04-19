from flask import Flask, render_template, redirect, request
from datetime import datetime
import sqlite3
import os


DATABASE = 'posts.db'
CREATE_QUERY = """CREATE TABLE IF NOT EXISTS posts
                  (id integer primary key, title text, text text,
                   author text, date text)
               """
POSTS_QUERY = """SELECT * FROM posts"""
POST_QUERY = """SELECT * FROM posts WHERE id = ?"""
INSERT_QUERY = """INSERT INTO posts (title, text, author, date)
                VALUES ('Hello', 'World 123', 'Vasya', '2002-01-02')
                """
INSERT_POST_QUERY = """INSERT INTO posts (title, text, author, date)
                VALUES (?, ?, ?, ?)
                """


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    with get_db_connection() as conn:
        conn.execute(CREATE_QUERY)

def init_db():
    if not os.path.exists(DATABASE):
        create_db()
        with get_db_connection() as conn:
            conn.execute(INSERT_QUERY)
            conn.commit()

def get_posts():
    with get_db_connection() as conn:
        posts = conn.execute(POSTS_QUERY).fetchall()
    return posts

def get_post(id):
    with get_db_connection() as conn:
        post = conn.execute(POST_QUERY, [id]).fetchone()
    return post

def insert_post(post):
    with get_db_connection() as conn:
        parameters = [post['title'], post['text'], post['author'], post['date']]
        conn.execute(INSERT_POST_QUERY, parameters)
        conn.commit()

app = Flask(__name__)

init_db()

@app.route('/')
def index():
    return render_template('index.html', posts=get_posts())

@app.route('/posts/<int:id>')
def about(id):
    if id not in range(1, len(get_posts()) + 1):
        return "", 404
    return render_template('post.html', post=get_post(id))

@app.route('/posts/add')
def posts_add():
    return render_template('post_add.html')

@app.route('/addpost', methods=['post'])
def addpost():
    if request.form:
        title = request.form.get('title')
        author = request.form.get('author')
        date = request.form.get('date')
        text = request.form.get('text')
        tags = request.form.get('tags')
        post = {'title': title, 'author': author, 'date': date, 'text': text}
        insert_post(post)
    return redirect('/')
