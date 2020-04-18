from flask import Flask
from api import api

app = Flask(__name__)

if __name__ == '__main__':
    api.init_app(app)
    app.run(debug=True)