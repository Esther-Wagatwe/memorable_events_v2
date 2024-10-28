import json
from flask import render_template, redirect, url_for, flash, jsonify, request
from models.user import User, check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models.event import Event, EventStatus
from models import db
from models.vendor import Vendor, event_vendors
from flask import Blueprint
from datetime import datetime
from models.task import Task
from models.guest import Guest
from sqlalchemy import func


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

@app_views.route('/event/<event_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def event_details(event_id):
    try:
        if event_id == 'new':
            event = Event(owner_id=current_user.user_id)
        else:
            event = Event.query.get_or_404(int(event_id))
            if event.owner_id != current_user.user_id:
                return jsonify({'success': False, 'error': 'You do not have permission to view this event'}), 403

        if request.method == 'POST':
            # Handle creating a new event
            event.name = request.form['name']
            event.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            event.location = request.form['location']
            event.description = request.form['description']
            event.status = EventStatus.ACTIVE
            event.spent_budget = 0.0
            event.expenses = {}
            db.session.add(event)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Event created successfully'})

        elif request.method == 'PUT':
            # Handle updating an existing event
            event.name = request.form['name']
            event.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            event.location = request.form['location']
            event.description = request.form['description']
            event.status = EventStatus(request.form['status'])
            if 'spent_budget' in request.form:
                event.spent_budget = float(request.form['spent_budget'])
            if 'expenses' in request.form:
                event.expenses = json.loads(request.form['expenses'])
            db.session.commit()
            return jsonify({'success': True, 'message': 'Event updated successfully'})

        elif request.method == 'DELETE':
            # Verify event ownership
            if event.owner_id != current_user.user_id:
                return jsonify({'success': False, 'error': 'Unauthorized'}), 403
                
            # Delete the event
            db.session.delete(event)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Event deleted successfully'})

        return render_template('event_details.html', event=event, EventStatus=EventStatus)

    except ValueError as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'An error occurred: {str(e)}'}), 500

