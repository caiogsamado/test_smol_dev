```python
from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, SubscriptionForm
from app.models import User, Subscription
from app.stripe_integration import create_subscription, update_subscription
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'login_error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'register_success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/subscription', methods=['GET', 'POST'])
@login_required
def subscription():
    form = SubscriptionForm()
    if form.validate_on_submit():
        subscription = Subscription(user_id=current_user.id, plan=form.plan.data)
        db.session.add(subscription)
        db.session.commit()
        create_subscription(subscription)
        flash('Subscription created successfully!', 'subscription_success')
        return redirect(url_for('index'))
    return render_template('subscription.html', title='Subscription', form=form)

@app.route('/update_subscription', methods=['GET', 'POST'])
@login_required
def update_subscription_route():
    form = SubscriptionForm()
    if form.validate_on_submit():
        subscription = Subscription.query.filter_by(user_id=current_user.id).first()
        subscription.plan = form.plan.data
        db.session.commit()
        update_subscription(subscription)
        flash('Subscription updated successfully!', 'subscription_success')
        return redirect(url_for('index'))
    return render_template('subscription.html', title='Update Subscription', form=form)
```