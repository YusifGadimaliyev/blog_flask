from blog import app, db, mail
from blog.forms import SignUpForm, LoginForm, PostForm, ContactForm
from blog.models import User, Post

from datetime import datetime
from flask_mail import Message
from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import login_user, logout_user, login_required, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/home")
@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.post_date.desc()).paginate(page=page, per_page=3)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template("index.html", title='Home page', posts=posts, next_url=next_url, prev_url=prev_url, page=page)


@app.route("/about")
def about():
    title = "About page"
    return render_template("about.html", title=title)

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    title = "Sign up page"
    form = SignUpForm()
    if form.validate_on_submit():
        create_user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            confirmed=False
        )
        db.session.add(create_user)
        db.session.commit()
        flash(f"Successfully registered!", "success")
        return redirect(url_for("login"))

    return render_template("sign_up.html", form=form, title=title)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    title = "Login page"
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash(f"email or password incorrect!", "danger")
    return render_template("login.html", form=form, title=title)


@app.route("/logout")
def log_out_user():
    logout_user()
    return redirect(url_for("index"))


@app.route("/add-post", methods=["GET", "POST"])
@login_required
def add_post():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    title = "Post Create page"
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            content=form.content.data,
            user=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash(f"Post successfully created", "success")
        return redirect(url_for("index"))
    return render_template("create_post.html", form=form, title=title)
    

@app.route("/post-details/<int:post_id>/")
def post_details(post_id):
    title = "Post detail page"
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post, title=title)


@app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    title = "Post update page"
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.content = form.content.data
        post.post_date = datetime.now()
        db.session.commit()
        flash(f"Your post are successfully edited", "success")
        return redirect(url_for("index"))
    elif request.method == "GET":
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.content.data = post.content
    return render_template("post_update.html", form=form, title=title)
    

@app.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post deleted!', 'warning')
    return redirect(url_for("index"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    title = "Contact form page"
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        msg = Message(
            subject,
            recipients=[app.config['MAIL_USERNAME']],
            body=message,
            sender=form.email.data)
        mail.send(msg)
        flash(f"We are recieved your message successfully", "success")
    return render_template("contact.html", form=form, title=title)
