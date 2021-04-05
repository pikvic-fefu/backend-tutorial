from flask import Flask, render_template
from datetime import datetime
from post.post import read_posts_from_file

app = Flask(__name__)

posts = read_posts_from_file("posts.txt")

@app.route('/')
def index():
    print(posts)
    return render_template('index.html', posts=posts)

@app.route('/posts/<int:id>')
def about(id):
    if id not in range(len(posts)):
        return "ERROR! Id is out of range" 
    return render_template('post.html', post=posts[id])