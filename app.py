"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "dragons"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def get_users_list():
    users = User.query.all()
    return render_template('list.html', users = users)

@app.route('/create_user')
def create_user_form():
    return render_template('create_user.html')

@app.route('/create_user', methods=["POST"])
def create_user_post():
    first = request.form['first_name']
    last = request.form['last_name']
    pic_url = request.form['url']

    new_user = User(first_name=first, last_name=last, image_url=pic_url)
    if not new_user.image_url:
        new_user.image_url = "https://www.clipartkey.com/mpngs/m/100-1006688_headshot-silhouette-placeholder-image-person-free.png" 
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

@app.route('/user/<user_id>')
def user_info(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users.html', user=user)

@app.route('/edit_user/<user_id>')
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/edit_user/<user_id>', methods=["POST"])
def submit_edit(user_id):
    first = request.form['first_name']
    last = request.form['last_name']
    pic_url = request.form['url']
    user = User.query.get_or_404(user_id)
    if first:
        user.first_name = first
    if last:
        user.last_name = last
    if pic_url:
        user.image_url = pic_url
    db.session.commit()
    return redirect('/')

@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    User.query.filter_by(id = user_id).delete()
    db.session.commit()
    return redirect('/')


    