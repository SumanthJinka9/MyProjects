from flask import Flask, render_template, request, redirect, flash, url_for, abort
from is_safe_url import is_safe_url
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlite3
import bcrypt
import json
from contact import ContactForm 
from login import LoginForm
from register import RegisterForm
from user import User

app = Flask(__name__)
app.config["SECRET_KEY"] = 'supersecret'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"


salt = bcrypt.gensalt()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@login_manager.user_loader
def load_user(email_id):
    conn = get_db_connection()
    user = conn.execute(f"SELECT * FROM users WHERE email = '{email_id}'").fetchone()
    conn.close()
    if not user:
        return None
    return User(user['name'], user['email'], user['password'])

@app.route("/", methods=["POST", "GET"])
def home():
    conn = get_db_connection()
    popular_courses = conn.execute('SELECT * FROM popular_courses').fetchall()
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        appuser = conn.execute(f"SELECT * FROM users WHERE email = '{email}'").fetchone()
        if appuser is None:
            return render_template('index.html', popular_courses=popular_courses, form=form, error="Either username or password is invalid")
        else:
            if bcrypt.checkpw(password.encode('utf-8'), appuser[2]):
                login_user(User(appuser[0], appuser[1], appuser[2]), remember=remember)
                flash("You have been logged in!", "success")

                next = request.args.get('next')
                if next and not is_safe_url(next):
                    return abort(400)

                return redirect(next or url_for('home'))
            else:
                return render_template('index.html', popular_courses=popular_courses, form=form, error="Either username or password is invalid")
    return render_template("index.html", popular_courses=popular_courses, form=form)
    
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", "success")
    return redirect(url_for("home"))

@app.route("/allcourses", methods=["GET"])
def allcourses():
    conn = get_db_connection()
    courses = conn.execute("""SELECT * FROM popular_courses""").fetchall()
    conn.close()
    results = [tuple(row) for row in courses]
    return json.dumps(results);

@app.route("/courses", methods=["GET", "POST"])
@login_required
def courses():
    if request.method == "POST":
        conn = get_db_connection()
        searchtext = request.form.get("searchtext")
        if searchtext == "":
            courses = conn.execute('SELECT * FROM courses').fetchall()
            conn.close()
            return render_template('courses.html', courses=courses)
        else:
            filtered = conn.execute(f"SELECT * FROM courses where name LIKE '%{searchtext}%' or description like '%{searchtext}%'").fetchall()
            conn.close()
            return render_template('courses.html', courses=filtered, searchtext=searchtext)
        
    else:
        conn = get_db_connection()
        courses = conn.execute('SELECT * FROM courses').fetchall()
        conn.close()
        return render_template('courses.html', courses=courses)

@app.route("/aboutus", methods=["GET"])
def aboutus():
    return render_template('aboutus.html')

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        conn.execute("""INSERT INTO leads VALUES (?, ?, ?, ?)""", (name, email, subject, message))
        conn.commit()
        conn.close()
        form.name.data = ''
        form.email.data = ''
        form.subject.data = ''
        form.message.data = ''
        return render_template('contact.html', form=form, message="We have recieved your message. We will get back to you soon!")
    return render_template("contact.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        email = form.email.data
        user = conn.execute(f"SELECT * FROM users WHERE email = '{email}'").fetchone()
        if user is not None:
            return render_template('register.html', form=form, error="User already exists")
        else:
            name = form.name.data
            password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
            user = User(name, email, password)
            conn.execute("""INSERT INTO users VALUES (?, ?, ?)""", (name, email, password))
            conn.commit()
            conn.close()
            flash('Thanks for registering')
            login_user(user)
            next = request.args.get('next')
            if next and not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('home'))
    return render_template("register.html", form=form)

@app.route("/cart", methods=["GET"])
def cart():
    return render_template('cart.html')

@app.route("/messages", methods=["GET"])
def messages():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM leads').fetchall()
    conn.close()
    return render_template('messages.html', messages=messages)

if __name__ == "__main__":
    app.run(debug=True)    