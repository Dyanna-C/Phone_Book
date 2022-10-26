from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import SignUpForm

# Create routes for our app
@app.route('/')
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