@app_views.route('/vendors', methods=['GET', 'POST'])
@login_required
def vendors():
    """Route for vendors page and vendor operations"""
    if request.method == 'GET':
        # Handle adding vendor to event
        action = request.args.get('action')
        if action == 'add':
            vendor_id = request.args.get('vendor_id')
            event_id = request.args.get('event_id')
            
            try:
                event = Event.query.get_or_404(event_id)
                vendor = Vendor.query.get_or_404(vendor_id)
                
                # Verify event ownership
                if event.owner_id != current_user.user_id:
                    flash('Unauthorized access', 'error')
                    return redirect(url_for('app_views.vendors'))

                # Check if vendor is already in event
                if vendor in event.vendors:
                    flash(f'"{vendor.name}" is already added to this event', 'error')
                else:
                    event.vendors.append(vendor)
                    db.session.commit()
                    flash(f'"{vendor.name}" added to event successfully', 'success')
                
                # Redirect back to vendors page with event_id
                return redirect(url_for('app_views.vendors', event_id=event_id))
            
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding vendor: {str(e)}', 'error')
                return redirect(url_for('app_views.vendors', event_id=event_id))

        # Regular vendors page display
        context = {
            'vendors': Vendor.query.all(),
            'event_id': request.args.get('event_id')
        }
        
        # If we're selecting vendors for an event, get the event's current vendors
        if context['event_id']:
            event = Event.query.get(context['event_id'])
            if event:
                context['event_vendors'] = event.vendors
            
        return render_template('vendors.html', **context)
        
    elif request.method == 'POST':
        try:
            data = request.json
            event_id = data.get('event_id')
            vendor_id = data.get('vendor_id')
            
            # Get event and vendor
            event = Event.query.get_or_404(event_id)
            vendor = Vendor.query.get_or_404(vendor_id)
            
            # Verify event ownership
            if event.owner_id != current_user.user_id:
                return jsonify({'error': 'Unauthorized'}), 403

            # Check if vendor is already in event
            if vendor in event.vendors:
                return jsonify({'error': 'Vendor already added to this event'}), 400
            
            # Add vendor to event
            event.vendors.append(vendor)
            db.session.commit()
            
            return jsonify({
                'message': 'Vendor added to event successfully',
                'vendor': vendor.serialize()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'PUT':
        try:
            data = request.json
            vendor_id = data.get('vendor_id')
            vendor = Vendor.query.get_or_404(vendor_id)
            
            # Verify vendor belongs to user's event
            if not any(event.owner_id == current_user.user_id for event in vendor.events):
                return jsonify({'error': 'Unauthorized'}), 403

            # Update vendor details
            if 'name' in data:
                vendor.name = data['name']
            if 'category' in data:
                vendor.category = data['category']
            if 'description' in data:
                vendor.description = data['description']
            if 'image_path' in data:
                vendor.image_path = data['image_path']
            if 'phone_number' in data:
                vendor.phone_number = data['phone_number']
            if 'email' in data:
                vendor.email = data['email']
            if 'service_fee' in data:
                vendor.service_fee = data['service_fee']
            if 'rating' in data:
                vendor.rating = data['rating']
            if 'status' in data:
                vendor.status = data['status']
            
            db.session.commit()
            
            return jsonify({
                'message': 'Vendor updated successfully',
                'vendor': vendor.serialize()
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'DELETE':
        try:
            data = request.json
            event_id = data.get('event_id')
            vendor_id = data.get('vendor_id')
            
            # Get event and vendor
            event = Event.query.get_or_404(event_id)
            vendor = Vendor.query.get_or_404(vendor_id)
            
            # Verify event ownership
            if event.owner_id != current_user.user_id:
                return jsonify({'error': 'Unauthorized'}), 403

            # Remove vendor from event
            if vendor in event.vendors:
                event.vendors.remove(vendor)
                db.session.commit()
                return jsonify({'message': 'Vendor removed from event successfully'})
            else:
                return jsonify({'error': 'Vendor not found in event'}), 404
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

@app_views.route('/dashboard')
@login_required
def dashboard():
    # Get all future events
    future_events = Event.query.filter(
        Event.owner_id == current_user.user_id,
        Event.date >= datetime.now().date()
    ).order_by(Event.date).all()

    # Get tasks grouped by event
    remaining_tasks = Task.query.join(Event).filter(
        Event.owner_id == current_user.user_id,
        Task.status != 'completed'
    ).order_by(Event.date, Task.task_id).all()

    # Get vendors with their associated events using explicit joins
    vendors_with_events = db.session.query(Vendor)\
        .select_from(Event)\
        .join(event_vendors)\
        .join(Vendor)\
        .filter(Event.owner_id == current_user.user_id)\
        .add_columns(Event.event_id)\
        .all()

    # Process vendors
    vendors = []
    for vendor, event_id in vendors_with_events:
        vendor.event_id = event_id
        vendors.append(vendor)
    
    # Count vendor statuses
    confirmed_vendors = sum(1 for v in vendors if v.status == 'confirmed')
    pending_vendors = sum(1 for v in vendors if v.status == 'pending')

    # Calculate guest statistics for the nearest future event (if any)
    if future_events:
        nearest_event = future_events[0]
        confirmed_guests = nearest_event.confirmed_guests
        pending_guests = nearest_event.pending_guests
    else:
        confirmed_guests = 0
        pending_guests = 0

    return render_template('dashboard.html',
                         future_events=future_events,
                         remaining_tasks=remaining_tasks,
                         vendors=vendors,
                         confirmed_vendors=confirmed_vendors,
                         pending_vendors=pending_vendors,
                         confirmed_guests=confirmed_guests,
                         pending_guests=pending_guests)

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

# Status update route (accessible from both dashboard and event details)
@app_views.route('/event/<int:event_id>/update_vendor_status/<int:vendor_id>', methods=['POST'])
@login_required
def update_vendor_status(event_id, vendor_id):
    try:
        event = Event.query.get_or_404(event_id)
        
        # Check if the current user is the event owner
        if event.owner_id != current_user.user_id:
            flash('You do not have permission to update vendor status for this event.', 'error')
            return redirect(url_for('app_views.event_details', event_id=event_id))

        new_status = request.form.get('status')
        if event.update_vendor_status(vendor_id, new_status):
            flash('Vendor status updated successfully', 'success')
        else:
            flash('Failed to update vendor status', 'error')

        # Redirect back to the appropriate page
        referrer = request.referrer
        if referrer and 'dashboard' in referrer:
            return redirect(url_for('app_views.dashboard'))
        return redirect(url_for('app_views.event_details', event_id=event_id))

    except Exception as e:
        flash('Error updating vendor status', 'error')
        return redirect(url_for('app_views.dashboard'))

@app_views.route('/event/<int:event_id>/remove_vendor/<int:vendor_id>', methods=['GET', 'DELETE'])
@login_required
def remove_vendor(event_id, vendor_id):
    """Remove a vendor from an event"""
    try:
        event = Event.query.get_or_404(event_id)
        vendor = Vendor.query.get_or_404(vendor_id)
        
        # Verify event ownership
        if event.owner_id != current_user.user_id:
            if request.method == 'DELETE':
                return jsonify({'error': 'Unauthorized access'}), 403
            flash('Unauthorized access', 'error')
            return redirect(url_for('app_views.event_details', event_id=event_id))

        # Check if vendor is in event
        if vendor not in event.vendors:
            if request.method == 'DELETE':
                return jsonify({'error': 'Vendor not in event'}), 400
            flash('Vendor is not associated with this event', 'error')
            return redirect(url_for('app_views.event_details', event_id=event_id))

        try:
            # Remove the association from the event_vendors table
            stmt = event_vendors.delete().where(
                db.and_(
                    event_vendors.c.event_id == event_id,
                    event_vendors.c.vendor_id == vendor_id
                )
            )
            db.session.execute(stmt)
            db.session.commit()
            
            if request.method == 'DELETE':
                return jsonify({'message': 'Vendor removed successfully'}), 200
                
            flash(f'"{vendor.name}" has been removed from the event', 'success')
            return redirect(url_for('app_views.event_details', event_id=event_id))
            
        except Exception as e:
            db.session.rollback()
            raise e
        
    except Exception as e:
        db.session.rollback()
        if request.method == 'DELETE':
            return jsonify({'error': str(e)}), 500
        flash(f'Error removing vendor: {str(e)}', 'error')
        return redirect(url_for('app_views.event_details', event_id=event_id))

@app_views.route('/event/<int:event_id>/tasks', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def tasks(event_id):
    """Handle all CRUD operations for tasks"""
    try:
        event = Event.query.get_or_404(event_id)
        if event.owner_id != current_user.user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        if request.method == 'POST':
            # Create new task
            data = request.json
            new_task = Task(
                event_id=event_id,
                description=data['name'],
                due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date(),
                status='pending'
            )
            
            db.session.add(new_task)
            db.session.commit()
            
            flash('Task created successfully!', 'success')
            return jsonify({
                'success': True,
                'message': 'Task created successfully',
                'task': new_task.serialize()
            })

        elif request.method == 'PUT':
            # Update existing task
            data = request.json
            task_id = data.get('task_id')
            if not task_id:
                return jsonify({'error': 'Task ID is required'}), 400

            task = Task.query.get_or_404(task_id)
            if task.event_id != event_id:
                return jsonify({'error': 'Task not found in this event'}), 404

            if 'name' in data:
                task.description = data['name']
            if 'description' in data:
                task.description = data['description']
            if 'due_date' in data:
                task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
            if 'status' in data:
                old_status = task.status
                task.status = data['status']
                status_message = f'Task marked as {data["status"]}'
                flash(status_message, 'success')

            db.session.commit()
            return jsonify({
                'success': True,
                'message': status_message if 'status' in data else 'Task updated successfully',
                'task': task.serialize()
            })
        
        elif request.method == 'DELETE':
            # Delete task
            data = request.json
            task_id = data.get('task_id')
            if not task_id:
                return jsonify({'error': 'Task ID is required'}), 400

            task = Task.query.get_or_404(task_id)
            if task.event_id != event_id:
                return jsonify({'error': 'Task not found in this event'}), 404

            db.session.delete(task)
            db.session.commit()
            flash('Task deleted successfully', 'success')
            return jsonify({
                'success': True,
                'message': 'Task deleted successfully'
            })

        elif request.method == 'GET':
            # Return all tasks for the event
            tasks = Task.query.filter_by(event_id=event_id).all()
            return jsonify({
                'success': True,
                'tasks': [task.serialize() for task in tasks]
            })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500