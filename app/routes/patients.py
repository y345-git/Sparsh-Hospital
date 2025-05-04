from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required
from app.models.patient import (
    get_all_patients, get_patient_by_id, create_patient, 
    update_patient, delete_patient
)
from app.utils.auth import role_required
from datetime import date
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from app.models.doctor import get_active_doctors, get_doctors_for_dropdown
from app.utils.pdf_generator import create_patient_pdf, create_followup_pdf
from app.models.followup import (
    create_followup, 
    get_patient_followups, 
    get_followup_by_id,
    delete_followup_record
)
import json
from app.models.medicine import get_all_medicines, save_prescription

patients_bp = Blueprint('patients', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_bool(value):
    if value is None or value == '':
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        if value.lower() in ('true', 't', 'yes', 'y', 'on', '1'):
            return True
        if value.lower() in ('false', 'f', 'no', 'n', 'off', '0'):
            return False
    if isinstance(value, int):
        return bool(value)
    return False

def convert_checkbox_value(value):
    """Convert checkbox value to boolean"""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', 't', 'yes', 'y', 'on', '1')
    if isinstance(value, int):
        return bool(value)
    return False

@patients_bp.route('/patients')
@login_required
def patient_list():
    patients = get_all_patients()
    return render_template('patients/list.html', patients=patients)

@patients_bp.route('/patients/add', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'doctor', 'staff'])
def add_patient():
    if request.method == 'POST':
        # Handle file uploads
        uploaded_files = []
        if 'report_files' in request.files:
            files = request.files.getlist('report_files')
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    # Create unique filename
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    unique_filename = f"{timestamp}_{filename}"
                    
                    # Ensure upload directory exists
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    
                    # Save file
                    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                    file.save(file_path)
                    uploaded_files.append(unique_filename)

        # Debug information
        # print("Form data:", request.form)
        
        # Debug print to check what's coming from the form
        # print("Form data for medical conditions:", {
        #     'has_thyroid': request.form.get('has_thyroid'),
        #     'has_diabetes': request.form.get('has_diabetes'),
        #     'has_asthma': request.form.get('has_asthma'),
        #     'has_bp': request.form.get('has_bp'),
        #     'has_epilepsy': request.form.get('has_epilepsy')
        # })
        
        patient_data = {
            # General Information
            'name': request.form.get('name', '').strip(),
            'opd_uid': request.form.get('opd_uid', '').strip(),
            'age': int(request.form.get('age', 0)),
            'gender': request.form.get('gender', '').strip(),
            'doctor_referred': request.form.get('doctor_referred', '').strip(),
            'address': request.form.get('address', '').strip(),
            'occupation_husband': request.form.get('occupation_husband', '').strip(),
            'occupation_wife': request.form.get('occupation_wife', '').strip(),
            'education': request.form.get('education', '').strip(),
            'phone1': request.form.get('phone1', '').strip(),
            'phone2': request.form.get('phone2', '').strip(),
            'email': request.form.get('email', '').strip(),
            'has_insurance': convert_to_bool(request.form.get('has_insurance')),
            'registration_date': request.form.get('registration_date', '').strip(),
            
            # Additional Basic Information
            # 'gender': request.form.get('gender', 'female'),
            # 'marital_status': request.form.get('marital_status', '').strip(),
            # 'blood_group': request.form.get('blood_group', '').strip(),
            # 'medical_conditions': request.form.get('medical_conditions', '').strip(),
            # 'medications': request.form.get('medications', '').strip(),
            # 'allergies': request.form.get('allergies', '').strip(),
            # 'emergency_contact_name': request.form.get('emergency_contact_name', '').strip(),
            # 'emergency_contact_relationship': request.form.get('emergency_contact_relationship', '').strip(),
            # 'emergency_contact_phone': request.form.get('emergency_contact_phone', '').strip(),
            # 'emergency_contact_phone_alt': request.form.get('emergency_contact_phone_alt', '').strip(),
            
            # Family Information
            'years_of_marriage': request.form.get('years_of_marriage', '').strip() or None,
            'boys_count': int(request.form.get('boys_count', 0)),
            'girls_count': int(request.form.get('girls_count', 0)),
            'had_abortion': convert_to_bool(request.form.get('had_abortion')),
            'abortion_count': int(request.form.get('abortion_count', 0)),
            'delivery_type': request.form.get('delivery_type', 'none'),
            
            # Menstrual Information
            'last_menstruation_date': request.form.get('last_menstruation_date', '').strip() or None,
            'menstruation_days': request.form.get('menstruation_days', '').strip() or None,
            'menstruation_cycle_length': request.form.get('menstruation_cycle_length', '').strip() or None,
            'menstruation_start_age': request.form.get('menstruation_start_age', '').strip() or None,
            
            # Other existing fields
            # 'date_of_birth': request.form.get('date_of_birth', '').strip() or None,
            
            # Medical History
            'previous_surgeries': request.form.get('previous_surgeries', '').strip(),
            'has_thyroid': int(request.form.get('has_thyroid', '0')),
            'has_diabetes': int(request.form.get('has_diabetes', '0')),
            'has_asthma': int(request.form.get('has_asthma', '0')),
            'has_bp': int(request.form.get('has_bp', '0')),
            'has_epilepsy': int(request.form.get('has_epilepsy', '0')),
            'on_medication': int(request.form.get('on_medication', '0')),
            'medication_names': request.form.get('medication_names', '').strip(),
            'had_pap_smear': int(request.form.get('had_pap_smear', '0')),
            'pap_smear_days': request.form.get('pap_smear_days', '').strip() or None,
            'medicine_allergies': request.form.get('medicine_allergies', '').strip(),
            'has_cancer_history': convert_to_bool(request.form.get('has_cancer_history')),
            'previous_reports': request.form.get('previous_reports', '').strip(),
            'report_files_path': request.form.get('report_files_path', '').strip(),
            
            # Symptoms & Complaints
            'has_blood_clots': convert_to_bool(request.form.get('has_blood_clots')),
            'blood_clots_days': request.form.get('blood_clots_days', '').strip() or None,
            'has_white_discharge': convert_to_bool(request.form.get('has_white_discharge')),
            'white_discharge_days': request.form.get('white_discharge_days', '').strip() or None,
            'has_red_discharge': convert_to_bool(request.form.get('has_red_discharge')),
            'red_discharge_days': request.form.get('red_discharge_days', '').strip() or None,
            'has_abdominal_pain': convert_to_bool(request.form.get('has_abdominal_pain')),
            'abdominal_pain_days': request.form.get('abdominal_pain_days', '').strip() or None,
            'has_vaginal_discharge': convert_to_bool(request.form.get('has_vaginal_discharge')),
            'vaginal_discharge_days': request.form.get('vaginal_discharge_days', '').strip() or None,
            'has_bleeding_intercourse': convert_to_bool(request.form.get('has_bleeding_intercourse')),
            'bleeding_intercourse_days': request.form.get('bleeding_intercourse_days', '').strip() or None,
            'has_urine_leakage': convert_to_bool(request.form.get('has_urine_leakage')),
            'urine_leakage_days': request.form.get('urine_leakage_days', '').strip() or None,
            'has_postmenopausal_bleeding': convert_to_bool(request.form.get('has_postmenopausal_bleeding')),
            'postmenopausal_bleeding_days': request.form.get('postmenopausal_bleeding_days', '').strip() or None,
            'has_breast_lump': convert_to_bool(request.form.get('has_breast_lump')),
            'breast_lump_days': request.form.get('breast_lump_days', '').strip() or None,
            'has_infertility': convert_to_bool(request.form.get('has_infertility')),
            'infertility_days': request.form.get('infertility_days', '').strip() or None,
            'other_troubles': request.form.get('other_troubles', '').strip(),
            'other_troubles_days': request.form.get('other_troubles_days', '').strip() or None,
            
            # General Examination
            'height': request.form.get('height', '').strip() or None,
            'weight': request.form.get('weight', '').strip() or None,
            'pulse_rate': request.form.get('pulse_rate', '').strip() or None,
            'blood_pressure': request.form.get('blood_pressure', '').strip(),
            'pallar': request.form.get('pallar', '').strip(),
            'edema': request.form.get('edema', '').strip(),
            'thyroid_exam': request.form.get('thyroid_exam', '').strip(),
            'lymph_nodes': request.form.get('lymph_nodes', '').strip(),
            'breast_exam': request.form.get('breast_exam', '').strip(),
            'rs_exam': request.form.get('rs_exam', '').strip(),
            'cvs_exam': request.form.get('cvs_exam', '').strip(),
            'pa_exam': request.form.get('pa_exam', '').strip(),
            'psv_exam': request.form.get('psv_exam', '').strip(),
            'pr_exam': request.form.get('pr_exam', '').strip(),
            
            # Surgery Details
            'surgery_name': request.form.get('surgery_name', '').strip(),
            'surgery_date': request.form.get('surgery_date', '').strip() or None,
            'surgery_hospital': request.form.get('surgery_hospital', '').strip(),
            'preop_investigation': request.form.get('preop_investigation', '').strip(),
            'preop_fitness': request.form.get('preop_fitness', '').strip(),
            'report_files': ','.join(uploaded_files) if uploaded_files else None
        }
        
        try:
            create_patient(patient_data)
            flash('Patient added successfully!', 'success')
            return redirect(url_for('patients.patient_list'))
        except Exception as e:
            print("Error creating patient:", str(e))  # Debug print
            flash('Error adding patient. Please try again.', 'danger')
            return render_template('patients/add.html', 
                                patient=request.form,
                                doctors=get_doctors_for_dropdown(),
                                today_date=date.today().strftime('%Y-%m-%d'))
    
    # For GET request
    active_doctors = get_doctors_for_dropdown()
    default_patient = {
        'gender': 'female',
        'marital_status': '',
        'blood_group': '',
        'medical_conditions': '',
        'medications': '',
        'allergies': '',
        'emergency_contact_name': '',
        'emergency_contact_relationship': '',
        'emergency_contact_phone': '',
        'emergency_contact_phone_alt': ''
    }
    
    return render_template('patients/add.html', 
                         patient=default_patient,
                         doctors=active_doctors,
                         today_date=date.today().strftime('%Y-%m-%d'))

