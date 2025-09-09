from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        if title == "" or desc == "":
            return redirect(url_for("hello_world"))

        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("hello_world"))
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route("/abut")
def about():
    return render_template("about.html")



@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method == "POST":
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)


if __name__ == "__main__":
    app.run(debug=True)
