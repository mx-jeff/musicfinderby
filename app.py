from flask import Flask
from flask_cors import CORS
from server import web

app = Flask(__name__)
CORS(app)
app.register_blueprint(web)

if __name__ == "__main__":
    app.run(debug=True)