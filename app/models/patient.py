from app.models.user import get_db_connection
import pymysql

def get_all_patients():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('''
        SELECT id, name, opd_uid, age, gender, phone1, email, 
               registration_date, status 
        FROM patients 
        ORDER BY registration_date DESC
    ''')
    patients = cursor.fetchall()
    
    # Add default values for any missing fields
    for patient in patients:
        if patient.get('gender') is None:
            patient['gender'] = 'female'
    
    cursor.close()
    conn.close()
    return patients

def get_patient_by_id(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM patients WHERE id = %s', (patient_id,))
    patient = cursor.fetchone()
    
    # Add default values if patient exists
    if patient:
        # Convert None values to empty strings or appropriate defaults
        defaults = {
            'report_files': ''  # Add default for report_files
        }
        
        for key, default_value in defaults.items():
            if patient.get(key) is None:
                patient[key] = default_value
    
    cursor.close()
    conn.close()
    return patient

def create_patient(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO patients (
            -- General Information
            name, opd_uid, age, gender, doctor_referred, address,
            occupation_husband, occupation_wife, education,
            phone1, phone2, email, has_insurance, registration_date,
            
            -- Family Information
            years_of_marriage, boys_count, girls_count,
            had_abortion, abortion_count, delivery_type,
            
            -- Menstrual Information
            last_menstruation_date, menstruation_days,
            menstruation_cycle_length, menstruation_start_age,
            
            -- Medical History
            previous_surgeries,
            has_thyroid, has_diabetes, has_asthma,
            has_bp, has_epilepsy,
            on_medication, medication_names,
            had_pap_smear, pap_smear_days,
            medicine_allergies, has_cancer_history,
            previous_reports, report_files,
            
            -- General Examination
            height, weight, pulse_rate, blood_pressure,
            pallar, edema, thyroid_exam, lymph_nodes,
            breast_exam, rs_exam, cvs_exam,
            pa_exam, psv_exam, pr_exam,
            
            -- Surgery Details
            surgery_name, surgery_date, surgery_hospital,
            preop_investigation, preop_fitness
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
    ''', (
        # General Information
        data['name'], data['opd_uid'], data['age'],
        data['gender'], data['doctor_referred'], data['address'],
        data['occupation_husband'], data['occupation_wife'], data['education'],
        data['phone1'], data['phone2'], data['email'],
        int(data.get('has_insurance', 0)), data['registration_date'],
        
        # Family Information
        data['years_of_marriage'], data['boys_count'], data['girls_count'],
        int(data.get('had_abortion', 0)), data['abortion_count'], data['delivery_type'],
        
        # Menstrual Information
        data['last_menstruation_date'], data['menstruation_days'],
        data['menstruation_cycle_length'], data['menstruation_start_age'],
        
        # Medical History
        data['previous_surgeries'],
        int(data.get('has_thyroid', 0)),
        int(data.get('has_diabetes', 0)),
        int(data.get('has_asthma', 0)),
        int(data.get('has_bp', 0)),
        int(data.get('has_epilepsy', 0)),
        int(data.get('on_medication', 0)),
        data['medication_names'],
        int(data.get('had_pap_smear', 0)),
        data['pap_smear_days'],
        data['medicine_allergies'],
        int(data.get('has_cancer_history', 0)),
        data['previous_reports'],
        data['report_files'],
        
        # General Examination
        data['height'], data['weight'], data['pulse_rate'],
        data['blood_pressure'], data['pallar'], data['edema'],
        data['thyroid_exam'], data['lymph_nodes'], data['breast_exam'],
        data['rs_exam'], data['cvs_exam'],
        data['pa_exam'], data['psv_exam'], data['pr_exam'],
        
        # Surgery Details
        data['surgery_name'], data['surgery_date'], data['surgery_hospital'],
        data['preop_investigation'], data['preop_fitness']
    ))
    
    conn.commit()
    cursor.close()
    conn.close()

def update_patient(patient_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE patients SET
            -- General Information
            name = %s, opd_uid = %s, age = %s,
            doctor_referred = %s, address = %s,
            occupation_husband = %s, occupation_wife = %s,
            education = %s, phone1 = %s, phone2 = %s,
            email = %s, has_insurance = %s, registration_date = %s,
            
            -- Family Information
            years_of_marriage = %s, boys_count = %s, girls_count = %s,
            had_abortion = %s, abortion_count = %s, delivery_type = %s,
            
            -- Menstrual Information
            last_menstruation_date = %s, menstruation_days = %s,
            menstruation_cycle_length = %s, menstruation_start_age = %s,
            
            -- Medical History
            previous_surgeries = %s,
            has_thyroid = %s, has_diabetes = %s, has_asthma = %s,
            has_bp = %s, has_epilepsy = %s,
            on_medication = %s, medication_names = %s,
            had_pap_smear = %s, pap_smear_days = %s,
            medicine_allergies = %s, has_cancer_history = %s,
            previous_reports = %s, report_files = %s,
            
            -- General Examination
            height = %s, weight = %s, pulse_rate = %s,
            blood_pressure = %s, pallar = %s, edema = %s,
            thyroid_exam = %s, lymph_nodes = %s, breast_exam = %s,
            rs_exam = %s, cvs_exam = %s,
            pa_exam = %s, psv_exam = %s, pr_exam = %s,
            
            -- Symptoms & Complaints
            has_blood_clots = %s, blood_clots_days = %s,
            has_white_discharge = %s, white_discharge_days = %s,
            has_red_discharge = %s, red_discharge_days = %s,
            has_abdominal_pain = %s, abdominal_pain_days = %s,
            has_vaginal_discharge = %s, vaginal_discharge_days = %s,
            has_bleeding_intercourse = %s, bleeding_intercourse_days = %s,
            has_urine_leakage = %s, urine_leakage_days = %s,
            has_postmenopausal_bleeding = %s, postmenopausal_bleeding_days = %s,
            has_breast_lump = %s, breast_lump_days = %s,
            has_infertility = %s, infertility_days = %s,
            other_troubles = %s, other_troubles_days = %s,
            
            -- Surgery Details
            surgery_name = %s, surgery_date = %s,
            surgery_hospital = %s, preop_investigation = %s,
            preop_fitness = %s
            
        WHERE id = %s
    ''', (
        # General Information
        data['name'], data['opd_uid'], data['age'],
        data.get('doctor_referred'), data['address'],
        data.get('occupation_husband'), data.get('occupation_wife'),
        data.get('education'), data['phone1'], data.get('phone2'),
        data.get('email'), data['has_insurance'], data['registration_date'],
        
        # Family Information
        data.get('years_of_marriage'), data['boys_count'], data['girls_count'],
        data['had_abortion'], data['abortion_count'], data['delivery_type'],
        
        # Menstrual Information
        data.get('last_menstruation_date'), data.get('menstruation_days'),
        data.get('menstruation_cycle_length'), data.get('menstruation_start_age'),
        
        # Medical History
        data.get('previous_surgeries'),
        bool(int(data.get('has_thyroid', '0'))),
        bool(int(data.get('has_diabetes', '0'))),
        bool(int(data.get('has_asthma', '0'))),
        bool(int(data.get('has_bp', '0'))),
        bool(int(data.get('has_epilepsy', '0'))),
        bool(int(data.get('on_medication', '0'))),
        data.get('medication_names'),
        bool(int(data.get('had_pap_smear', '0'))),
        data.get('pap_smear_days'),
        data.get('medicine_allergies'),
        bool(int(data.get('has_cancer_history', '0'))),
        data.get('previous_reports'),
        data.get('report_files'),
        
        # General Examination
        data.get('height'),
        data.get('weight'),
        data.get('pulse_rate'),
        data.get('blood_pressure'),
        data.get('pallar'),
        data.get('edema'),
        data.get('thyroid_exam'),
        data.get('lymph_nodes'),
        data.get('breast_exam'),
        data.get('rs_exam'),
        data.get('cvs_exam'),
        data.get('pa_exam'),
        data.get('psv_exam'),
        data.get('pr_exam'),
        
        # Symptoms & Complaints
        data.get('has_blood_clots', False),
        data.get('blood_clots_days'),
        data.get('has_white_discharge', False),
        data.get('white_discharge_days'),
        data.get('has_red_discharge', False),
        data.get('red_discharge_days'),
        data.get('has_abdominal_pain', False),
        data.get('abdominal_pain_days'),
        data.get('has_vaginal_discharge', False),
        data.get('vaginal_discharge_days'),
        data.get('has_bleeding_intercourse', False),
        data.get('bleeding_intercourse_days'),
        data.get('has_urine_leakage', False),
        data.get('urine_leakage_days'),
        data.get('has_postmenopausal_bleeding', False),
        data.get('postmenopausal_bleeding_days'),
        data.get('has_breast_lump', False),
        data.get('breast_lump_days'),
        data.get('has_infertility', False),
        data.get('infertility_days'),
        data.get('other_troubles'),
        data.get('other_troubles_days'),
        
        # Surgery Details and Where clause
        data.get('surgery_name'),
        data.get('surgery_date'),
        data.get('surgery_hospital'),
        data.get('preop_investigation'),
        data.get('preop_fitness'),
        patient_id
    ))
    
    conn.commit()
    cursor.close()
    conn.close()

def delete_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM patients WHERE id = %s', (patient_id,))
    conn.commit()
    cursor.close()
    conn.close() 