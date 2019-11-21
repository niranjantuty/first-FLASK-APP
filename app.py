# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 05:32:13 2019

@author: Niranjan
"""
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

# arranging things in the database
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default="N/A")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post'+ str(self.id)

all_posts = [
    {
        'title': 'Post 1',
        'content': 'This is the content of Post 1. What the fuck !',
        'author': 'Niranjan'
    },
    {
        'title': 'Post 2',
        'content': 'This is the content of Post 2. What the fuck !'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts',methods=['POST','GET'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)  # will be added for only the current session
        db.session.commit()  # will save permanently in db file
        return redirect('/posts')

    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


@app.route('/home/users/<string:name>/id/<int:id>')
def hello(name,id):
    return "Hello, "+ name +" your id is: " + str(id)

@app.route('/onlyget', methods=['GET','POST'])
def onlyget():
    return "You can only get this page"

# debugging mode
if __name__ == "__main__":
    app.run(debug=True)
