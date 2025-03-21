from operator import pos
from flask import render_template, Blueprint, flash, g, redirect, request, url_for

from werkzeug.exceptions import abort

from models.db_config import db
from models.post_model import Post
from models.user_model import User
from controllers.auth_controller import login_required


blog = Blueprint('blog', __name__)

#Obtner un ususario
def get_user(id):
    user = User.query.get_or_404(id)
    if g.user.role == "profesor" and user.role != "instructor_profesores":
        return None
    elif g.user.role == "estudiante" and user.role != "instructor_estudiantes":
        return None
    return user

@blog.route("/")
def index():
    if g.user:
        if g.user.role == "profesor":
            posts = Post.query.join(User).filter(User.role == "instructor_profesores").all()
        elif g.user.role == "estudiante":
            posts = Post.query.join(User).filter(User.role == "instructor_estudiantes").all()
        else:
            posts = Post.query.filter_by(author=g.user.id).all()
    else:
        posts = []
    posts = list(reversed(posts))
    db.session.commit()
    return render_template('blog/index.html', posts = posts, get_user=get_user)

#Registrar un post 
@blog.route('/blog/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        post = Post(g.user.id, title, body)

        error = None
        if not title:
            error = 'Se requiere un título'
        else:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
        
        flash(error)
        
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = Post.query.get(id)

    if post is None:
        abort(404, f'Id {id} de la publicación no existe.')

    if check_author and post.author != g.user.id:
        abort(404)
    
    return post

#Update post 
@blog.route('/blog/update/<int:id>', methods=('GET','POST'))
@login_required
def update(id):

    post = get_post(id) 

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.body = request.form.get('body')

        error = None
        if not post.title:
            error = 'Se requiere un título'
        else:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
        
        flash(error)
        
    return render_template('blog/update.html', post=post)

#Eliminar un post
@blog.route('/blog/delete/<int:id>')
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('blog.index'))