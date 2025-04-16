import json
import os
import hashlib
import uuid
from datetime import datetime
import streamlit as st

class Authentication:
    def __init__(self):
        self.students_file = 'data/students.json'
        self.admin_file = 'data/admin.json'
        
        # Create admin file if it doesn't exist
        if not os.path.exists(self.admin_file):
            self._create_default_admin()
    
    def _create_default_admin(self):
        """Create a default admin account if none exists"""
        try:
            admin_data = {
                "id": "admin-001",
                "name": "Library Admin",
                "email": "admin@library.com",
                "password": self._hash_password("admin123"),
                "role": "admin",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            os.makedirs(os.path.dirname(self.admin_file), exist_ok=True)
            with open(self.admin_file, 'w') as f:
                json.dump([admin_data], f, indent=4)
        except Exception as e:
            st.error(f"Error creating default admin: {str(e)}")
    
    def _hash_password(self, password):
        """Hash a password for storing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, email, password, role):
        """Authenticate a user based on email, password and role"""
        try:
            if role == "admin":
                file_path = self.admin_file
            else:
                file_path = self.students_file
            
            if not os.path.exists(file_path):
                return False, "User database not found"
            
            with open(file_path, 'r') as f:
                users = json.load(f)
            
            hashed_password = self._hash_password(password)
            
            for user in users:
                if user['email'] == email and user['password'] == hashed_password:
                    # Check if student is approved
                    if role == "student" and not user.get('approved', False):
                        return False, "Your account is pending approval by the admin"
                    
                    return True, {
                        "id": user['id'],
                        "name": user['name'],
                        "role": user['role'],
                        "email": user['email'],
                        "approved": user.get('approved', True) if role == "student" else True,
                        "flagged": user.get('flagged', False) if role == "student" else False
                    }
            
            return False, "Invalid email or password"
        except Exception as e:
            return False, f"Login error: {str(e)}"
    
    def register_student(self, name, email, password):
        """Register a new student"""
        try:
            # Create students file if it doesn't exist
            if not os.path.exists(self.students_file):
                os.makedirs(os.path.dirname(self.students_file), exist_ok=True)
                with open(self.students_file, 'w') as f:
                    json.dump([], f)
            
            # Check if email already exists
            with open(self.students_file, 'r') as f:
                students = json.load(f)
            
            for student in students:
                if student['email'] == email:
                    return False, "Email already registered"
            
            # Create new student
            new_student = {
                "id": f"STU-{uuid.uuid4().hex[:6].upper()}",
                "name": name,
                "email": email,
                "password": self._hash_password(password),
                "role": "student",
                "approved": False,
                "flagged": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            students.append(new_student)
            
            # Save updated students list
            with open(self.students_file, 'w') as f:
                json.dump(students, f, indent=4)
            
            return True, "Registration successful! Please wait for admin approval."
        except Exception as e:
            return False, f"Registration error: {str(e)}"