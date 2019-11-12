from flask import Flask, render_template
from flask import request

from views import *

app = Flask(__name__)
# app.secret_key = b'\xe7x\xd2\xd3\x028\xb1\xf15\xb1?\xc1\x8d\xa9\xdaz'


# @app.route("/")
# def home_page():
#     return "Welcome to MedCheck Project!"


@app.route("/")
def admin_page():
    try:
        hospitals = get_hospitals()
        print("Rendering...", file=sys.stderr)
    except Exception as e:
        return e
    else:
        return render_template('admin.html', hospitals=hospitals)


@app.route("/hebe")
def hebe_page():
    return "Hebele hubele!"


if __name__ == "__main__":
    app.debug = True
    app.run()
