from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from app import app
from app.forms import SignUpForm, LogInForm
from app.models import User

# Create routes for our app
@app.route('/')
def index():
    user_info = {
        'username': 'cbale',
        'email': 'christianb@movies.com'
    }
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    return render_template('index.html', user=user_info, colors=colors)

@app.route('/posts')
def posts():
    return render_template('posts.html')

def home():
    return render_template('home.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Thank You For Adding To Our Phonebook!')
        # Get data from form (first name, last name, street address, phone number )
        first_name = form.first_name.data
        last_name = form.last_name.data
        street_address = form.street_address.data
        phone_number = form.phone_number.data
        print(first_name, last_name, street_address, phone_number)
        # Add a new user to the database

        # Flash a success message
        flash("Success ! Thank You For Your Contribution")
        # Redirect back to home
        return redirect(url_for('home'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        # Get the form data
        username = form.username.data
        password = form.password.data
        # Check to see if there is a user with that username and password
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            # log the user in
            login_user(user)
            flash(f"{user} is now logged in.", 'primary')
            return redirect(url_for('index'))
        else:
            flash('Incorrect username and/or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))
    