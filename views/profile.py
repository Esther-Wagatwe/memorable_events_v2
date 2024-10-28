"""Profile and account management views.

This module handles user profile, settings, landing page and about page routes.
It manages authentication redirects and template rendering for these core pages.
"""
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from views import app_views


@app_views.route('/')
def landingpage():
    """Handle the main landing page route.
    
    If user is already authenticated, redirects to their dashboard.
    Otherwise displays the landing page.

    Returns:
        Response: Redirects to dashboard for authenticated users,
                 otherwise renders landing page template
    """
    if current_user.is_authenticated:
        return redirect(url_for('app_views.dashboard'))
    return render_template('landingpage.html')


@app_views.route('/about') 
def about():
    """Handle the about page route.
    
    Displays general information about the application.

    Returns:
        Response: Rendered about page template
    """
    return render_template('about.html')


@app_views.route('/profile')
@login_required
def profile():
    """Handle the user profile page route.
    
    Requires authentication. Displays user profile information
    and account details.

    Returns:
        Response: Rendered profile page template
    """
    return render_template('profile.html')


@app_views.route('/settings')
@login_required 
def settings():
    """Handle the user settings page route.
    
    Requires authentication. Allows users to modify their
    account preferences and settings.

    Returns:
        Response: Rendered settings page template
    """
    return render_template('settings.html')
