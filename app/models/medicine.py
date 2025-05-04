from app.models.user import get_db_connection
import pymysql

def get_all_medicines():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM medicines WHERE status = 'active' ORDER BY name")
    medicines = cursor.fetchall()
    cursor.close()
    conn.close()
    return medicines

def add_medicine(name, description=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medicines (name, description) VALUES (%s, %s)",
        (name, description)
    )
    conn.commit()
    medicine_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return medicine_id

def save_prescription(followup_id, prescriptions):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for prescription in prescriptions:
        cursor.execute("""
            INSERT INTO prescriptions 
            (followup_id, medicine_id, medicine_name, quantity, notes)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            followup_id,
            prescription.get('medicine_id'),
            prescription['medicine_name'],
            prescription['quantity'],
            prescription.get('notes')
        ))
    
    conn.commit()
    cursor.close()
    conn.close()

def get_followup_prescriptions(followup_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT * FROM prescriptions 
        WHERE followup_id = %s 
        ORDER BY created_at
    """, (followup_id,))
    prescriptions = cursor.fetchall()
    cursor.close()
    conn.close()
    return prescriptions 