from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user_management import (
    get_all_users, get_user_by_username, create_user, 
    update_user, delete_user, get_user_by_id
)
from app.utils.auth import role_required
import re

users_bp = Blueprint('users', __name__)

def validate_user_data(data, check_password=True):
    errors = []
    
    # Validate username
    if not data['username'] or len(data['username']) < 3:
        errors.append('Username must be at least 3 characters long')
    
    # Validate full name
    if not data['full_name'] or len(data['full_name']) < 2:
        errors.append('Full name must be at least 2 characters long')
    
    # Validate email
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(data['email']):
        errors.append('Please enter a valid email address')
    
    # Validate password
    if check_password and data.get('password'):
        if len(data['password']) < 6:
            errors.append('Password must be at least 6 characters long')
    
    # Validate role
    valid_roles = ['admin', 'doctor', 'receptionist']
    if data['role'] not in valid_roles:
        errors.append('Invalid role selected')
    
    return errors

@users_bp.route('/users')
@login_required
@role_required(['admin'])
def user_list():
    users = get_all_users()
    return render_template('users/list.html', users=users)

@users_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def add_user():
    if request.method == 'POST':
        user_data = {
            'name': request.form.get('name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'password': request.form.get('password', '').strip(),
            'role': request.form.get('role', 'staff')
        }
        
        try:
            create_user(user_data)
            flash('User added successfully!', 'success')
            return redirect(url_for('users.user_list'))
        except Exception as e:
            flash('Error adding user. Please try again.', 'danger')
    
    return render_template('users/add.html')

@users_bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def edit_user(id):
    user = get_user_by_id(id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('users.user_list'))
    
    if request.method == 'POST':
        user_data = {
            'name': request.form.get('name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'role': request.form.get('role', 'staff')
        }
        
        password = request.form.get('password', '').strip()
        if password:
            user_data['password'] = password
        
        try:
            update_user(id, user_data)
            flash('User updated successfully!', 'success')
            return redirect(url_for('users.user_list'))
        except Exception as e:
            flash('Error updating user. Please try again.', 'danger')
    
    return render_template('users/edit.html', user=user)

@users_bp.route('/users/delete/<int:id>')
@login_required
@role_required(['admin'])
def delete_user_route(id):
    if id == current_user.id:
        flash('Cannot delete your own account.', 'danger')
        return redirect(url_for('users.user_list'))
    
    try:
        delete_user(id)
        flash('User deleted successfully!', 'success')
    except Exception as e:
        flash('Error deleting user. Please try again.', 'danger')
    return redirect(url_for('users.user_list')) 