from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    get_flashed_messages,
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///login.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "supersecretkey123"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


@app.route("/", methods=["GET"])
def home():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    get_flashed_messages()

    user = User.query.filter_by(email=email, password=password).first()

    if user:
        session["user_id"] = user.id
        flash("LOGIN SUCCESSFULLY", "success")
        return redirect(url_for("dashboard"))
    else:
        flash("Invalid User ID or Password", "danger")
        return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please Login", "warning")
        return redirect(url_for("home"))
    return render_template("dashboard.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("PASSWORD DON'T MATCH! Please Retype", "danger")
            return redirect(url_for("register"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists", "danger")
            return redirect(url_for("register"))

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
