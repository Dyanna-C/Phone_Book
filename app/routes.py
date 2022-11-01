from flask import render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from app import app
from app.forms import SignUpForm, LogInForm, AddressForm
from app.models import User, Address

# Create routes for our app
@app.route('/')
def index():
    user_info = {
        'username': 'cbale',
        'email': 'christianb@movies.com'
    }
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    return render_template('index.html', user=user_info, colors=colors)

@app.route('/address')
def posts():
    return render_template('address.html')

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
        address = form.address.data
        phone_number = form.phone_number.data
        print(first_name, last_name, address, phone_number)
        # Add a new user to the database

        # Flash a success message
        flash("Success ! Thank You For Your Contribution")
        # Redirect back to home
        return redirect(url_for('index'))

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

#####

# @app.route('/update')
#@login_required
#def settings():
#    pass

#@app.route("/users/create", methods=["GET", "POST"])
#def user_create():
#    if request.method == "POST":
#        user = User(
#            username=request.form["username"],
#            email=request.form["email"],
#        )
#        db.session.add(user)
#        db.session.commit()
#        return redirect(url_for("user_detail", id=user.id))
#
#    return render_template("user/create.html")


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    form = AddressForm()
    if form.validate_on_submit():
        # Get the data from the form

        first_name = form.first_name.data
        last_name = form.last_name.data
        address = form.address.data
        phone_number = form.phone_number.data
        print(first_name, last_name, address, phone_number)

        # Create a new instance of Address with the info from the form
        new_address = AddressForm(first_name =first_name.data, last_name =last_name.data, phone_number = phone_number.data)
        # flash a message of success
        flash(f"{new_address} has been added.", "success")
        # Redirect back to the home page
        return redirect(url_for('index'))

    return render_template('create.html', form=form)

@app.route('/address/<address_id>')


def get_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        flash(f"Post with id #{address_id} does not exist", "warning")
        return redirect(url_for('index'))
    return render_template('address.html', address=address)

@app.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_address(address_id):
    address = Address.query.get(address_id)
    if not address:
        flash(f"Post with id #{address_id} does not exist", "warning")
        return redirect(url_for('index'))
    if address.author != current_user:
        flash('You do not have permission to edit this post', 'danger')
        return redirect(url_for('index'))
    form = AddressForm()
    if form.validate_on_submit():
        # Get the form data
        first_name = form.first_name.data
        last_name = form.last_name.data
        address = form.address.data
        phone_number = form.phone_number.data
        # update the post
        address.update(first_name =first_name.data, last_name =last_name.data, phone_number = phone_number.data)
        flash(f"{address.title} has been updated", "success")
        return redirect(url_for('get_post', post_id=post.id))
    return render_template('edit_post.html', post=post, form=form)

@app.route('/posts/<post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"Post with id #{post_id} does not exist", "warning")
        return redirect(url_for('index'))
    if post.author != current_user:
        flash('You do not have permission to delete this post', 'danger')
        return redirect(url_for('index'))
    post.delete()
    flash(f"{post.title} has been deleted", 'info')
    return redirect(url_for('index'))