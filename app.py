"""Blogly application."""
from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post, Tag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "penguinz!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def home_page():
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('posts/home.html', posts=recent_posts)

@app.route("/users/all_users")
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('users/all_users.html', users=users)

@app.route("/users/<int:id>")
def show_user(id):
    """Show details about a user"""
    user = User.query.get_or_404(id)
    return render_template('users/user_details.html', user=user)

@app.route('/users/new')
def add_user_form():
    return render_template("users/new_user_form.html")

@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None
    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    flash(f"User: {first_name} {last_name} Added!")
    return redirect(f"{new_user.id}")


@app.route('/users/<int:id>/edit_user')
def edit_user(id):
    user = User.query.get_or_404(id)
    return render_template('users/edit_user.html', user=user)

@app.route('/users/<int:id>/edit_user', methods=["POST"])
def submit_edit_user(id):
    user = User.query.get_or_404(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    #image_url = image_url if image_url else None

    db.session.add(user)
    db.session.commit()

    flash(f"User: {user.full_name} Has Been Updated!")
    return redirect(f"/users/{user.id}")


@app.route('/users/<int:id>/delete', methods=["POST", "GET"])
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    flash(f"User: {user.first_name} {user.last_name} Has Been Deleted!")
    return redirect('/')



    ###########################################

                    #POSTS#

    ###########################################

@app.route('/users/<int:id>/new_post')
def add_post_form(id):
    user = User.query.get_or_404(id)
    tags = Tag.query.all()
    return render_template("posts/new_post_form.html", user=user, tags=tags)

@app.route('/users/<int:id>/new_post', methods=["POST"])
def create_post(id):
    user = User.query.get_or_404(id)
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title,
                    content=content, user=user, tags=tags)
    db.session.add(new_post)
    db.session.commit()

    flash("New Post Added!")
    return redirect(f"/posts/show_post/{new_post.id}")
    #return redirect("/new")

@app.route("/posts/show_post/<int:id>")
def show_post(id):
    """Show a specific post"""
    post = Post.query.get_or_404(id)
    return render_template('posts/show_post.html', post=post)

@app.route('/posts/<int:id>/edit_post')
def edit_post(id):
    post = Post.query.get_or_404(id)
    tags = Tag.query.all()
    return render_template('posts/edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:id>/edit_post', methods=["POST"])
def submit_post_edit(id):
    post = Post.query.get_or_404(id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()

    flash("Post Updated!")
    return redirect("/")

@app.route('/posts/<int:id>/delete', methods=["POST", "GET"])
def delete_post(id):
    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    flash(f"Post: {post.title} Has Been Deleted!")
    return redirect('/')

@app.route("/posts/all_posts")
def list_posts():
    """Shows list of all posts in db"""
    posts = Post.query.all()
    return render_template('posts/all_posts.html', posts=posts)


    ###########################################

                    #TAGS#

    ###########################################

@app.route('/tags/new')
def add_tag_form():
    return render_template("tags/new_tag.html")

@app.route('/tags/new', methods=["POST"])
def create_tag():

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['tag_name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/")

@app.route("/tags")
def list_tags():
    """Shows list of all tags in db"""
    tags = Tag.query.all()
    return render_template('tags/all_tags.html', tags=tags)

@app.route('/tags/<int:id>')
def show_tag(id):
    tag = Tag.query.get_or_404(id)
    return render_template('tags/show_tag.html', tag=tag)

@app.route('/tags/<int:id>/edit')
def edit_tag(id):
    tag = Tag.query.get_or_404(id)
    return render_template('tags/edit_tag.html', tag=tag)

@app.route('/tags/<int:id>/edit', methods=["POST"])
def submit_tag_edit(id):
    tag = Tag.query.get_or_404(id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")
    return redirect("/")