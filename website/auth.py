from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from. import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else: flash('Email not found in database.', category='error')


    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('userName')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif len(username) < 3:
            flash("Username must be greater than 2 characters.", category='error')
            # Alert user
            pass
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category='error')
            # Aler user
            pass
        elif len(password) < 7:
            flash("Password must be at least 7 characters.", category='error')
            # Alert user
            pass
        elif user is None:
            new_user = User(email=email, password=generate_password_hash(password, method='sha256'), user_name=username)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.explore'))
        else:
            pass



    return render_template("sign_up.html", user=current_user)