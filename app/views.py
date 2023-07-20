```python
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager, stripe_keys
from app.models import User, Subscription
from app.forms import LoginForm, RegistrationForm, SubscriptionForm, PaymentForm
import stripe

stripe.api_key = stripe_keys.secret_key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/subscribe', methods=['GET', 'POST'])
@login_required
def subscribe():
    form = SubscriptionForm()
    if form.validate_on_submit():
        subscription = Subscription(user_id=current_user.id, plan=form.plan.data)
        db.session.add(subscription)
        db.session.commit()
        flash('Subscription successful.')
        return redirect(url_for('dashboard'))
    return render_template('subscription.html', form=form)

@app.route('/payment', methods=['POST'])
@login_required
def make_payment():
    form = PaymentForm()
    if form.validate_on_submit():
        customer = stripe.Customer.create(email=current_user.email, source=form.stripeToken.data)
        charge = stripe.Charge.create(customer=customer.id, amount=2000, currency='usd', description='Flask Charge')
        flash('Payment successful.')
        return redirect(url_for('dashboard'))
    return render_template('payment.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
```