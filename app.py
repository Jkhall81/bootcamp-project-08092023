from auth import auth
from api_routes import api_bp
from crud_routes import crud_bp
from flask import Flask, flash, render_template, request, redirect, session, url_for
from flask_login import current_user, LoginManager
from flask_migrate import Migrate
from forms.forms import csrf
from models import User, Movie, db
import config

app = Flask(__name__)
app.config.from_object(config)
migrate = Migrate(app, db)
db.init_app(app)
csrf.init_app(app)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(crud_bp, url_prefix='/crud')
app.register_blueprint(api_bp, url_prefix='/api')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.route('/', methods=['POST', 'GET'])
def home():
	user_theme = request.args.get('theme')
	user = current_user
	return render_template('home.html', user=user, user_theme=user_theme)


if __name__ == '__main__':
	#with app.app_context():
	#	db.create_all()
	#	print(' * database up and running!')
	app.run(debug=True, host='0.0.0.0', port=5000)
