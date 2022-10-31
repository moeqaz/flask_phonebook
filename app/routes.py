from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.forms import SignUp, LogIn, AddContacts
from app.models import User, Address


@app.route('/')
def home():
    contacts = Address.query.all()
    return render_template('index.html', contacts=contacts)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUp()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        check_user = User.query.filter( (User.username == username) | ( (User.email == email) ) ).first()
        if check_user is not None:
            flash("User with username and/or email already exists.", 'danger')
            return redirect(url_for('signup'))
        new_user = User(name=name, email=email, username=username, password=password)
        flash(f"Hello {new_user}! Your account has been created! You can now start adding contacts to your phonebook!", "warning")
        return redirect(url_for('home'))
    
    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LogIn()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user} is now logged in!", 'primary')
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password. Please try again!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(f"You have been logged out.", 'warning')
    return redirect(url_for('home'))


@app.route('/phonebook', methods=["GET", "POST"])
@login_required
def phonebook():
    form = AddContacts()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        address = form.address.data
        check_address = Address.query.filter(Address.phone_number == phone_number).first()
        if check_address is not None:
            flash("A contact in your phonebook with that phone number already exists!", 'danger')
            return redirect(url_for('phonebook'))
        new_contact = Address(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address, user_id=current_user.id)
        flash(f"{new_contact} has been added as a contact in your phonebook!", "warning")
        return redirect(url_for('home'))

    return render_template('phonebook.html', form=form)

@app.route('/contacts/<contact_id>')
def get_contact(contact_id):
    contact = Address.query.get(contact_id)
    if not contact:
        flash(f"Contact with id #{contact_id} does not exist!", "danger")
        return redirect(url_for('home'))
    return render_template('contact.html', contact=contact)

@app.route('/contacts/<contact_id>/edit', methods=["GET", "POST"])
def edit_contact(contact_id):
    contact = Address.query.get(contact_id)
    if not contact:
        flash(f"Contact with id #{contact_id} does not exist!", "danger")
        return redirect(url_for('home'))
    form = AddContacts()
    if form.validate_on_submit():
        new_phone_number = form.phone_number.data
        new_address = form.address.data
        contact.update(phone_number=new_phone_number, address=new_address)
        flash(f"Contact information for {contact.first_name} {contact.last_name} has been updated", "warning")
        return redirect(url_for('get_contact', contact_id=contact.id))
    return render_template('edit_contact.html', contact=contact, form=form)

@app.route('/contacts/<contact_id>/delete', methods=["GET", "POST"])
def delete_contact(contact_id):
    contact = Address.query.get(contact_id)
    if not contact:
        flash(f"Contact with id #{contact_id} does not exist!", "danger")
        return redirect(url_for('home'))
    contact.delete()
    flash(f"{contact.first_name} {contact.last_name} has been deleted from your phonebook.", "warning")
    return redirect(url_for('home'))