from flask import Flask
from flask import request

app = Flask(__name__)
app.secret_key = b'\xe7x\xd2\xd3\x028\xb1\xf15\xb1?\xc1\x8d\xa9\xdaz'


@app.route("/")
def home_page():
    return "Welcome to MedCheck Project!"


@app.route("/hebe")
def hebe_page():
    return "Hebele hubele!"


if __name__ == "__main__":
    app.run()
