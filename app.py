from flask import Flask, render_template, session, redirect, url_for
from config import Config
from routes.auth import auth
from routes.portfolio import portfolio

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(portfolio, url_prefix="/portfolio")

@app.route("/")
def home():
    if "user" in session:
        return render_template("home.html", username=session["user"])
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(port=8080,debug=True)
