import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from lab_bank import app, db, bcrypt
from lab_bank.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from lab_bank.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():

    posts = Post.query.all()
    return render_template('home.html', title = 'Página Inicial', posts = posts)  # mágica???


@app.route('/about')
def about():

    return render_template('about.html', title='About')


@app.route('/user/<username>')
def user(username):

    return f'<h1> Usuário: {escape(username)} </h1>'


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:

        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Conta criada para {form.username.data}', 'success')

        return redirect(url_for('login')) # or home?

    return render_template('register.html', title='Registrar', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:

        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email = form.email.data).first()

        if (user and bcrypt.check_password_hash(user.password, form.password.data)):

            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:

            flash(f'Login incorreto, verifique email e senha', 'danger')

    return render_template('login.html', title='Entrar', form=form)

@app.route('/logout')
def logout():

    logout_user()

    return redirect(url_for('home'))

def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', 'profile_pictures', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()

    if form.validate_on_submit():

        if form.picture.data:

            picture_file = save_picture(form.picture.data)
            current_user.profile_picture = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Sua conta foi atualizada', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':

        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_picture = url_for('static', filename = 'profile_pictures/' + current_user.profile_picture)

    return render_template('account.html', title='Account', profile_picture = profile_picture, form = form)
    
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
     
    form = PostForm()
    
    if form.validate_on_submit():
        
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Atualização postada', 'success')
        
        return redirect(url_for('home'))
     
    return render_template('create_post.html', title='Atualização', form = form)
    
@app.route('/post/<int:post_id>/')
def post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    return render_template('post.html', title = post.title, post = post)
    
@app.route('/post/<int:post_id>/update/')
@login_required
def update_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        
        abort(403)
        
    form = PostForm()
    
    return render_template('create_post.html', title='Editar atualização', form = form)