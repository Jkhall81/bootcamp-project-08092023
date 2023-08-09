from datamanager.sqlite_data_manager import SQLiteDataManager
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from forms.forms import UserRegistrationForm, LoginForm

auth = Blueprint('auth', __name__)
data_manager = SQLiteDataManager('data/db.sqlite3')


@auth.route('/login', methods=['GET', 'POST'])
def login():
	user_theme = request.args.get('theme')
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		email = form.email.data
		password = form.password.data

		user = User.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password, password):
				flash('logged in successfully!')
				login_user(user, remember=True)
				return redirect(url_for('home', theme=user_theme))
			else:
				flash('Incorrect password, try again!')

		else:
			flash('Email does not exist.')

	return render_template('login.html', user=current_user, form=form, user_theme=user_theme)


@auth.route('/logout')
def logout():
	user_theme = request.args.get('theme')
	if current_user.is_authenticated:
		logout_user()
		flash('You have successfully logged out!')
	return redirect(url_for('home', theme=user_theme))


@auth.route('/add_user', methods=['GET', 'POST'])
def add_user():
	user_theme = request.args.get('theme')
	user = current_user
	form = UserRegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
			name = form.name.data
			email = form.email.data
			password = form.password.data
			bio = form.bio.data

			data_manager.add_user(name=name, email=email, password=generate_password_hash(password, method='sha256'), bio=bio)
			flash('User successfully registered!')
			new_user = User.query.filter_by(email=email).first()
			login_user(new_user)
			flash('You have been logged in successfully!')
			return redirect(url_for('home'))
	return render_template('create_user.html', form=form, user=user, user_theme=user_theme)
	