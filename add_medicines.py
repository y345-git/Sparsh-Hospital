from app.models.user import get_db_connection
from app.models.medicine import add_medicine
import pymysql

# List of common medicines with their descriptions
medicines = [
    {
        "name": "Paracetamol 500mg",
        "description": "Pain reliever and fever reducer"
    },
    {
        "name": "Amoxicillin 500mg",
        "description": "Antibiotic for bacterial infections"
    },
    {
        "name": "Omeprazole 20mg",
        "description": "Proton pump inhibitor for acid reflux and ulcers"
    },
    {
        "name": "Metformin 500mg",
        "description": "Oral diabetes medicine"
    },
    {
        "name": "Amlodipine 5mg",
        "description": "Calcium channel blocker for high blood pressure"
    },
    {
        "name": "Cetirizine 10mg",
        "description": "Antihistamine for allergies"
    },
    {
        "name": "Aspirin 75mg",
        "description": "Blood thinner and pain reliever"
    },
    {
        "name": "Metronidazole 400mg",
        "description": "Antibiotic for bacterial and parasitic infections"
    },
    {
        "name": "Diclofenac 50mg",
        "description": "Non-steroidal anti-inflammatory drug (NSAID)"
    },
    {
        "name": "Azithromycin 500mg",
        "description": "Antibiotic for bacterial infections"
    },
    {
        "name": "Pantoprazole 40mg",
        "description": "Proton pump inhibitor for acid reflux"
    },
    {
        "name": "Ciprofloxacin 500mg",
        "description": "Antibiotic for bacterial infections"
    },
    {
        "name": "Ranitidine 150mg",
        "description": "H2 blocker for acid reflux and ulcers"
    },
    {
        "name": "Ibuprofen 400mg",
        "description": "Non-steroidal anti-inflammatory drug (NSAID)"
    },
    {
        "name": "Doxycycline 100mg",
        "description": "Antibiotic for bacterial infections"
    }
]

def add_medicines_to_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if medicines already exist
    cursor.execute("SELECT COUNT(*) as count FROM medicines")
    result = cursor.fetchone()
    count = result['count'] if isinstance(result, dict) else result[0]
    
    if count > 0:
        print("Medicines already exist in the database.")
        print(f"Current medicine count: {count}")
        
        # Ask for user confirmation to proceed
        response = input("Do you want to add more medicines anyway? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return
    
    # Add medicines
    successful = 0
    failed = 0
    
    for medicine in medicines:
        try:
            # Check if medicine already exists
            cursor.execute("SELECT id FROM medicines WHERE name = %s", (medicine['name'],))
            if cursor.fetchone() is None:
                add_medicine(medicine['name'], medicine['description'])
                successful += 1
                print(f"Added: {medicine['name']}")
            else:
                print(f"Skipped (already exists): {medicine['name']}")
                failed += 1
        except Exception as e:
            print(f"Error adding {medicine['name']}: {str(e)}")
            failed += 1
    
    print("\nOperation completed!")
    print(f"Successfully added: {successful}")
    print(f"Skipped/Failed: {failed}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("Starting medicine database initialization...")
    add_medicines_to_db() 