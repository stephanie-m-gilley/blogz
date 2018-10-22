from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:0791@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "y336789sg34"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    body = db.Column(db.String(400))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(15))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged In")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

    #the bs below is no worky and buggy AF!  >:(

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()

        #TODO add conditionals to authenticate a valid user login 

        if not existing_user and len(username) > 3 and len(password) > 3 and password == verify:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username

            return redirect('/newpost')
        
        if len(username) == 0:
            flash('Required Field')
        if len(username) < 3:
            flash('Username must be more than 3 characters')

        if len(password) == 0: #only catching this 1.... why!?
            flash('Required Field')
        if len(password) < 3 and len(password) >= 1:
            flash('Must be more than 3 characters')
        if password != verify:
            flash('Passwords do not match')#logs someone in even with just a password

        if username == existing_user:
            flash('Existing User')

    
        

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    flash('Logout Successful!')
    return redirect('/blog')


@app.route('/', methods=['POST', 'GET'])
def index():

    authors = User.query.all()
    return render_template('index.html', authors=authors)
    



@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():

    title_error = ""
    body_error = ""
    owner = User.query.filter_by(username=session['username']).first()
    

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if len(title) == 0:
            title_error = "Title can not be left blank"
        if len(body) == 0:
            body_error = "Blog body can not be left blank"

        if not title_error and not body_error:
            new_blog = Blog(title, body, owner)
            db.session.add(new_blog)
            db.session.commit()
            id = new_blog.id
            return redirect('/blog?id={}'.format(id))

    return render_template('newpost.html', title_error=title_error, body_error=body_error)

@app.route('/blog', methods=['POST', 'GET'])
def blog(): 
        
    id = request.args.get("id")
    user = request.args.get("user")
    blogs = Blog.query.all()
    authors = User.query.all()
    

    if user is not None:
        owner = User.query.filter_by(username=user).first()
        user_blogs = Blog.query.filter_by(owner_id=owner.id).all()
        return render_template('singleUser.html', user_blogs=user_blogs, authors=authors)

    if id is not None:
        blog = Blog.query.get(str(id))
        return render_template('single_blog.html', blog=blog, authors=authors)
    


    return render_template('blog.html', blogs=blogs, authors=authors)


        


    
if __name__ == '__main__':
    app.run()