@patients_bp.route('/patients/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'doctor', 'staff'])
def edit_patient(id):
    patient = get_patient_by_id(id)
    if not patient:
        flash('Patient not found.', 'danger')
        return redirect(url_for('patients.patient_list'))
    
    if request.method == 'POST':
        # Handle new file uploads
        new_files = []
        if 'report_files' in request.files:
            files = request.files.getlist('report_files')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    unique_filename = f"{timestamp}_{filename}"
                    
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
                    new_files.append(unique_filename)

        # Get existing files - handle as dictionary access
        existing_files = patient.get('report_files', '').split(',') if patient.get('report_files') else []
        # Filter out empty strings
        existing_files = [f for f in existing_files if f]
        # Combine with new files
        all_files = existing_files + new_files
        
        patient_data = {
            # General Information
            'name': request.form.get('name', '').strip(),
            'opd_uid': request.form.get('opd_uid', '').strip(),
            'age': int(request.form.get('age', 0)),
            'gender': request.form.get('gender', '').strip(),
            'doctor_referred': request.form.get('doctor_referred', '').strip(),
            'address': request.form.get('address', '').strip(),
            'occupation_husband': request.form.get('occupation_husband', '').strip(),
            'occupation_wife': request.form.get('occupation_wife', '').strip(),
            'education': request.form.get('education', '').strip(),
            'phone1': request.form.get('phone1', '').strip(),
            'phone2': request.form.get('phone2', '').strip(),
            'email': request.form.get('email', '').strip(),
            'has_insurance': bool(int(request.form.get('has_insurance', '0'))),
            'registration_date': request.form.get('registration_date', '').strip(),
            
            # Family Information
            'years_of_marriage': request.form.get('years_of_marriage', '').strip() or None,
            'boys_count': int(request.form.get('boys_count', 0)),
            'girls_count': int(request.form.get('girls_count', 0)),
            'had_abortion': bool(int(request.form.get('had_abortion', '0'))),
            'abortion_count': int(request.form.get('abortion_count', 0)),
            'delivery_type': request.form.get('delivery_type', 'none'),
            
            # Menstrual Information
            'last_menstruation_date': request.form.get('last_menstruation_date', '').strip() or None,
            'menstruation_days': request.form.get('menstruation_days', '').strip() or None,
            'menstruation_cycle_length': request.form.get('menstruation_cycle_length', '').strip() or None,
            'menstruation_start_age': request.form.get('menstruation_start_age', '').strip() or None,
            
            # Other existing fields
            'date_of_birth': request.form.get('date_of_birth', '').strip() or None,
            'gender': request.form.get('gender', 'female'),
            'marital_status': request.form.get('marital_status', '').strip(),
            'blood_group': request.form.get('blood_group', '').strip(),
            'medical_conditions': request.form.get('medical_conditions', '').strip(),
            'medications': request.form.get('medications', '').strip(),
            'allergies': request.form.get('allergies', '').strip(),
            'emergency_contact_name': request.form.get('emergency_contact_name', '').strip(),
            'emergency_contact_relationship': request.form.get('emergency_contact_relationship', '').strip(),
            'emergency_contact_phone': request.form.get('emergency_contact_phone', '').strip(),
            'emergency_contact_phone_alt': request.form.get('emergency_contact_phone_alt', '').strip(),
            
            # Medical History
            'previous_surgeries': request.form.get('previous_surgeries', '').strip(),
            'has_thyroid': convert_checkbox_value(request.form.get('has_thyroid')),
            'has_diabetes': convert_checkbox_value(request.form.get('has_diabetes')),
            'has_asthma': convert_checkbox_value(request.form.get('has_asthma')),
            'has_bp': convert_checkbox_value(request.form.get('has_bp')),
            'has_epilepsy': convert_checkbox_value(request.form.get('has_epilepsy')),
            'on_medication': convert_checkbox_value(request.form.get('on_medication')),
            'medication_names': request.form.get('medication_names', '').strip(),
            'had_pap_smear': convert_checkbox_value(request.form.get('had_pap_smear')),
            'pap_smear_days': request.form.get('pap_smear_days', '').strip() or None,
            'medicine_allergies': request.form.get('medicine_allergies', '').strip(),
            'has_cancer_history': convert_checkbox_value(request.form.get('has_cancer_history')),
            'previous_reports': request.form.get('previous_reports', '').strip(),
            'report_files_path': request.form.get('report_files_path', '').strip(),
            
            # Symptoms & Complaints
            'has_blood_clots': convert_checkbox_value(request.form.get('has_blood_clots')),
            'blood_clots_days': request.form.get('blood_clots_days', '').strip() or None,
            'has_white_discharge': convert_checkbox_value(request.form.get('has_white_discharge')),
            'white_discharge_days': request.form.get('white_discharge_days', '').strip() or None,
            'has_red_discharge': convert_checkbox_value(request.form.get('has_red_discharge')),
            'red_discharge_days': request.form.get('red_discharge_days', '').strip() or None,
            'has_abdominal_pain': convert_checkbox_value(request.form.get('has_abdominal_pain')),
            'abdominal_pain_days': request.form.get('abdominal_pain_days', '').strip() or None,
            'has_vaginal_discharge': convert_checkbox_value(request.form.get('has_vaginal_discharge')),
            'vaginal_discharge_days': request.form.get('vaginal_discharge_days', '').strip() or None,
            'has_bleeding_intercourse': convert_checkbox_value(request.form.get('has_bleeding_intercourse')),
            'bleeding_intercourse_days': request.form.get('bleeding_intercourse_days', '').strip() or None,
            'has_urine_leakage': convert_checkbox_value(request.form.get('has_urine_leakage')),
            'urine_leakage_days': request.form.get('urine_leakage_days', '').strip() or None,
            'has_postmenopausal_bleeding': convert_checkbox_value(request.form.get('has_postmenopausal_bleeding')),
            'postmenopausal_bleeding_days': request.form.get('postmenopausal_bleeding_days', '').strip() or None,
            'has_breast_lump': convert_checkbox_value(request.form.get('has_breast_lump')),
            'breast_lump_days': request.form.get('breast_lump_days', '').strip() or None,
            'has_infertility': convert_checkbox_value(request.form.get('has_infertility')),
            'infertility_days': request.form.get('infertility_days', '').strip() or None,
            'other_troubles': request.form.get('other_troubles', '').strip(),
            'other_troubles_days': request.form.get('other_troubles_days', '').strip() or None,
            
            # General Examination
            'height': request.form.get('height', '').strip() or None,
            'weight': request.form.get('weight', '').strip() or None,
            'pulse_rate': request.form.get('pulse_rate', '').strip() or None,
            'blood_pressure': request.form.get('blood_pressure', '').strip(),
            'pallar': request.form.get('pallar', '').strip(),
            'edema': request.form.get('edema', '').strip(),
            'thyroid_exam': request.form.get('thyroid_exam', '').strip(),
            'lymph_nodes': request.form.get('lymph_nodes', '').strip(),
            'breast_exam': request.form.get('breast_exam', '').strip(),
            'rs_exam': request.form.get('rs_exam', '').strip(),
            'cvs_exam': request.form.get('cvs_exam', '').strip(),
            'pa_exam': request.form.get('pa_exam', '').strip(),
            'psv_exam': request.form.get('psv_exam', '').strip(),
            'pr_exam': request.form.get('pr_exam', '').strip(),
            
            # Surgery Details
            'surgery_name': request.form.get('surgery_name', '').strip(),
            'surgery_date': request.form.get('surgery_date', '').strip() or None,
            'surgery_hospital': request.form.get('surgery_hospital', '').strip(),
            'preop_investigation': request.form.get('preop_investigation', '').strip(),
            'preop_fitness': request.form.get('preop_fitness', '').strip(),
            'report_files': ','.join(all_files) if all_files else None
        }
        
        try:
            update_patient(id, patient_data)
            flash('Patient updated successfully!', 'success')
            return redirect(url_for('patients.patient_list'))
        except Exception as e:
            flash('Error updating patient. Please try again.', 'danger')
    
    # Get both active doctors and current doctor if inactive
    doctors = get_doctors_for_dropdown(patient.get('doctor_referred'))
    return render_template('patients/edit.html', 
                         patient=patient,
                         doctors=doctors)

@patients_bp.route('/patients/delete/<int:id>')
@login_required
@role_required(['admin'])
def delete_patient_route(id):
    try:
        # Get patient files before deletion
        patient = get_patient_by_id(id)
        if patient and patient.get('report_files'):
            # Delete associated files
            for filename in patient['report_files'].split(','):
                if filename:
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)
        
        delete_patient(id)
        flash('Patient deleted successfully!', 'success')
    except Exception as e:
        print(f"Error deleting patient: {str(e)}")
        flash('Error deleting patient. Please try again.', 'danger')
    return redirect(url_for('patients.patient_list')) 

