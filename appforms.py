from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, TextAreaField, FileField, \
    BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from db_handling import User

class RegistrationForm(FlaskForm):
    """
    New member application/form which has a number of fields, namely user name, firstName, lastName, email, and password
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    firstname = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7, max=20)])
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


class sForm(FlaskForm):
    """
    A search form/field in our home page that allows end-users to search clothes from our database
     """
    gare = StringField('', filters=[lambda x: x])
    submit = SubmitField('Search')

class ClothesForm(FlaskForm):
    #def __init__(self):
    SIZE_CHOICES = [('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')]
    GENDER_CHOICES = [('MEN', 'MEN'), ('WOMEN', 'WOMEN'), ('KIDS', 'KIDS')]
    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=15)])
    gender = SelectField('Gender', validators=[DataRequired()], choices=GENDER_CHOICES)
    size = SelectField('Size', validators=[DataRequired()], choices=SIZE_CHOICES)
    price = FloatField('Price')
    des = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=400)])
    pic = FileField(' Add a picture', validators=[DataRequired()])

    #pic = FileField(u'Image File', [validators.regexp(u'^[^/\\]\.jpg$')])
    #description = TextAreaField(u'Image Description')





    submit = SubmitField('Post')


class Inputs(FlaskForm):
    """
    A sort form/field in our home page that allows end-users to sort clothes based on price, date, gender or size.
    """
    myChoices = [('price', 'price'),('date', 'date'),('gender', 'gender'),('size', 'size')]
    myField = SelectField(u'', choices=myChoices, validators=[DataRequired()])
    submit = SubmitField('Sort')


class MessageSeller(FlaskForm):
    """
    A message form in our home page that allows end-users to contact seller.
    """
    msg = TextAreaField('', validators=[DataRequired(), Length(min=1, max=400)])
    submit = SubmitField('Send')


class LoginForm(FlaskForm):
    """
    A login form that allows authorized users to login to out web app and post new clothes and read buyers messages
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')