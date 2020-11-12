from blog import app, db
from flask import render_template, flash, redirect, url_for, abort, request
from blog.models import Post, User
from blog.forms import LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from blog.utils import title_slugifier, save_picture

## Views ##

@app.route("/")
def homepage(): 
    page_number = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.insert_time.desc()).paginate(page_number, 3, True)
    
    if posts.has_next:
        next_page = url_for("homepage", page=posts.next_num)
    else:
        next_page = None
    
    if posts.has_prev:
        previous_page = url_for("homepage", page=posts.prev_num)
    else:
        previous_page = None

    return render_template("homepage.html", posts=posts, current_page=page_number,
                            next_page=next_page, previous_page=previous_page)

@app.route("/contact")
def contact():
    return render_template("contact_page.html")

@app.route("/about")
def about():
    return render_template("about_page.html")

@app.route("/post/<string:post_slug>")
def post_detail(post_slug):
    # post = Post.query.get_or_404(post_id)
    post = Post.query.filter_by(slug=post_slug).first_or_404()
    return render_template("post_detail.html", post=post)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

## Forms ##

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('username not present in the system!')
            return redirect(url_for('login'))
        if not user.check_password(form.password.data):
            flash('password uncorrect!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('homepage'))
    return render_template("login.html", form=form)

@app.route("/create-post", methods=["GET", "POST"])
@login_required
def post_create():
    form = PostForm()
    if form.validate_on_submit():
        slug = title_slugifier(form.title.data)
        new_post = Post(title=form.title.data, body=form.body.data, slug=slug,
                        description=form.description.data, author=current_user)
        if form.image.data:
            try:
                image = save_picture(form.image.data)
                new_post.image = image
            except Exception:
                db.session.add(new_post)
                db.session.commit()
                flash('Error occoured during image upload')
                return redirect(url_for('post_update', post_id=new_post.id))

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post_detail', post_slug=slug))
    return render_template('post_editor.html', form=form)

@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def post_update(post_id):
    post_instance = Post.query.get_or_404(post_id)
    if post_instance.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post_instance.title = form.title.data
        post_instance.description = form.description.data
        post_instance.body = form.body.data

        if form.image.data:
            try:
                image = save_picture(form.image.data)
                post_instance.image = image
            except Exception:
                db.session.commit()
                flash('Error occoured during image upload')
                return redirect(url_for('post_update', post_id=post_instance.id))

        db.session.commit()
        return redirect(url_for('post_detail', post_slug=post_instance.slug))
    elif request.method == "GET":
        form.title.data = post_instance.title
        form.description.data = post_instance.description
        form.body.data = post_instance.body

    post_image = post_instance.image or None
    return render_template("post_editor.html", form=form, post_image=post_image)

@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def post_delete(post_id):
    post_instance = Post.query.get_or_404(post_id)
    if post_instance.author != current_user:
        abort(403)
    db.session.delete(post_instance)
    db.session.commit()
    return redirect(url_for('homepage'))
