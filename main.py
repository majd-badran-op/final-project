from flask import Flask
from app.interfaces.routes import register_routes
from app.interfaces.exception import register_error_handlers
from app.interfaces.routes import setup_cors

app = Flask(__name__)

setup_cors(app)
register_routes(app)
register_error_handlers(app)

if __name__ == '__main__':
    app.run(debug=True)
