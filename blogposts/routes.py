from flask import render_template, url_for, flash, redirect, request
from blogposts.models import User, Post
from blogposts.forms import RegistrationForm, LoginForm
from blogposts import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts = [{
    'name': 'Shiva',
    'date_posted': 20190213,
    'author': 'sredhangali',
    'content': 'i ama a name of the '

}, {
    'name': 'Himesh',
    'date_posted': 20180213,
    'author': 'srikanta',
    'content': 'this is a test done to get'

}]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='about')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!!.You are able to Log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title=' Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
   return render_template('account.html',title='Account')   