@patients_bp.route('/patients/delete-file/<int:patient_id>/<path:filename>')
@login_required
@role_required(['admin', 'doctor', 'staff'])
def delete_file(patient_id, filename):
    patient = get_patient_by_id(patient_id)
    if not patient:
        flash('Patient not found', 'error')
        return redirect(url_for('patients.patient_list'))
    
    # Check if file exists in patient's files
    existing_files = patient.get('report_files', '').split(',') if patient.get('report_files') else []
    if filename in existing_files:
        # Remove file from filesystem
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Remove file from patient's record
        existing_files.remove(filename)
        patient_data = {
            'report_files': ','.join(existing_files) if existing_files else None
        }
        update_patient(patient_id, patient_data)
        
        flash('File deleted successfully', 'success')
    else:
        flash('File not found', 'error')
    
    return redirect(url_for('patients.edit_patient', id=patient_id)) 

@patients_bp.route('/patients/print/<int:id>')
@login_required
@role_required(['admin', 'doctor', 'staff'])
def print_patient(id):
    patient = get_patient_by_id(id)
    if not patient:
        flash('Patient not found.', 'danger')
        return redirect(url_for('patients.patient_list'))
    
    pdf_buffer = create_patient_pdf(patient)
    return send_file(
        pdf_buffer,
        download_name=f'patient_{patient["name"]}_{patient["opd_uid"]}.pdf',
        mimetype='application/pdf'
    ) 

