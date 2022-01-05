from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import LoginForm ,PostForm,NamerForm,PasswordForm,UserForm, PostForm
from flask_ckeditor import CKEditor
#create a form class


#Create a flask instance


app = Flask(__name__)
app.config['SECRET_KEY'] = "NikolaRokvic"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:test@localhost/users'

ckeditor = CKEditor(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))


@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
	return render_template('dashboard.html')


@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("Login Successfull")
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong Password!")
		else:
			flash("User Not Found")

	return render_template('login.html', form=form)


@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
	logout_user()
	flash("You have been logged out successfully")
	return redirect(url_for('login'))


@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
	post = Posts.query.get_or_404(id)
	
	if current_user.id == post.author.id:
		try:

			db.session.delete(post)
			db.session.commit()
			flash("Post deleted successfully")

		except:

			flash("There was a problem deleting the post, please try again")


		posts = Posts.query.order_by(Posts.date_posted)
		return render_template("posts.html", posts=posts)
	else:
		flash("You cannot delete this post")

		posts = Posts.query.order_by(Posts.date_posted)
		return render_template("posts.html", posts=posts)


@app.route('/posts/edit/<int:id>)', methods=['GET','POST'])
@login_required
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.slug = form.slug.data
		post.content = form.content.data

		db.session.add(post)
		db.session.commit()
		flash("Post updated successfully")
		return redirect(url_for('post', id=post.id))

	if current_user.id == post.author_id:
		form.title.data = post.title
		form.slug.data = post.slug
		form.content.data = post.content
		return render_template('edit_post.html', form=form)
	else:
		flash("You are not authorised to edit that post")
		posts = Posts.query.order_by(Posts.date_posted)
		return render_template("posts.html", posts=posts)


@app.route('/posts/<int:id>')
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template("post.html", post=post)


@app.route('/posts')
def posts():
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template("posts.html", posts=posts)


@app.route('/add-post', methods=['GET','POST'])
@login_required
def add_post():
	form = PostForm()

	if form.validate_on_submit():
		post = Posts(title=form.title.data , content = form.content.data, author=current_user,slug=form.slug.data)

		form.title.data=''
		form.content.data=''
		form.slug.data=''

		db.session.add(post)
		db.session.commit()

		flash("Post added successfully")

	return render_template('add_post.html', form=form)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
	user_to_delete = Users.query.get_or_404(id)
	form = UserForm()
	name=None

	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("User Dleted Successfully")
		return render_template("add_user.html", user_to_delete=user_to_delete, name=name, form=form)

	except:
		flash("Error occured while deleting user, please try again")
		return render_template("add_user.html", user_to_delete=user_to_delete, name=name, form=form)


@app.route('/update/<int:id>', methods=['GET','POST'])
@login_required
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.username = request.form['username']
		name_to_update.about_author = request.form['about_author']
		try:
			db.session.commit()
			flash("User Updated Successfully")
			return render_template("update.html", form=form, name_to_update=name_to_update)
		except:
			flash("Error occured while updating user, please try again")
			return render_template("update.html", form=form, name_to_update=name_to_update)
			
	else:
		return render_template("update.html", form=form, name_to_update=name_to_update, id=id)



@app.route('/')

def index():
	return redirect(url_for('posts'))

@app.route('/user/<name>')

def user(name):
	return render_template("user.html", name=name)


@app.errorhandler(404)

def page_not_found(e):
	return render_template("404.html"), 404


@app.errorhandler(500)

def page_not_found(e):
	return render_template("500.html"), 500


@app.route('/user/add', methods=['GET','POST'])

def add_user():
	name = None
	form = UserForm()

	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			hashed_pw = generate_password_hash(form.password_hash.data)
			user = Users(username=form.username.data,name=form.name.data, email= form.email.data, password_hash=hashed_pw)
			db.session.add(user)
			db.session.commit()
		
		name = form.name.data
		form.name.data = ''
		form.email.data = ''
		form.username.data = ''
		form.password_hash.data = ''
		flash("User added successfully")

	our_users = Users.query.order_by(Users.date_added)

	return render_template("add_user.html", form=form, name=name, our_users=our_users)





class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default= datetime.now)
	about_author = db.Column(db.Text(500), nullable=True)
	posts = db.relationship('Posts', backref='author')

	#password hashing

	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError('Nope!')

	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)


	def verify_password(self,password):
		return check_password_hash(self.password_hash, password)


	def __repr__(self):
		return '<Name %r>' %self.name



class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	#author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.now)
	slug = db.Column(db.String(255))
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))