import mysql.connector
import bcrypt
from config import DB_CONFIG

# Connect to MySQL
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Create users table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
)
""")

def register_user(username, password):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        print("User registered successfully!")
    except mysql.connector.Error as err:
        print("Error:", err)

def login_user(username, password):
    cursor.execute("SELECT password_hash FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        print("Login successful!")
    else:
        print("Invalid username or password.")

# Example usage
if __name__ == "__main__":
    register_user("krishna", "securepassword123")
    login_user("krishna", "securepassword123")