@patients_bp.route('/patients/<int:id>/followups')
@login_required
@role_required(['admin', 'doctor', 'staff'])
def patient_followups(id):
    patient = get_patient_by_id(id)
    if not patient:
        flash('Patient not found.', 'danger')
        return redirect(url_for('patients.patient_list'))
    
    followups = get_patient_followups(id)
    return render_template('patients/followups.html', 
                         patient=patient, 
                         followups=followups)

@patients_bp.route('/patients/<int:id>/followups/add', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'doctor'])
def add_followup(id):
    if request.method == 'POST':
        followup_data = {
            'patient_id': id,
            'visit_date': request.form.get('visit_date'),
            'complaints': request.form.get('complaints'),
            'examination': request.form.get('examination'),
            'diagnosis': request.form.get('diagnosis'),
            'treatment': request.form.get('treatment'),
            'next_visit_date': request.form.get('next_visit_date'),
            'doctor_name': request.form.get('doctor_name')
        }
        
        try:
            # Create followup
            followup_id = create_followup(followup_data)
            
            # Handle prescriptions
            prescriptions_json = request.form.get('prescriptions')
            if prescriptions_json:
                prescriptions = json.loads(prescriptions_json)
                save_prescription(followup_id, prescriptions)
            
            flash('Follow-up added successfully!', 'success')
            return redirect(url_for('patients.patient_followups', id=id))
        except Exception as e:
            flash('Error adding follow-up. Please try again.', 'danger')
            return render_template('patients/add_followup.html',
                                patient=get_patient_by_id(id),
                                doctors=get_active_doctors(),
                                medicines=get_all_medicines(),
                                today_date=date.today().strftime('%Y-%m-%d'))

    return render_template('patients/add_followup.html',
                         patient=get_patient_by_id(id),
                         doctors=get_active_doctors(),
                         medicines=get_all_medicines(),
                         today_date=date.today().strftime('%Y-%m-%d'))

