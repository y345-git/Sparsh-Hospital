from flask import Blueprint, render_template, redirect, url_for, send_from_directory, current_app
from flask_login import login_required
from app.models.patient import get_all_patients
from app.models.doctor import get_active_doctors
# from app.models.appointment import get_todays_appointments, get_upcoming_appointments
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get counts
    total_patients = len(get_all_patients())
    total_doctors = len(get_active_doctors())
    appointments_today = 0  # Will be implemented when appointments are added
    
    # Mock data for upcoming appointments
    upcoming_appointments = []
    """
    # Will be implemented when appointments are added
    upcoming_appointments = get_upcoming_appointments()
    appointments_today = len(get_todays_appointments())
    """
    
    return render_template('dashboard.html',
                         total_patients=total_patients,
                         total_doctors=total_doctors,
                         appointments_today=appointments_today,
                         upcoming_appointments=upcoming_appointments) 

@main_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static/img'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon') 