from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, TextAreaField, FileField, \
    BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from db_handling import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    firstname = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class searchForm(FlaskForm):
    garment_search = StringField('Search garment', render_kw={'style':'height:10%'}, validators=[DataRequired(), Length(max=60)])


class sForm(FlaskForm):
    gare = StringField('', filters=[lambda x: x])
    submit = SubmitField('Search')


class Inputs(FlaskForm):
    myChoices = [('price', 'price'),('date', 'date'),('gender', 'gender'),('size', 'size')]
    myField = SelectField(u'', choices=myChoices, validators=[DataRequired()])
    submit = SubmitField('Sort')


class MessageSeller(FlaskForm):
    msg = TextAreaField('', validators=[DataRequired(), Length(min=1, max=400)])
    submit = SubmitField('Send')


class ClothesForm(FlaskForm):
    #def __init__(self):
    SIZE_CHOICES = [('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')]
    GENDER_CHOICES = [('MEN', 'MEN'), ('WOMEN', 'WOMEN'), ('KIDS', 'KIDS')]
    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=30)])
    gender = SelectField('Gender', validators=[DataRequired()], choices=GENDER_CHOICES)
    size = SelectField('Size', validators=[DataRequired()], choices=SIZE_CHOICES)
    price = FloatField('Price')
    des = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=400)])
    pic = FileField(' Add a picture', validators=[DataRequired()])
    submit = SubmitField('Post')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')