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
def display_entries():
    all_entries=Blog.query.all()
    return render_template('blog_home.html', entries=all_entries)









if __name__ == '__main__':
    app.run()