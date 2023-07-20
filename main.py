```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.stripe_integration import StripeIntegration

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
stripe_integration = StripeIntegration()

from app import routes, models

if __name__ == "__main__":
    app.run(debug=True)
```