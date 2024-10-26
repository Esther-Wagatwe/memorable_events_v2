from flask import render_template, redirect, url_for, flash, jsonify, request
from models.user import User, check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models.event import Event, EventStatus
from models import db
from models.vendor import Vendor
from flask import Blueprint
from datetime import datetime


app_views = Blueprint('app_views', __name__)

@app_views.route('/login', methods=['GET', 'POST'])
def login():
    """Route for the login page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Login attempt for email: {email}")  # Debug print

        #check if email and password are provided
        if not email or not password:
            flash('Email and password are required', 'error')
            return redirect(url_for('app_views.login'))

        user = User.query.filter_by(email=email).first()

        #check if user exists and password is correct   
        if user and user.password_hash and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('app_views.dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('app_views.login'))
    
    return render_template('login.html')

@app_views.route('/signup', methods=['GET', 'POST'])
def signup():
    """Route for the signup page"""

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if all required fields are provided
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return redirect(url_for('app_views.signup'))

        # Check if the user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            if existing_user.username == username:
                flash('Username already exists', 'error')
            else:
                flash('Email address already exists', 'error')
            return redirect(url_for('app_views.signup'))
        
        # Create a new user
        try:
            new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Account created successfully!', 'success')
            return redirect(url_for('app_views.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'error')
            return redirect(url_for('app_views.signup'))
    
    # GET request: render the signup form
    return render_template('signup.html')


@app_views.route('/')
def landingpage():
    """Route for the landing page"""
    return render_template('landingpage.html')

@app_views.route('/events')
@login_required
def events():
    """Route for events page"""
    user_id = current_user.user_id
    events = Event.query.filter_by(owner_id=user_id).all()
    serialized_events = [event.serialize() for event in events]
    return render_template('events.html', events=serialized_events)

@app_views.route('/event/<event_id>', methods=['GET', 'POST', 'PUT'])
@login_required
def event_details(event_id):
    if event_id == 'new':
        event = Event(owner_id=current_user.user_id)
    else:
        event = Event.query.get_or_404(int(event_id))
        if event.owner_id != current_user.user_id:
            flash('You do not have permission to view this event', 'error')
            return redirect(url_for('app_views.events'))

    if request.method == 'POST':
        # Handle creating a new event
        event.name = request.form['name']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        event.location = request.form['location']
        event.description = request.form['description']
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully', 'success')
        return redirect(url_for('app_views.event_details', event_id=event.event_id))

    elif request.method == 'PUT':
        # Handle updating an existing event
        event.name = request.form['name']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        event.location = request.form['location']
        event.description = request.form['description']
        db.session.commit()
        flash('Event updated successfully', 'success')
        return redirect(url_for('app_views.event_details', event_id=event.event_id))

    context = {
        'event': event,
        'expenses': event.expenses if event_id != 'new' else {},
        'spent_budget': event.spent_budget if event_id != 'new' else 0
    }
    return render_template('event_details.html', **context)

@app_views.route('/vendors')
def vendors():
    """Route for vendors page"""
    #get vendors data and store in a dictionary
    context = {}
    vendors = Vendor.query.all()
    context['vendors'] = vendors
    return render_template('vendors.html', **context)

@app_views.route('/dashboard')
@login_required
def dashboard():
    """Route for the dashboard page"""
    context = {}
    #get vendor data
    vendors = Vendor.query.all()
    context['vendors'] = vendors
    return render_template('dashboard.html', **context)

@app_views.route('/events/<int:event_id>/add_expense', methods=['POST'])
@login_required
def add_expense(event_id):
    """Route to add an expense to an event"""
    event = Event.query.get_or_404(event_id)
    
    # Check if the current user is the owner of the event
    if event.owner_id != current_user.user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    description = data.get('description')
    amount = data.get('amount')

    if not description or not amount:
        return jsonify({'error': 'Description and amount are required'}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({'error': 'Amount must be a number'}), 400

    event.add_expense(description, amount)

    return jsonify({
        'description': description,
        'amount': amount,
        'total_spent': event.spent_budget,
        'expenses': event.expenses
    }), 201

@app_views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('app_views.index'))

@app_views.route('/about')
def about():
    return render_template('about.html')

@app_views.route('/contact')
def contact():
    return "Contact"
    # return render_template('contact.html')

@app_views.route('/profile')
@login_required
def profile():
    return "profile"
    # return render_template('privacy.html')

@app_views.route('/settings')
@login_required
def settings():
    return "settings"

@app_views.route('/api/event_statuses')
@login_required
def get_event_statuses():
    return jsonify([status.value for status in EventStatus])
