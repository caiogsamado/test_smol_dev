from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Subscription

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Invalid email address.')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class SubscriptionForm(FlaskForm):
    subscription_name = StringField('Subscription Name', validators=[DataRequired()])
    subscription_price = StringField('Subscription Price', validators=[DataRequired()])
    submit = SubmitField('Create Subscription')

    def validate_subscription_name(self, subscription_name):
        subscription = Subscription.query.filter_by(name=subscription_name.data).first()
        if subscription is not None:
            raise ValidationError('Please use a different subscription name.')