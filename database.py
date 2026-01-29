import pymysql
from pymysql.cursors import DictCursor

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Suji@2007',  # XAMPP default password is empty
    'database': 'sujidb',
    'cursorclass': DictCursor
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None
def close_db_connection(connection):
    """Close database connection"""
    if connection:
        connection.close()

# ========================================
# USER RELATED FUNCTIONS
# ========================================

def get_user_by_email(email):
    """Get user details by email"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        cursor.close()
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        close_db_connection(connection)

def authenticate_user(email, password):
    """Check if user exists with given credentials"""
    user = get_user_by_email(email)
    if user and user['password'] == password:
        return user
    return None 
def create_user(name, email, password, role):
    """Create a new user (teacher/student)"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, password, role))
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False
    finally:
        close_db_connection(connection)   
def create_exam(teacher_id, title, subject, total_marks, question_paper, answer_key):
    """Create a new exam"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        query = """INSERT INTO exams (teacher_id, title, subject, total_marks, question_paper, answer_key) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (teacher_id, title, subject, total_marks, question_paper, answer_key))
        exam_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        return exam_id
    except Exception as e:
        print(f"Error creating exam: {e}")
        return None
    finally:
        close_db_connection(connection)
def get_teacher_exams(teacher_id):
    """Get all exams created by a teacher"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM exams WHERE teacher_id = %s ORDER BY created_at DESC"
        cursor.execute(query, (teacher_id,))
        exams = cursor.fetchall()
        cursor.close()
        return exams
    except Exception as e:
        print(f"Error fetching exams: {e}")
        return []
    finally:
        close_db_connection(connection)
def upload_answer_sheet(exam_id, student_id, answer_sheet_filename):
    """Upload student answer sheet"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        query = "INSERT INTO answer_sheets (exam_id, student_id, answer_sheet) VALUES (%s, %s, %s)"
        cursor.execute(query, (exam_id, student_id, answer_sheet_filename))
        sheet_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        return sheet_id
    except Exception as e:
        print(f"Error uploading answer sheet: {e}")
        return None
    finally:
        close_db_connection(connection)
def get_student_answer_sheets(student_id):
    """Get all answer sheets of a student"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        query = """SELECT a.*, e.title, e.subject 
                   FROM answer_sheets a 
                   JOIN exams e ON a.exam_id = e.id 
                   WHERE a.student_id = %s 
                   ORDER BY a.uploaded_at DESC"""
        cursor.execute(query, (student_id,))
        sheets = cursor.fetchall()
        cursor.close()
        return sheets
    except Exception as e:
        print(f"Error fetching answer sheets: {e}")
        return []
    finally:
        close_db_connection(connection)
def save_result(answer_sheet_id, score, total_marks, percentage, weak_areas, feedback):
    """Save evaluation result"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        query = """INSERT INTO results (answer_sheet_id, score, total_marks, percentage, weak_areas, feedback) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (answer_sheet_id, score, total_marks, percentage, weak_areas, feedback))
        result_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        return result_id
    except Exception as e:
        print(f"Error saving result: {e}")
        return None
    finally:
        close_db_connection(connection)
def get_student_results(student_id):
    """Get all results of a student"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        query = """SELECT r.*, e.title, e.subject, u.name as student_name
                   FROM results r
                   JOIN answer_sheets a ON r.answer_sheet_id = a.id
                   JOIN exams e ON a.exam_id = e.id
                   JOIN users u ON a.student_id = u.id
                   WHERE u.id = %s
                   ORDER BY r.evaluated_at DESC"""
        cursor.execute(query, (student_id,))
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        print(f"Error fetching results: {e}")
        return []
    finally:
        close_db_connection(connection)
def get_student_latest_result(student_id):
    """Get latest result of a student (for dashboard)"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        query = """SELECT r.*, e.title, e.subject
                   FROM results r
                   JOIN answer_sheets a ON r.answer_sheet_id = a.id
                   JOIN exams e ON a.exam_id = e.id
                   WHERE a.student_id = %s
                   ORDER BY r.evaluated_at DESC
                   LIMIT 1"""
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        print(f"Error fetching latest result: {e}")
        return None
    finally:
        close_db_connection(connection)
def test_connection():
    """Test database connection"""
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()
            print(f" Connected to database: {db_name}")
            
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print(f" Tables: {[list(t.values())[0] for t in tables]}")
            
            cursor.close()
            close_db_connection(connection)
            return True
        return False
    except Exception as e:
        print(f" Connection error: {e}")
        return False

# Test when file is run directly
if __name__ == '__main__':
    test_connection()       