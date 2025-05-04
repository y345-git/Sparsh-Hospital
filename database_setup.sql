DROP DATABASE IF EXISTS hospital_management;
CREATE DATABASE IF NOT EXISTS hospital_management;
USE hospital_management;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'doctor', 'staff') NOT NULL DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Generate a new hash for admin123 and insert it
INSERT INTO users (name, email, password, role) 
VALUES (
    'Administrator', 
    'admin@hospital.com',
    'pbkdf2:sha256:1000000$bu8EE6W551mM3zJ9$3db7b3e4cec45d4c2a0c5cc68b7afd51dcf07410eb60df6d2d3bfe4744c34304',
    'admin'
);

CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address TEXT,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- General Information
    name VARCHAR(100) NOT NULL,
    opd_uid VARCHAR(50) UNIQUE NOT NULL,
    age INT NOT NULL,
    gender ENUM('female', 'male', 'other') NOT NULL DEFAULT 'female',
    doctor_referred VARCHAR(100),
    address TEXT,
    occupation_husband VARCHAR(100),
    occupation_wife VARCHAR(100),
    education VARCHAR(100),
    phone1 VARCHAR(20) NOT NULL,
    phone2 VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    has_insurance BOOLEAN DEFAULT FALSE,
    registration_date DATE NOT NULL,
    
    -- Family Information
    years_of_marriage INT,
    boys_count INT DEFAULT 0,
    girls_count INT DEFAULT 0,
    had_abortion BOOLEAN DEFAULT FALSE,
    abortion_count INT DEFAULT 0,
    delivery_type ENUM('normal', 'cesarean', 'both', 'none') DEFAULT 'none',
    
    -- Menstrual Information
    last_menstruation_date DATE,
    menstruation_days INT,
    menstruation_cycle_length INT,
    menstruation_start_age INT,
    
    -- Medical History
    previous_surgeries TEXT,
    has_thyroid BOOLEAN DEFAULT FALSE,
    has_diabetes BOOLEAN DEFAULT FALSE,
    has_asthma BOOLEAN DEFAULT FALSE,
    has_bp BOOLEAN DEFAULT FALSE,
    has_epilepsy BOOLEAN DEFAULT FALSE,
    on_medication BOOLEAN DEFAULT FALSE,
    medication_names TEXT,
    had_pap_smear BOOLEAN DEFAULT FALSE,
    pap_smear_days INT,
    medicine_allergies TEXT,
    has_cancer_history BOOLEAN DEFAULT FALSE,
    previous_reports TEXT,
    report_files TEXT,
    
    -- Symptoms & Complaints
    has_blood_clots BOOLEAN DEFAULT FALSE,
    blood_clots_days INT,
    has_white_discharge BOOLEAN DEFAULT FALSE,
    white_discharge_days INT,
    has_red_discharge BOOLEAN DEFAULT FALSE,
    red_discharge_days INT,
    has_abdominal_pain BOOLEAN DEFAULT FALSE,
    abdominal_pain_days INT,
    has_vaginal_discharge BOOLEAN DEFAULT FALSE,
    vaginal_discharge_days INT,
    has_bleeding_intercourse BOOLEAN DEFAULT FALSE,
    bleeding_intercourse_days INT,
    has_urine_leakage BOOLEAN DEFAULT FALSE,
    urine_leakage_days INT,
    has_postmenopausal_bleeding BOOLEAN DEFAULT FALSE,
    postmenopausal_bleeding_days INT,
    has_breast_lump BOOLEAN DEFAULT FALSE,
    breast_lump_days INT,
    has_infertility BOOLEAN DEFAULT FALSE,
    infertility_days INT,
    other_troubles TEXT,
    other_troubles_days INT,
    
    -- General Examination
    height DECIMAL(5,2),
    weight DECIMAL(5,2),
    pulse_rate INT,
    blood_pressure VARCHAR(20),
    pallar TEXT,
    edema TEXT,
    thyroid_exam TEXT,
    lymph_nodes TEXT,
    breast_exam TEXT,
    rs_exam TEXT,
    cvs_exam TEXT,
    pa_exam TEXT,
    psv_exam TEXT,
    pr_exam TEXT,
    
    -- Surgery Details
    surgery_name VARCHAR(200),
    surgery_date DATE,
    surgery_hospital VARCHAR(200),
    preop_investigation TEXT,
    preop_fitness TEXT,
    
    -- System Fields
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE followups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    visit_date DATE NOT NULL,
    complaints TEXT,
    examination TEXT,
    diagnosis TEXT,
    treatment TEXT,
    next_visit_date DATE,
    doctor_name VARCHAR(100) NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

CREATE TABLE medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    followup_id INT NOT NULL,
    medicine_id INT,
    medicine_name VARCHAR(255) NOT NULL,
    quantity VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (followup_id) REFERENCES followups(id) ON DELETE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON DELETE SET NULL
); 