from flask import Flask, render_template, request
from flask import redirect as rd
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
db = SQLAlchemy(app)

# URL Routing

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',  methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        users = User.query.all()
        for user in users:
            if email == user.email and password == user.password:
                user_posts = BlogPost.query.filter_by(author=email).all()
                return render_template('posts.html', posts=user_posts, user_id=user.id) 
        return rd('/login')
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        db.session.add(User(email=email, password=password))
        db.session.commit()
        user_id = User.query.filter_by(email=email)[0].id
        user_posts = BlogPost.query.filter_by(author=email).all()
        return render_template('posts.html', posts=user_posts, user_id=user_id)
    else:
        return render_template('signup.html')

@app.route('/posts/<id>', methods=['POST'])
def posts(id):
    if request.method == "POST":
        post_title = request.form['title']
        post_content = request.form['content']
        author = User.query.get(id).email
        db.session.add(BlogPost(title=post_title, content=post_content, author=author))
        db.session.commit()
        user_posts = BlogPost.query.filter_by(author=author).all()
        return render_template('posts.html', posts=user_posts, user_id=id)

@app.route('/delete/<id>')
def delete(id):
    author = BlogPost.query.get(id).author
    user_id = User.query.filter_by(email=author)[0].id
    db.session.delete(BlogPost.query.get(id))
    db.session.commit()
    user_posts = User.query.filter_by(email=author).all()
    return render_template('posts.html', posts=user_posts, user_id=user_id)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        post = BlogPost.query.get(id)
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        
        
        return rd('/posts')
    else:
        post = BlogPost.query.get_or_404(id)
        return render_template('edit.html', post=post)

# Functions


# Creating Models

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(30), nullable=False, default='N/A')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Post #" + str(self.id)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "User #" + str(self.id)


if __name__ == "__main__":
    app.run(debug=True)


# These are unused pieces of code that might come in handy




