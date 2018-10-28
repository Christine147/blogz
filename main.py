from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_body = db.Column(db.String(3000))

    def __init__(self, blog_title, blog_body):
        self.blog_title = blog_title
        self.blog_body = blog_body

@app.route('/', methods=['GET'])
def home():
    show_blog = Blog.query.all()
    return render_template('blog_home.html', show_blog=show_blog)

@app.route('/blog_home', methods=['POST','GET'])
def display_entry():
    show_blog = Blog.query.all()
    return render_template('blog_home.html', show_blog=show_blog)

@app.route('/newpost', methods=['POST', 'GET'])
def new_entry():
        
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        title_error = ''
        body_error = ''

        if not blog_title:
            title_error = "Dude, name yo blog!"

        if not blog_body:
            body_error = "You must have something to say, duh"

        if not blog_title or not blog_body:
            return render_template('newpost.html', title_error=title_error, body_error=body_error,
            blog_title=blog_title, blog_body=blog_body)
        
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect ('/blog_home')
    
                      
    return render_template('newpost.html')

@app.route('/single_blog')
def single_blog():
    new_id = request.args.get('id')
    find_title = Blog.query.get(new_id).blog_title
    find_body = Blog.query.get(new_id).blog_body
    return render_template ('single_blog.html', find_title=find_title, find_body=find_body)    

if __name__ == '__main__':
    app.run()