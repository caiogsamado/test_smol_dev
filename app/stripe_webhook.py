```python
from flask import Blueprint, request
from app import stripe_keys
import stripe

stripe.api_key = stripe_keys.sk_test

stripe_webhook = Blueprint('stripe_webhook', __name__)

@stripe_webhook.route('/webhook', methods=['POST'])
def webhook_received():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys.endpoint_secret
        )
    except ValueError as e:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        return 'Invalid signature', 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        handle_checkout_session(session)

    return 'Success', 200

def handle_checkout_session(session):
    print("Payment was successful.")
    # Here you should define what will happen when payment is successful.
    # For example, you can create a new subscription for a user.
```