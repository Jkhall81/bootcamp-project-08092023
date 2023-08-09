from datamanager.sqlite_data_manager import SQLiteDataManager
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from forms.forms import AddMovieForm, EditUserForm, MovieCommentForm, EditCommentForm
from models import Comment, User, Movie, db

crud_bp = Blueprint('crud', __name__)
data_manager = SQLiteDataManager('data/db.sqlite3')


# List users

@crud_bp.route('/users')
def list_users():
	user_theme = request.args.get('theme')
	user = current_user
	users = data_manager.get_all_users()
	return render_template('users.html', users=users, user=user, user_theme=user_theme)

# List User's movies

@crud_bp.route('/users/<int:user_id>')
def list_user_movies(user_id):
	user_theme = request.args.get('theme')
	logged_in_user = current_user
	user = data_manager.get_user(user_id)
	movies = data_manager.get_user_movies(user_id)

	return render_template('user_movies.html', user=user,  movies=movies, user_id=user_id, logged_in_user=current_user, user_theme=user_theme)


# Add Movie

@crud_bp.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
	user_theme = request.args.get('theme')
	form = AddMovieForm(request.form)
	user = data_manager.get_user(user_id)

	if request.method == 'POST' and form.validate():
		try:
				moviename = form.moviename.data
				data_manager.add_movie(user_id, moviename)
				flash('Movie successfully added!')
				return redirect(url_for('crud.list_user_movies', user_id=user_id, theme=user_theme))

		except Exception as e:
				flash(f'An error occurred while adding the movie: {str(e)}')

	return render_template('add_movie.html', user_id=user_id, user=user, form=form, user_theme=user_theme)



@crud_bp.route('/users/<int:user_id>/update_movie/<int:movie_id>')
def update_movie():
	"""
	All my movie data is coming from an API, why would I let users mess it up?
	"""
	pass


# Delete Movie

@crud_bp.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['GET'])
def delete_movie(user_id, movie_id):
	user_theme = request.args.get('theme')
	data_manager.delete_movie(user_id, movie_id)
	flash('Movie successfully deleted!')
	return redirect(url_for('crud.list_user_movies', user_id=user_id, user_theme=user_theme))


# Delete User

@crud_bp.route('/users/<int:user_id>/delete', methods=['GET'])
def delete_user(user_id):

	data_manager.delete_user(user_id)
	return redirect(url_for('list_users'))


# Edit User
@crud_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
	user_theme = request.args.get('theme')
	form = EditUserForm(request.form)
	if request.method == 'POST' and form.validate():
			user = data_manager.get_user(user_id)
			if user:
				name = form.name.data
				email = form.email.data
				bio = form.bio.data

				User.query.filter_by(id=user_id).update({
					User.name: name,
					User.email: email,
					User.bio: bio
				})
				db.session.commit()
				flash('Info updated successfully!')
				
			return redirect(url_for('crud.list_users', theme=user_theme))

	user = data_manager.get_user(user_id)
	return render_template('edit_user.html', user=user, form=form, user_theme=user_theme)

# Shows movie details after clicking movie image link
@crud_bp.route('/movie_details/<int:movie_id>', methods=['GET', 'POST'])
def movie_details(movie_id):
	user_theme = request.args.get('theme')
	user = current_user
	movie = Movie.query.get_or_404(movie_id)
	comments = Comment.query.filter(Comment.movie_id == movie_id).all()
	form = MovieCommentForm(request.form)
	
	if request.method == 'POST' and form.validate():
		email = form.email.data
		subject = form.subject.data
		comment_text = form.comment_text.data

		new_comment = Comment(email=email, subject=subject, comment_text=comment_text, user_id=user.id, movie_id=movie_id)

		db.session.add(new_comment)
		db.session.commit()
		flash('Comment added successfully!')
		return redirect(url_for('crud.movie_details', movie_id=movie_id))
	return render_template('movie_details.html', user=user, movie=movie, form=form, comments=comments, user_theme=user_theme)

# edit a review after clicking link with tooltip
@crud_bp.route('/edit_comment/<int:comment_id>', methods=['GET', 'POST'])
def edit_comment(comment_id):
	form = EditCommentForm(request.form)
	user = current_user
	comment = Comment.query.get(comment_id)
	movie_id = comment.movie_id

	if request.method == 'POST' and form.validate():
		email = form.email.data
		subject = form.subject.data
		comment_text = form.comment_text.data

		comment.email = email
		comment.subject = subject
		comment.comment_text = comment_text

		db.session.commit()
		flash('Changes made successfully!')
		return redirect(url_for('crud.movie_details', movie_id=movie_id))

	return render_template('edit_comment.html', user=user, form=form, comment=comment, movie_id=movie_id)


@crud_bp.route('/delete/<int:comment_id>/<int:movie_id>', methods=['GET', 'POST'])
def delete_comment(comment_id, movie_id):
	comment = Comment.query.get(comment_id)
	if comment:
		db.session.delete(comment)
		db.session.commit()
		flash('Comment deleted successfully!')
		return redirect(url_for('crud.movie_details', movie_id=movie_id))

	else:
		flash('Comment not found!')
		return redirect(url_for('home'))
