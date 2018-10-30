from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from hashutils import make_pw_hash, check_pw_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Cupcake21@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'zephyr'


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')
    
    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    post = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, title, post, owner):
        self.title = title
        self.post = post
        self.owner = owner
  
@app.before_request
def require_login():
    allowed_routes = ['login', 'list_blogs', 'index', 'signup' 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['Password']
        user = User.query.filter_by(username=username).first()

        username_error = ''
        password_error = ''

        if not username and not password:
            username_error = "Username can't be empty."
            password_error = "Password can't be empty."
            return render_template('login.html', username_error = username_error, password_error = password_error)
        if not password:
            password_error = "Password can't be empty."
            return render_template('login.html', password_error = password_error, username = username)
        if not username:
            username_error = "Username can't be empty."
            return render_template('login.html', username_error = username_error)

        if user and check_pw_hash(password, user.pw_hash):
            session['username'] = username
            return redirect('/newpost')
        if user and not user.pw_hash == password:
            password_error = "Incorrect password. Please try again."
            return render_template('login.html', password_error = password_error, username = username)
        if not user:
            username_error = "Username required."
            return render_template('login.html', username_error = username_error)

    else:
        return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['Password']
        verify = request.form['VerifyPassword']

        username_error = ''
        password_error = ''
        verify_error = ''
        existing_user = User.query.filter_by(username=username).first()
        
        if not username or not password or not verify:
            username_error = "Username required."
            return render_template('signup.html', username_error = username_error)
        
        if len(username) < 3:
            username_error = "Username must be at least three characters."
            return render_template('signup.html', username_error = username_error)
        if len(password) < 3:
            password_error = "Password must be at least three characters."
            return render_template('signup.html', password_error = password_error, username = username, username_error = username_error)

        if existing_user:
            username_error = "Username already exists."
            return render_template('signup.html', username_error = username_error)

        if not existing_user and not password==verify:
            password_error = "Passwords do not match"
            verify_error = "Passwords do not match"
            return render_template('signup.html', username = username, password_error = password_error, verify_error = verify_error)

        if not existing_user and password==verify:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        
    else: 
        return render_template('signup.html')


@app.route('/blog', methods=['POST', 'GET'])
def list_blogs():
    post_id = request.args.get('id')
    author_id = request.args.get('owner_id')
    all_posts = Blog.query.all()
    if post_id:
        indv_post = Blog.query.get(post_id)
        return render_template('single_blog.html', posts=indv_post)
    if author_id:
        posts_from_author = Blog.query.filter_by(owner_id=author_id)
        return render_template('singleUser.html', posts=posts_from_author)
    
    return render_template('blog.html', posts=all_posts)


def empty(x):
    if len(x) == 0:
        return True
    else:
        return False


@app.route('/newpost', methods=['GET', 'POST'])
def add_entry():

    if request.method == 'POST':
        title_error = ''
        body_error = ''

        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        owner = User.query.filter_by(username=session['username']).first()
        new_post = Blog(blog_title, blog_body, owner)

        if not empty(blog_title) and not empty(blog_body):
            db.session.add(new_post)
            db.session.commit()
            post_link = "/blog?id=" + str(new_post.id)
            return redirect(post_link)
        else:
            if empty(blog_title) and empty(blog_body):
                title_error = "Dude, name yo blog!"
                body_error = "You must have something to say, duh"
                return render_template('newpost.html', title_error=title_error, body_error=body_error)
            elif empty(blog_title) and not empty(blog_body):
                title_error = "Title is missing."
                return render_template('newpost.html', title_error=title_error, blog_body=blog_body)
            elif empty(blog_body) and not empty(blog_title):
                body_error = "Blog entry is missing."
                return render_template('newpost.html', blog_title=blog_title, body_error=body_error,)

    else: 
        return render_template('newpost.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


@app.route('/')
def index():
    all_users = User.query.distinct()
    return render_template('index.html', usernames=all_users)



if __name__ == '__main__':
    app.run()