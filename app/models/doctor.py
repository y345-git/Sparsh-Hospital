from app.models.user import get_db_connection
import pymysql

def get_all_doctors():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM doctors ORDER BY name')
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return doctors

def get_doctor_by_id(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM doctors WHERE id = %s', (doctor_id,))
    doctor = cursor.fetchone()
    cursor.close()
    conn.close()
    return doctor

def create_doctor(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO doctors (name, specialization, email, phone, address, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (data['name'], data['specialization'], data['email'], 
          data['phone'], data['address'], data['status']))
    conn.commit()
    cursor.close()
    conn.close()

def update_doctor(doctor_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE doctors 
        SET name = %s, specialization = %s, email = %s, phone = %s, address = %s, status = %s
        WHERE id = %s
    ''', (data['name'], data['specialization'], data['email'], data['phone'], 
          data['address'], data['status'], doctor_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_doctor(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM doctors WHERE id = %s', (doctor_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_active_doctors():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT id, name, specialization FROM doctors WHERE status = "active" ORDER BY name')
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return doctors 

def get_doctors_for_dropdown(selected_doctor_id=None):
    """Get list of doctors for dropdown with optional selected doctor"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        # First get the selected doctor if one is specified
        selected_doctor = None
        if selected_doctor_id:
            cursor.execute("""
                SELECT id, name, specialization, status 
                FROM doctors 
                WHERE id = %s
            """, (selected_doctor_id,))
            selected_doctor = cursor.fetchone()
        
        # Get all active doctors
        cursor.execute("""
            SELECT id, name, specialization, status 
            FROM doctors 
            WHERE status = 'active' 
            ORDER BY name
        """)
        active_doctors = cursor.fetchall()
        
        # Create a list of unique doctors (avoiding duplicates if selected doctor is active)
        doctors_list = []
        seen_ids = set()
        
        # Add selected doctor first if exists
        if selected_doctor:
            doctors_list.append(selected_doctor)
            seen_ids.add(selected_doctor['id'])
        
        # Add all active doctors
        for doctor in active_doctors:
            if doctor['id'] not in seen_ids:
                doctors_list.append(doctor)
                seen_ids.add(doctor['id'])
        
        cursor.close()
        conn.close()
        
        # Format doctors for dropdown
        formatted_list = []
        for doctor in doctors_list:
            # Only add specialization if it exists and is not empty
            formatted_name = doctor['name']
            if doctor['specialization'] and doctor['specialization'].strip():
                formatted_name += f" - {doctor['specialization']}"
            
            if doctor['status'] == 'inactive':
                formatted_name += " (Inactive)"
                
            formatted_list.append({
                'id': str(doctor['id']),
                'name': formatted_name,
                'selected': str(doctor['id']) == str(selected_doctor_id) if selected_doctor_id else False
            })
            
        return formatted_list
        
    except Exception as e:
        print(f"Error getting doctors for dropdown: {e}")
        return [] 