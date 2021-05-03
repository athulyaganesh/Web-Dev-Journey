import sqlite3
from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.exceptions import abort

app= Flask(__name__)
app.config['SECRET_KEY']='4a56thH9kf'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory=sqlite3.Row
    return conn

def get_post(post_id):
    conn=get_db_connection()
    post = conn.execute('SELECT * from posts where id=?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/')
def index():
    conn=get_db_connection()
    posts=conn.execute('SELECT * from posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/create',methods=('GET','POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content=request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn=get_db_connection()
            conn.execute('INSERT INTO posts(title,content) VALUES(?,?)',
                         (title,content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:num_id>/edit', methods=('GET','POST'))
def edit(num_id):
    post=get_post(num_id)

    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn=get_db_connection()
            conn.execute('UPDATE posts SET title=?, content=?'
                     'WHERE id=?', (title, content,num_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('edit.html',post=post)

@app.route('/<int:num_id>/delete',methods=('POST',))
def delete(num_id):
    post=get_post(num_id)
    conn=get_db_connection()
    conn.execute('DELETE FROM posts where id=?', (num_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))
    

if __name__=='__main__':
    app.run(debug=True)

    
#https://morioh.com/p/20750b8a8580
