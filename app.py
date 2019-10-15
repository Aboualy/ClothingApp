import os
import secrets
from PIL import Image
from werkzeug.datastructures import FileStorage
import base64
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

from clothes import ClothesForm
from db_handling import User, Garment
from loginpage import LoginForm
from userreg import RegistrationForm, searchForm
from db_config import bcrypt, db, app


@app.route("/")
@app.route("/home")
def home(garments=None):
    if garments is None:
        garments = Garment.query.all()

    return render_template('home.html', garments=garments)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


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


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    garments = Garment.query.all()

    return render_template('account.html', title='Account',garments=garments)


@app.route("/garment/<int:garment_id>/update", methods=['GET', 'POST'])
@login_required
def update_garment(garment_id):
    garment = Garment.query.get_or_404(garment_id)
    if garment.author != current_user:
        abort(403)
    form = ClothesForm()
    if form.validate_on_submit():
        garment.title = form.title.data
        garment.gender = form.gender.data
        garment.size = form.size.data
        garment.price = form.price.data
        garment.des = form.des.data
        garment.pic = f'{base64.b64encode(form.pic.data.read()).decode("utf-8")}'
        db.session.commit()
        flash('Your garment has been updated!', 'success')
        return redirect(url_for('garment', garment_id=garment.id))
    elif request.method == 'GET':
        form.title.data = garment.title
        form.des.data = garment.des
    return render_template('create_garment.html', title='Update Garment',
                           form=form, legend='Update Garment')




@app.route("/garment/<int:garment_id>/delete", methods=['POST'])
@login_required
def delete_garment(garment_id):
    garment = Garment.query.get_or_404(garment_id)
    db.session.delete(garment)
    db.session.commit()
    flash('Your clothes have been successfully deleted!', 'success')
    return redirect(url_for('account'))

@app.route("/garment/new", methods=['GET', 'POST'])
@login_required
def new_garment():
    form = ClothesForm()
    if form.validate_on_submit():
        gender = str(form.gender.data)
        size = str(form.size.data)
        print(size)
        pic = f'{base64.b64encode(form.pic.data.read()).decode("utf-8")}'
        garment = Garment(title=form.title.data,  gender=gender, size=size, price=form.price.data, des=form.des.data, author=current_user, pic=pic)
        db.session.add(garment)
        db.session.commit()
        flash('Your clothes have been successfully added!', 'success')
        return redirect(url_for('home'))
    return render_template('create_garment.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/garment/<int:garment_id>")
def garment(garment_id):
    garment = Garment.query.get_or_404(garment_id)
    return render_template('garment.html', title=garment.title, garment=garment)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = searchForm()
    garments = Garment.query.all()
    if form.validate_on_submit():
        search_term = form.query.data
        print(search_term)
        results = garments.filter(Garment.des.like('%' + search_term + '%'))
        print(results)
        return render_template('search.html', form=form, results=results)

    return render_template('search.html', form=form)




if __name__ == '__main__':
    app.run()
