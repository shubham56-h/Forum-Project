from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forumdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# creating database schema as class
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return f"<User {self.username}>"
    
@app.route('/', methods=['GET', 'POST'])
def login() :
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('home'))
                
        return render_template('login.html', isVailid=False)

    return render_template('login.html', isVailid=True)

@app.route('/user', methods=['GET', 'POST'])
def user() :
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        new_user = User(full_name=full_name, username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('user.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    isPosted = False
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        new_post = Post(title=title, desc=desc)

        db.session.add(new_post)
        db.session.commit()
        isPosted = True
    return render_template('index.html', posted=isPosted)

@app.route('/posts')
def posts():
    all_posts = Post.query.all()
    return render_template('posts.html', posts=all_posts)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_post(id):
    post_to_delete = Post.query.get(id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect('/posts')

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_post(id):
    post_to_edit = Post.query.get(id)
    if request.method == 'POST':
        post_to_edit.title = request.form.get('title')
        post_to_edit.desc = request.form.get('desc')
        # print(post_to_edit.desc)
        db.session.commit()
        return redirect('/posts')
    return render_template('index.html', post=post_to_edit)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
