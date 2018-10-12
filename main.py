from flask import Flask, request, redirect, render_template, sessions, flash
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

    def __init__(self, title, body):
        self.title = title
        self.body = body
        

@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():

    title_error = ""
    body_error = ""

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if len(title) == 0:
            title_error = "Title can not be left blank"
        if len(body) == 0:
            body_error = "Blog body can not be left blank"

        if not title_error and not body_error:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            id = new_blog.id
            return redirect('/blog?id={}'.format(id))

    return render_template('newpost.html', title_error=title_error, body_error=body_error)

@app.route('/blog', methods=['POST', 'GET'])
def home():
        
    blogs = Blog.query.all()
    id = request.args.get("id")
    if id is not None:
        blog = Blog.query.get(str(id))
        return render_template('single_blog.html', blog=blog)


    return render_template('blog.html', blogs=blogs)


        


    
if __name__ == '__main__':
    app.run()