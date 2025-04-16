import streamlit as st
import os
import json
from datetime import datetime
import pandas as pd
from auth.authentication import Authentication
from pages.admin_dashboard import AdminDashboard
from pages.student_dashboard import StudentDashboard
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from services.file_handler import FileHandler

# Initialize session state if not already done
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_id = None
    st.session_state.user_name = None

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Initialize data files if they don't exist
file_handler = FileHandler()
file_handler.initialize_data_files()

# Set page config
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .success-msg {
        color: #0f5132;
        background-color: #d1e7dd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .error-msg {
        color: #842029;
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .warning-msg {
        color: #664d03;
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .info-card {
        background-color: #cfe2ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 class='main-header'>📚 Library Management System</h1>", unsafe_allow_html=True)

# Authentication instance
auth = Authentication()

# Main application flow
def main():
    # Sidebar navigation
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/library-building.png", width=100)
        st.markdown("## Navigation")
        
        if st.session_state.logged_in:
            st.success(f"Logged in as: {st.session_state.user_name}")
            st.info(f"Role: {st.session_state.user_role.capitalize()}")
            
            if st.button("Logout"):
                # Log the logout action
                file_handler.log_action(
                    st.session_state.user_id,
                    st.session_state.user_role,
                    "logout",
                    f"{st.session_state.user_name} logged out"
                )
                # Reset session state
                st.session_state.logged_in = False
                st.session_state.user_role = None
                st.session_state.user_id = None
                st.session_state.user_name = None
                st.rerun()
        else:
            page = st.radio("Select", ["Login", "Register"])
            
            if page == "Login":
                login_page = LoginPage(auth, file_handler)
                login_page.show()
            else:
                register_page = RegisterPage(auth, file_handler)
                register_page.show()
    
    # Main content based on login status and role
    if st.session_state.logged_in:
        if st.session_state.user_role == "admin":
            admin_dashboard = AdminDashboard(file_handler)
            admin_dashboard.show()
        elif st.session_state.user_role == "student":
            student_dashboard = StudentDashboard(file_handler)
            student_dashboard.show()
    else:
        # Welcome page for non-logged in users
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Welcome to the Library Management System")
        st.markdown("""
        This system allows you to:
        - Browse and search for books
        - Issue and return books
        - Manage student accounts
        - Track library activities
        
        Please login or register to continue.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display some sample books for preview
        try:
            books = file_handler.read_json_file('books.json')
            if books:
                st.markdown("<h3 class='sub-header'>📚 Featured Books</h3>", unsafe_allow_html=True)
                cols = st.columns(3)
                for i, book in enumerate(books[:6]):  # Show up to 6 books
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div class='card'>
                            <h4>{book['title']}</h4>
                            <p><strong>Author:</strong> {book['author']}</p>
                            <p><strong>Genre:</strong> {book['genre']}</p>
                            <p><strong>Status:</strong> {'Available' if book['available'] else 'Not Available'}</p>
                        </div>
                        """, unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not load sample books: {str(e)}")

if __name__ == "__main__":
    main()