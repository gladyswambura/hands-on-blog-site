from flask import (render_template, redirect, url_for, flash, request)
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import SignUpForm, LoginForm
from .. import db


# SignUp route/Register
@auth.route("/signup", methods = ["GET", "POST"], strict_slashes=False)
def register():
    signup_form = SignUpForm()
    if signup_form.validate_on_submit():
        user = User(first_name = signup_form.first_name.data,
                    last_name = signup_form.last_name.data,  
                    username = signup_form.username.data, 
                    email = signup_form.email.data,
                    password = signup_form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash(f"Account Succesfully created", "success")
        return redirect(url_for("auth.login"))
    title = "Sign Up"
    return render_template("auth/signup.html", signup_form = signup_form, title = title)

# Login route
@auth.route("/login/", methods=["GET", "POST"], strict_slashes=False)
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data)

            return redirect(request.args.get("next") or url_for("main.index"))
        flash("Invalid Username or Password")
    
    title = "Login"
    return render_template("auth/login.html", login_form = login_form, title = title)

# Logout route
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))