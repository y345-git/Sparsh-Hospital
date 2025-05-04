import pymysql
import socket

def test_connection():
    host = "5.180.255.213"
    port = 5551
    user = "root"
    password = "a9AknLDiC5laxxK4QAx2EiEXGrXzKnBxrx57bVKnY3rbfkmjaPWRhp2S59E0hl5V"
    database = "hospital_management"

    # First test socket connection
    print(f"Testing socket connection to {host}:{port}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    try:
        sock.connect((host, port))
        sock.close()
        print("Socket connection successful")
    except socket.error as e:
        print(f"Socket connection failed: {e}")
        return

    # Then test MySQL connection
    print("\nTesting MySQL connection")
    connection_params = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': database,
        'connect_timeout': 10,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
        'unix_socket': None,
        'ssl': None,
        'read_timeout': 10,
        'write_timeout': 10,
        'use_unicode': True,
        'client_flag': 0
    }

    try:
        connection = pymysql.connect(**connection_params)
        print("Successfully connected to MySQL database!")
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
    except Exception as e:
        print("Error while connecting to MySQL:", e)
    finally:
        if 'connection' in locals():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    test_connection() 