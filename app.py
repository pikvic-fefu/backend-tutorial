from flask import Flask, render_template, redirect, request
from datetime import datetime
from post.post import read_posts_from_file, Post
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

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    conn = get_db_connection()
    conn.execute(CREATE_QUERY)
    conn.commit()
    conn.close()

def init_db():
    if not os.path.exists(DATABASE):
        create_db()
        conn = get_db_connection()
        conn.execute(INSERT_QUERY)
        conn.commit()
        conn.close()

def get_posts():
    conn = get_db_connection()
    posts = conn.execute(POSTS_QUERY).fetchall()
    conn.close()
    return posts

def get_post(id):
    conn = get_db_connection()
    post = conn.execute(POST_QUERY, [(id)]).fetchone()
    conn.close()
    return post

app = Flask(__name__)

init_db()

posts = get_posts()

@app.route('/')
def index():
    return render_template('index.html', posts=get_posts())

@app.route('/posts/<int:id>')
def about(id):
    if id not in range(1, len(posts) + 1):
        return "ERROR! Id is out of range"
    print(dict(get_post(id)))
    return render_template('post.html', post=get_post(id))

@app.route('/posts/add')
def posts_add():
    return render_template('post_add.html')

@app.route('/addpost', methods=['post'])
def addpost():
    global posts
    if request.form:
        title = request.form.get('title')  # запрос к данным формы
        author = request.form.get('author')
        date = request.form.get('date')
        text = request.form.get('text')
        tags = request.form.get('tags')
        id = len(posts)
        post = Post(id, title, author, date, text, tags)
        print(post)
        post.save_post(DATABASE)
        posts = read_posts_from_file(DATABASE)
    return redirect('/')
