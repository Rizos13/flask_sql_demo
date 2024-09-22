import psycopg2
#import os
from flask import Flask, render_template, request, flash, session, redirect, url_for, abort, g
from FDataBase import FDataBase


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alisasmirnova:mypassword@localhost:5432/postgres'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'fdgfh78@#5?>gfhf89dx,v06k'


def connect_db():
    conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    conn.autocommit = True
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().execute(f.read())
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu = dbase.getMenu(), posts=dbase.getPostsAnonce())


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) >= 1:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('ERROR  of add post', category='error')
            else:
                flash('Post added successfully', category='success')
        else:
            flash('ERROR  of add post', category='error')

    return render_template('addpost.html', menu=dbase.getMenu(), title="Add post")


@app.route("/post/<int:id_post>")
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

if __name__ == "__main__":
    app.run(debug=True)


