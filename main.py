from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(3000))

def __init__(id, title, body):
        id.title = title
        id.body = body

@app.route('/', methods=['GET'])
def home():
    
    return render_template('blog_home.html')

@app.route('/blog')
def display_entry():
    entry_id=request.arg.get('id')
    entry=Blog.query.get(entry_id)
    return render_template('blog_home.html', entry=entry)

@app.route('/newpost')
def new_entry():
    if request.method == 'GET':
        return render_template('newpost.html')
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error = ""
        body_error = ""

    if len(blog_title) < 1:
        title_error = "Dude, name yo blog!"

    if len(blog_body) <1:
        body_error = "You must have something to say, duh"

    if not title_error and not body_error:
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        query_parameter = "/newpost?id=" + str(new_blog.id)

    else:
        render_template('newpost.html', title_error=title_error, body_error=body_error)              

if __name__ == '__main__':
    app.run()