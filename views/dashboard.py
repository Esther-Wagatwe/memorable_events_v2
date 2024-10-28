"""Dashboard views module.

This module handles the dashboard view for the event planning application.
It displays upcoming events, tasks, vendor information, and guest statistics.
"""
from flask import render_template
from flask_login import login_required, current_user
from datetime import datetime

from views import app_views
from models.event import Event
from models.task import Task
from models.vendor import Vendor, event_vendors
from extensions import db

@app_views.route('/dashboard')
@login_required
def dashboard():
    """Render the main dashboard view.
    
    Displays:
    - Future events for the logged in user
    - Remaining incomplete tasks across all events
    - Vendor information and status counts
    - Guest statistics for the nearest upcoming event
    
    Returns:
        str: Rendered dashboard.html template with context data
    """
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