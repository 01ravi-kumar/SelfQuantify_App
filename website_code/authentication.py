from flask import Blueprint, render_template, request, flash , redirect, url_for
import re
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth',__name__)


@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email = request.form["login_email"]
        password = request.form["login_password"]

        user = User.query.filter(User.email==email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Logged in successfully!",category="success")
                login_user(user,remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password! Try Again", category="error")
        else:
            flash("User does not exist. Please sign up", category="error")


    return render_template("login.html",user=current_user)


@auth.route("/logout")
@login_required
def Logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign_up",methods=["GET","POST"])
def sign_up():
    if request.method=="POST":
        user_email = request.form["email"]
        user_name = request.form["name"]
        user_password1 = request.form["password1"]
        user_password2 = request.form["password2"]



        regex = '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
        if User.query.filter(User.email==user_email).first() is not None:
            flash("User Already exist. Sign up")

        elif not re.search(regex,user_email):
            flash("Invalid email. Please enter an valid email", category="error")

        elif len(user_name)<1:
            flash("Name must be atleast 1 character long.", category="error")

        elif len(user_password1)<4 or user_password1.isalpha() or user_password1.isnumeric():
            flash("Password must be 4 or more character containing alphabets and number", category="error")

        elif user_password2 != user_password1:
            flash("Password does not match",category="error")

        else:
            new_user = User(name=user_name, email=user_email,password=generate_password_hash(user_password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash("Account created Successfully", category="success")

            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)