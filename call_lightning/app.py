from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, LoginManager, login_required, login_user, logout_user


app = Flask(__name__)
app.secret_key = "extremely_secure"

login_manager = LoginManager()
login_manager.init_app(app)


class User():
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.username


class Launch():
    def __init__(self, target: str, reason: str, launch_time: str):
        self.target = target
        self.reason = reason
        self.launch_time = launch_time


@login_manager.user_loader
def load_user(username: str, *args) -> User:
    with open("data/users.csv", "r") as f:
        for _line in f.readlines():
            _username, _password = _line.strip().split(",")
            if username == _username:
                return User(_username, _password)
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        with open("data/users.csv", "a") as f:
            username = request.form.get("username")
            password = request.form.get("password")
            f.write(f"{username},{password}\n")
        return redirect(url_for("login"))
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        with open("data/users.csv", "r") as f:
            for _line in f.readlines():
                _username, _password = _line.strip().split(",")
                if username == _username and password == _password:
                    login_user(User(username, password))
                    break
            return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/launch", methods=["GET", "POST"])
@login_required
def launch():
    if request.method == "POST":
        with open("data/launch.csv", "a") as f:
            target = request.form.get("target")
            reason = request.form.get("reason")
            launch_time = request.form.get("launch_time")
            f.write(f"{target},{reason},{launch_time}\n")
            terminate(target, reason, launch_time)
    with open("data/launch.csv", "r") as f:
        launches = []
        for _line in f.readlines():
            target, reason, launch_time = _line.strip().split(",")
            launches.append(Launch(target, reason, launch_time))
        print(launches)
        return render_template("launch.html", launches=launches)


def terminate(target: str, reason: str, launch_time: str):
    pass
