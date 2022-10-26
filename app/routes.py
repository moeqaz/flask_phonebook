from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import AddContacts


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/phonebook')
def phonebook():
    form = AddContacts()
    if form.validate_on_submit():
        print('this form worked!')
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        print(first_name, last_name, phone_number, address)
        flash('You have successfully added your contact!')
        return redirect(url_for('home'))

    return render_template('phonebook.html', form=form)

