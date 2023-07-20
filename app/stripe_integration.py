import stripe
from flask import current_app as app
from .models import Subscription, db

stripe.api_key = app.config['STRIPE_SECRET_KEY']

def create_subscription(user, plan):
    customer = stripe.Customer.create(
        email=user.email,
        source=request.form['stripeToken']
    )

    subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[{'plan': plan}],
    )

    new_subscription = Subscription(
        user_id=user.id,
        stripe_subscription_id=subscription.id,
        active=True
    )

    db.session.add(new_subscription)
    db.session.commit()

    return new_subscription

def update_subscription(subscription_id, new_plan):
    subscription = stripe.Subscription.retrieve(subscription_id)
    subscription.items = [{'plan': new_plan}]
    subscription.save()

    updated_subscription = Subscription.query.filter_by(stripe_subscription_id=subscription_id).first()
    updated_subscription.plan = new_plan
    db.session.commit()

    return updated_subscription

def cancel_subscription(subscription_id):
    stripe.Subscription.delete(subscription_id)

    cancelled_subscription = Subscription.query.filter_by(stripe_subscription_id=subscription_id).first()
    cancelled_subscription.active = False
    db.session.commit()

    return cancelled_subscription