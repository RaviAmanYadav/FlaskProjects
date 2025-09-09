from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

# ----- Configuration -----
ENV = "dev"
if ENV == "dev":
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:5688@localhost/lexus"
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://username:password@remote_host/dbname"
    )

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ----- Database Model -----
class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(
        db.String(200)
    )  # Removed unique=True to allow multiple entries
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


# ----- Routes -----
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    customer = request.form.get("customer")
    dealer = request.form.get("dealer")
    rating = request.form.get("rating")
    comments = request.form.get("comments")

    if not customer or not dealer:
        return render_template("index.html", message="Please enter required fields")

    if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
        data = Feedback(customer, dealer, rating, comments)
        db.session.add(data)
        db.session.commit()
        send_mail(customer, dealer, rating, comments)
        return render_template("success.html")
    return render_template("index.html", message="You have already submitted feedback")


# ----- Main -----
if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all()  # Ensures tables are created before server starts
            print("Tables created in database:", db.engine.url.database)
        except Exception as e:
            print(" Error creating tables:", e)

    app.run()
