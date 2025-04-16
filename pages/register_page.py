import streamlit as st

class RegisterPage:
    def __init__(self, auth, file_handler):
        self.auth = auth
        self.file_handler = file_handler
    
    def show(self):
        st.markdown("<h2 class='sub-header'>Student Registration</h2>", unsafe_allow_html=True)
        
        with st.form("register_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            submit_button = st.form_submit_button("Register")
            
            if submit_button:
                if not name or not email or not password or not confirm_password:
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    success, message = self.auth.register_student(name, email, password)
                    
                    if success:
                        # Log the registration action
                        students = self.file_handler.read_json_file('students.json')
                        student_id = next((s['id'] for s in students if s['email'] == email), None)
                        
                        if student_id:
                            self.file_handler.log_action(
                                student_id,
                                "student",
                                "registration",
                                f"New student {name} registered"
                            )
                        
                        st.success(message)
                    else:
                        st.error(message)
        
        st.markdown("---")
        st.markdown("Already have an account? Login using the Login option.")