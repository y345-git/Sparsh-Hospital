from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.doctor import (
    get_all_doctors, get_doctor_by_id, create_doctor, 
    update_doctor, delete_doctor
)
from app.utils.auth import role_required
import re

doctors_bp = Blueprint('doctors', __name__)

def validate_doctor_data(data):
    errors = []
    
    # Validate name
    if not data['name'] or len(data['name']) < 2:
        errors.append('Name must be at least 2 characters long')
    
    # Validate email
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(data['email']):
        errors.append('Please enter a valid email address')
    
    # Validate phone
    phone_pattern = re.compile(r'^\d{10}$')
    if not phone_pattern.match(data['phone']):
        errors.append('Phone number must be 10 digits')
    
    # Validate specialization
    if not data['specialization'] or len(data['specialization']) < 2:
        errors.append('Specialization must be at least 2 characters long')
    
    # Validate address
    if not data['address'] or len(data['address'].strip()) < 5:
        errors.append('Address must be at least 5 characters long')
    
    return errors

@doctors_bp.route('/doctors')
@login_required
def doctor_list():
    doctors = get_all_doctors()
    return render_template('doctors/list.html', doctors=doctors)

@doctors_bp.route('/doctors/add', methods=['GET', 'POST'])
@login_required
def add_doctor():
    if request.method == 'POST':
        doctor_data = {
            'name': request.form.get('name', '').strip(),
            'specialization': request.form.get('specialization', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'address': request.form.get('address', '').strip(),
            'status': request.form.get('status', 'active')
        }
        
        errors = validate_doctor_data(doctor_data)
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('doctors/add.html', doctor=doctor_data)
        
        try:
            create_doctor(doctor_data)
            flash('Doctor added successfully!', 'success')
            return redirect(url_for('doctors.doctor_list'))
        except Exception as e:
            flash('Error adding doctor. Please try again.', 'danger')
            return render_template('doctors/add.html', doctor=doctor_data)
    
    return render_template('doctors/add.html')

@doctors_bp.route('/doctors/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_doctor(id):
    doctor = get_doctor_by_id(id)
    if not doctor:
        flash('Doctor not found.', 'danger')
        return redirect(url_for('doctors.doctor_list'))
    
    if request.method == 'POST':
        doctor_data = {
            'name': request.form.get('name', '').strip(),
            'specialization': request.form.get('specialization', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'address': request.form.get('address', '').strip(),
            'status': request.form.get('status')
        }
        
        errors = validate_doctor_data(doctor_data)
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('doctors/edit.html', doctor=doctor_data)
        
        try:
            update_doctor(id, doctor_data)
            flash('Doctor updated successfully!', 'success')
            return redirect(url_for('doctors.doctor_list'))
        except Exception as e:
            flash('Error updating doctor. Please try again.', 'danger')
            return render_template('doctors/edit.html', doctor=doctor_data)
    
    return render_template('doctors/edit.html', doctor=doctor)

@doctors_bp.route('/doctors/delete/<int:id>')
@login_required
def delete_doctor_route(id):
    try:
        delete_doctor(id)
        flash('Doctor deleted successfully!', 'success')
    except Exception as e:
        flash('Error deleting doctor. Please try again.', 'danger')
    return redirect(url_for('doctors.doctor_list')) 