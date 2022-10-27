from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import AddContacts
from app.models import Address


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/phonebook', methods=["GET", "POST"])
def phonebook():
    form = AddContacts()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        print(first_name, last_name, phone_number, address)
        new_address = Address(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address)
        flash(f"{first_name} {last_name} has been added as a contact in your phonebook!", "warning")
        return redirect(url_for('home'))

    return render_template('phonebook.html', form=form)

