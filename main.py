from flask import Flask, request, redirect, render_template, sessions
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:0791@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#app.secret_key = "y336789sg34"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    body = db.Column(db.String(400))

    def __init__(self, name):
        self.name = name

@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
    

        return redirect('/')
    return render_template('newpost.html')

@app.route('/blog', methods=['POST', 'GET'])
def home():
    blogs = Blog.query.get(new_blog)
    return render_template('blog.html')



#@app.route('/', methods=['POST', 'GET'])
#def index():

    #blogs =
    #return render_template('blog.html')
        


    
if __name__ == '__main__':
    app.run()