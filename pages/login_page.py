import streamlit as st

class LoginPage:
    def __init__(self, auth, file_handler):
        self.auth = auth
        self.file_handler = file_handler
    
    def show(self):
        st.markdown("<h2 class='sub-header'>Login</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["student", "admin"])
            
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if not email or not password:
                    st.error("Please fill in all fields")
                else:
                    success, result = self.auth.login(email, password, role)
                    
                    if success:
                        # Set session state
                        st.session_state.logged_in = True
                        st.session_state.user_role = result["role"]
                        st.session_state.user_id = result["id"]
                        st.session_state.user_name = result["name"]
                        
                        # Log the login action
                        self.file_handler.log_action(
                            result["id"],
                            result["role"],
                            "login",
                            f"{result['name']} logged in as {result['role']}"
                        )
                        
                        st.success(f"Welcome, {result['name']}!")
                        st.rerun()

                    else:
                        st.error(result)
        
        st.markdown("---")
        st.markdown("Don't have an account? Register as a student using the Register option.")