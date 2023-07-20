from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class SubscriptionForm(FlaskForm):
    plan = StringField('Plan', validators=[DataRequired()])
    submit = SubmitField('Subscribe')

class PaymentForm(FlaskForm):
    card_number = StringField('Card Number', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired()])
    expiry_date = StringField('Expiry Date', validators=[DataRequired()])
    submit = SubmitField('Make Payment')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Profile')