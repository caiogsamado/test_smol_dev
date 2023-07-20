# Stripe Keys
import os

stripe_keys = {
  'secret_key': os.environ.get('STRIPE_SECRET_KEY'),
  'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY')
}