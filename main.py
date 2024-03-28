from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from forms import NewShop, LoginForm, RegisterForm, EditShop
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import smtplib, os


# SMTP VARIABLES
EMAIL = os.environ.get("Email")
APP_PW = os.environ.get("App_PW")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("app_secret_key")
bootstrap = Bootstrap5(app)


# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
     return db.get_or_404(User, user_id)


### CONNECT TO DB
db_uri = app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee.db?charset=utf8mb4'
db = SQLAlchemy()
db.init_app(app)


# User Table - Test Site with user@email.com
class User(UserMixin, db.Model):
     __tablename__ = "users"
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(100), unique=True)
     email = db.Column(db.String(100), unique=True)
     password = db.Column(db.String(100))


# Cafe Entry Table
class CoffeeShop(db.Model):
    __tablename__ = "shops"
    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(100))
    open = db.Column(db.String(10))
    close = db.Column(db.String(10))
    coffee = db.Column(db.String(10))
    wifi = db.Column(db.String(10))
    seating = db.Column(db.String(10))
    location = db.Column(db.String(100))
    postedby = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# Global variable used in add and delete routes 
DB_INDEX = None

# Log in required decorator function
def login_required(func):
    @wraps(func) # Func is the function that is passed into args. For example, the function to load a page
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or  current_user.is_authenticated == False:
            return abort(403) # Abort returns the HTTP Error specified
        return func(*args, **kwargs)
    return decorated_function


## FLASK WEB ROUTES
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/shops")
def shops():   
    list_of_shops = [["Store Name", "Open Time", "Closing Time", "Coffee Rating", "Wifi Rating", "Seating and Power Rating", "Location", "Posted By"]]
    df = pd.read_sql_table('shops', con='sqlite:///./instance/coffee.db')
    for index, row in df.iterrows():
        df_list = [row.shop_name, row.open, row.close, row.coffee, row.wifi, row.seating, row.location, row.postedby]
        list_of_shops.append(df_list)
    return render_template("shops.html", shops=list_of_shops)


@app.route("/register", methods=["GET", "POST"])
def register():
     register_form = RegisterForm()
     if request.method=="POST":
        email = request.form.get("email").lower()
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if user:
            flash("You have already signed up with that email! Please login!")
            return redirect(url_for("login"))

        plaintext_password = request.form.get("password")
        hashed_password = generate_password_hash(
            password=plaintext_password,
            method="pbkdf2:sha256",
            salt_length=8,)
        new_user = User(
            email = request.form.get("email"),
            password = hashed_password,
            name = request.form.get("name"),)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for("home"))
     
     return render_template("register.html", register_form=register_form, current_user = current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login():

     login_form = LoginForm()
     with app.app_context():
          result = db.session.execute(db.select(User)).fetchall()
     if request.method == "POST":
          email = request.form.get("email").lower()
          password = request.form.get("password")
          result = db.session.execute(db.select(User).where(User.email==email))
          user = result.scalar()
          if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))
        
          elif not check_password_hash(user.password, password):
               flash("That password is incorrect, please try again.")
               return redirect(url_for("login"))
          
          else:
               login_user(user)
               return redirect(url_for("home"))

     return render_template("login.html", login_form=login_form, current_user = current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add', methods=["GET", "POST"])
@login_required
def add():
    
    # Adds a new shop to the DB using the new shop form. Posted by is posed by the signed in user name.
    add_form = NewShop(
        posted_by = current_user.name
    )
    if add_form.validate_on_submit():
        new_location = CoffeeShop(
          shop_name = request.form.get("store_name"),
          open = request.form.get("open"),
          close = request.form.get("close"),
          coffee = request.form.get("coffee"),
          wifi = request.form.get("wifi"),
          seating = request.form.get("seating"),
          location = request.form.get("location_url"),
          postedby = request.form.get("posted_by"),)

        db.session.add(new_location)
        db.session.commit()

        return redirect(url_for("shops"))

    return render_template('add.html', add_form=add_form)


@app.route('/edit', methods=["GET", "POST"])
@login_required
def edit():
    global DB_INDEX
    shop_id = request.args.get("id")
    DB_INDEX = shop_id
    shop = db.get_or_404(CoffeeShop, shop_id)
    edit_form = EditShop(
        store_name = shop.shop_name,
        open = shop.open,
        close = shop.close,
        coffee = shop.coffee,
        wifi = shop.wifi,
        seating = shop.seating,
        location_url = shop.location,
        posted_by = shop.postedby,
        )

    if edit_form.validate_on_submit():
        shop.shop_name = edit_form.store_name.data
        shop.open = edit_form.open.data
        shop.close = edit_form.close.data
        shop.coffee = edit_form.coffee.data
        shop.wifi = edit_form.wifi.data
        shop.seating = edit_form.seating.data
        shop.location = edit_form.location_url.data
        shop.postedby = edit_form.posted_by.data
        db.session.commit()

        return redirect(url_for("shops"))

    return render_template('edit.html', edit_form=edit_form)


@app.route(f'/delete')
def delete():
    global DB_INDEX
    shop_id = int(DB_INDEX)
    shop = db.get_or_404(CoffeeShop, shop_id)
    db.session.delete(shop)
    db.session.commit()

    return redirect(url_for('shops'))


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method =="GET":
            paragraph_line = "Want to get in touch? Fill out the form below to send me a message and I will get back to you as soon as possible!"
            return render_template("contact.html", paragraph=paragraph_line)
    
    elif request.method == "POST":
         paragraph_line = "Your message has been sent!"
         name = request.form["name"]
         email = request.form["email"]
         phone_number = request.form["phone"]
         user_message = request.form["message"]

         send_message(name=name, email=email, phone=phone_number, message=user_message)
         return render_template("contact.html", paragraph=paragraph_line)


def send_message(name, email, phone, message):
    
    email_message = f"Subject:New Message from Coffee Shop Website\n\nFrom: {name}\nEmail: {email}\nPhone Number: {phone}\nMessage:{message}"
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=EMAIL, password=APP_PW)
    connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=email_message)
    connection.close()


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)