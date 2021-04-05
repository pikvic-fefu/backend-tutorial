from flask import Flask, render_template, redirect, request
from datetime import datetime
from post.post import read_posts_from_file, Post

DATABASE = 'posts.txt'

app = Flask(__name__)

posts = read_posts_from_file(DATABASE)

@app.route('/')
def index():
    print(posts)
    return render_template('index.html', posts=posts)

@app.route('/posts/<int:id>')
def about(id):
    if id not in range(len(posts)):
        return "ERROR! Id is out of range" 
    return render_template('post.html', post=posts[id])

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
