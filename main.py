import flask
import base64
app = flask.Flask(__name__)


#this should prompt a user to sign in with google, or select their account mode (student or administrator)
@app.route("/")
def index():
    

@app.route("/user")
def user_dashboard():
    pass
@app.route("/admin")
def admin_dashboard():
    pass
    

if __name__ == "__main__":
    app.run(ssl_context="adhoc")