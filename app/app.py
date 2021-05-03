from flask import Flask, render_template, redirect, request
from datetime import datetime
import sqlite3
import os
from app.db.database import Database

DATABASE = 'posts.db'

app = Flask(__name__)

db = Database(DATABASE)
db.init_db()

@app.route('/')
def index():
    posts = db.get_posts()
    for post in posts:
        post = dict(post)
        tags = db.select_tags_for_post(post['id'])
        post["tags"] = tags
        print(post)
    
    return render_template('index.html', posts=posts)

@app.route('/posts/<int:id>')
def about(id):
    if id not in range(1, len(db.get_posts()) + 1):
        return "", 404
    return render_template('post.html', post=db.get_post(id))

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
        post_id = db.insert_post(post)
        tags = tags.split()
        for tag in tags:
            tag_id = db.insert_tag(tag)
            db.insert_post_tag(post_id, tag_id)

    return redirect('/')