@patients_bp.route('/followups/print/<int:id>')
@login_required
@role_required(['admin', 'doctor', 'staff'])
def print_followup(id):
    followup = get_followup_by_id(id)
    if not followup:
        flash('Follow-up not found.', 'danger')
        return redirect(url_for('patients.patient_list'))
    
    patient = get_patient_by_id(followup['patient_id'])
    
    pdf_buffer = create_followup_pdf(followup, patient)
    return send_file(
        pdf_buffer,
        download_name=f'followup_{patient["name"]}_{followup["visit_date"].strftime("%Y%m%d")}.pdf',
        mimetype='application/pdf'
    ) 

@patients_bp.route('/patients/followups/delete/<int:id>')
@login_required
@role_required(['admin', 'doctor'])
def delete_followup(id):
    try:
        # Get followup to check patient_id
        followup = get_followup_by_id(id)
        if not followup:
            flash('Follow-up not found.', 'danger')
            return redirect(url_for('patients.patient_list'))
        
        patient_id = followup['patient_id']
        delete_followup_record(id)
        flash('Follow-up deleted successfully!', 'success')
        return redirect(url_for('patients.patient_followups', id=patient_id))
    except Exception as e:
        print(f"Error deleting followup: {str(e)}")
        flash('Error deleting follow-up. Please try again.', 'danger')
        return redirect(url_for('patients.patient_followups', id=patient_id)) 