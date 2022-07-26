"""Blogly application."""
from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User
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
    return render_template('/base.html')


@app.route("/users/all_users")
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('users/all_users.html', users=users)

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
    #return redirect("/new")


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

    flash(f"User: {user.first_name} {user.last_name} Has Been Updated!")
    return redirect('/')


@app.route('/users/<int:id>/delete', methods=["POST", "GET"])
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    flash(f"User: {user.first_name} {user.last_name} Has Been Deleted!")
    return redirect('/')

@app.route('/users/new')
def add_user_form():
    return render_template("users/new.html")

@app.route("/users/<int:id>")
def show_user(id):
    """Show details about a user"""
    user = User.query.get_or_404(id)
    return render_template('users/user_details.html', user=user)
