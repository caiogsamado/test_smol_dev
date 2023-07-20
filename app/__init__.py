```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from app.stripe_integration import StripeIntegration

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize Stripe Integration
stripe_integration = StripeIntegration(app)

from app import routes, models
```