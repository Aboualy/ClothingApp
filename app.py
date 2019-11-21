#!/usr/bin/env python3
# coding: utf8
import os
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request, abort
from sqlalchemy import or_
import base64
from db_config import bcrypt, db, app
from appforms import RegistrationForm, sForm, Inputs, LoginForm, ClothesForm, MessageSeller
from db_handling import User, Garment, Message


@app.route("/")
@app.route("/home")
def home(garments=None, *args):
    """
    The home page fetches and renders all the clothes available in our database and in addition it has a number of forms
    e.g. search form, messageSeller form and sort form with a view to providing more functionalities to the end-user.
    :param garments: all the clothes stored in our database
    :param args:
    :return:
    """
    form = sForm()
    mSeller = MessageSeller()
    iform = Inputs()
    if garments is None:
        garments = Garment.query.all()
    return render_template('home.html', garments=garments, form=form, iform=iform, mSeller=mSeller)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/privacypolicy")
def privacypolicy():
    return render_template('privacypolicy.html', title='privacypolicy')

@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Register page has a registration form that allows an end-user to create a Login Credentials
    :return:
    """
    users = User.query
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if db.session.query(User).filter_by(email=form.email.data).count() < 1:
            user = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        else:
            flash('email is already registered', 'success')

    return render_template('register.html', title='Register', form=form)


@app.route("/home/<int:garment_id>/message", methods=['GET', 'POST'])
def message(garment_id):
    """
     web page with a message form
    :param garment_id: the unique id that each clothes (post) has
    :return:  renders a page with a message form that allows an en user to contact a specific seller
    """
    mSeller = MessageSeller()
    garments = Garment.query
    users = User.query
    if mSeller.validate_on_submit():
        if current_user.is_authenticated:
            flash(f'You cannot send a message to yourself!', 'failure')
        else:
            gar = garments.filter_by(id=garment_id).first()
            userid = gar.user_id
            user = users.filter_by(id=userid).first()
            message = Message(gar_name= gar.title, msg=mSeller.msg.data, sender=user, )
            db.session.add(message)
            db.session.commit()
            flash('Your message have been successfully sent!', 'success')
            return redirect(url_for('home'))
    return render_template('message.html', title='Message seller',
                           mSeller=mSeller, legend='Message seller')

@app.route("/login", methods=['GET', 'POST'])
def login():
    """
     A web page that allows an end-user with login credentials to login
    :return:
    """
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
    messages = Message.query.all()
    return render_template('account.html', title='Account', garments=garments, messages=messages)


@app.route("/garment/<int:garment_id>/update", methods=['GET', 'POST'])
@login_required
def update_garment(garment_id):
    """
    A web page that allows an end-user with login credentials to update a specific clothes
    :param garment_id:
    :return:
    """
    garment = Garment.query.get_or_404(garment_id)
    if garment.seller != current_user:
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
        #return redirect(url_for('garment', garment_id=garment.id))
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = garment.title
        form.des.data = garment.des
    return render_template('create_garment.html', title='Update Garment',
                           form=form, legend='Update Garment')
    #return render_template('home.html')


@app.route("/garment/<int:garment_id>/delete", methods=['POST'])
@login_required
def delete_garment(garment_id):
    """
    A web page that allows an end-user with login credentials to delete a specific clothes
    :param garment_id:
    :return:
    """
    garment = Garment.query.get_or_404(garment_id)
    db.session.delete(garment)
    db.session.commit()
    flash('Your clothes have been successfully deleted!', 'success')
    return redirect(url_for('account'))


@app.route("/garment/new", methods=['GET', 'POST'])
@login_required
def new_garment():
    """
    A web page that allows an end-user to add new clothes
    """
    form = ClothesForm()
    if form.validate_on_submit():
        gender = str(form.gender.data)
        size = str(form.size.data)
        pic = f'{base64.b64encode(form.pic.data.read()).decode("utf-8")}'
        garment = Garment(title=form.title.data,  gender=gender, size=size, price=form.price.data,  des=form.des.data, seller=current_user, pic=pic)
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
    """
     A web page (with a search form) embedded into our home page that allows an end-user to make a search
    :return:  the result of the search process
    """
    mSeller = MessageSeller()
    form = sForm()
    iform = Inputs()
    garments = Garment.query
    if form.validate_on_submit():
        search_term = form.gare.data
        #garments = garments.filter( Garment.des.like('%' +search_term +'%'))
        garments = garments.filter(or_(Garment.des.like('%' + search_term + '%'), Garment.title.like('%' + search_term + '%'),
                                       Garment.price.like('%' + search_term + '%'), Garment.size.like('%' + search_term + '%'),
                                       Garment.gender.like('%' + search_term + '%')
                                       ))
        garments = garments.order_by(Garment.des).all()
       # return render_template('search.html', form=form, results=results)
        return render_template('home.html', garments=garments, form=form, iform=iform)

    return render_template('search.html', form=form)


@app.route('/sort', methods=['GET', 'POST'])
def sort():
    """
     A web page (with a sort form) embedded into our home page that allows an end-user to sort clothes
    :return: the output is then sorted according to a consumer selection  
    """
    form = sForm()
    iform = Inputs()
    mSeller = MessageSeller()
    garments = Garment.query
    if  iform.validate_on_submit():
        sort_value = iform.myField.data
        if sort_value == "price":
            garments = Garment.query.order_by(Garment.price.desc())
        elif sort_value == "date":
            garments = Garment.query.order_by(Garment.date_posted.desc())
        elif sort_value == "gender":
            garments = Garment.query.order_by(Garment.gender.desc())
        elif sort_value == "size":
            garments = Garment.query.order_by(Garment.size.desc())

        return render_template('home.html', garments=garments, form=form, iform=iform, mSeller=mSeller)

    return render_template('sort.html', iform=iform)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
