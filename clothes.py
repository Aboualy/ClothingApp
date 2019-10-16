from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length


class ClothesForm(FlaskForm):
    #def __init__(self):
    SIZE_CHOICES = [('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')]
    GENDER_CHOICES = [('MEN', 'MEN'), ('WOMEN', 'WOMEN'), ('KIDS', 'KIDS')]
    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=30)])
    gender = SelectField('Gender', validators=[DataRequired()], choices=GENDER_CHOICES)
    size = SelectField('Size', validators=[DataRequired()], choices=SIZE_CHOICES)
    price = FloatField('Price')
    des = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=100)])
    pic = FileField(' Add a picture', validators=[DataRequired()])
    submit = SubmitField('Post')