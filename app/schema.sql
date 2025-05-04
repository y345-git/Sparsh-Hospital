CREATE TABLE IF NOT EXISTS followups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    visit_date DATE NOT NULL,
    complaints TEXT,
    examination TEXT,
    diagnosis TEXT,
    treatment TEXT,
    next_visit_date DATE,
    doctor_name VARCHAR(255),
    created_at DATETIME NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
); 