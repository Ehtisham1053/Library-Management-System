import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

class AdminDashboard:
    def __init__(self, file_handler):
        self.file_handler = file_handler
    




    def show(self):
        st.markdown("<h2 class='sub-header'>Admin Dashboard</h2>", unsafe_allow_html=True)
        
        # Tabs for different admin functions
        tabs = st.tabs(["Dashboard", "Books", "Students", "Issue/Return", "Pending Requests", "Logs"])
        
        # Dashboard Tab
        with tabs[0]:
            self._show_dashboard()
        
        # Books Tab
        with tabs[1]:
            self._show_books_management()
        
        # Students Tab
        with tabs[2]:
            self._show_students_management()
        
        # Issue/Return Tab
        with tabs[3]:
            self._show_issue_return()
        
        # Pending Requests Tab
        with tabs[4]:
            self._show_pending_requests()
        
        # Logs Tab
        with tabs[5]:
            self._show_logs()
















    
    def _show_dashboard(self):
        st.markdown("<h3>Library Overview</h3>", unsafe_allow_html=True)
        
        # Get analytics
        analytics = self.file_handler.get_analytics()
        
        if not analytics:
            st.error("Could not load analytics data")
            return
        
        # Display analytics in cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='card'>
                <h4>Books</h4>
                <p><strong>Total:</strong> {analytics['total_books']}</p>
                <p><strong>Available:</strong> {analytics['available_books']}</p>
                <p><strong>Issued:</strong> {analytics['issued_books']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='card'>
                <h4>Students</h4>
                <p><strong>Total:</strong> {analytics['total_students']}</p>
                <p><strong>Approved:</strong> {analytics['approved_students']}</p>
                <p><strong>Pending:</strong> {analytics['pending_students']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='card'>
                <h4>Status</h4>
                <p><strong>Currently Issued:</strong> {analytics['currently_issued']}</p>
                <p><strong>Flagged Students:</strong> {analytics['flagged_students']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Recent activity
        st.markdown("<h3>Recent Activity</h3>", unsafe_allow_html=True)
        
        logs = self.file_handler.get_logs(limit=10)
        
        if not logs.empty:
            st.dataframe(logs, use_container_width=True)
        else:
            st.info("No recent activity")
        
        # Books due soon
        st.markdown("<h3>Books Due Soon</h3>", unsafe_allow_html=True)
        
        issued_books = self.file_handler.read_json_file('issued_books.json')
        books = self.file_handler.read_json_file('books.json')
        students = self.file_handler.read_json_file('students.json')
        
        # Filter for books that are not returned and due within 3 days
        current_date = datetime.now()
        due_soon = []
        
        for issue in issued_books:
            if not issue.get('returned', False):
                due_date = datetime.strptime(issue['due_date'], "%Y-%m-%d %H:%M:%S")
                days_left = (due_date - current_date).days
                
                if days_left <= 3:
                    # Get book and student details
                    book = next((b for b in books if b['id'] == issue['book_id']), None)
                    student = next((s for s in students if s['id'] == issue['student_id']), None)
                    
                    if book and student:
                        due_soon.append({
                            "Issue ID": issue['id'],
                            "Book": book['title'],
                            "Student": student['name'],
                            "Due Date": issue['due_date'],
                            "Days Left": days_left
                        })
        
        if due_soon:
            due_soon_df = pd.DataFrame(due_soon)
            st.dataframe(due_soon_df, use_container_width=True)
        else:
            st.info("No books due soon")

















    
    def _show_books_management(self):
        st.markdown("<h3>Books Management</h3>", unsafe_allow_html=True)
        
        # Tabs for different book operations
        book_tabs = st.tabs(["All Books", "Add Book", "Edit Book", "Delete Book"])
        
        # All Books Tab
        with book_tabs[0]:
            self._show_all_books()
        
        # Add Book Tab
        with book_tabs[1]:
            self._show_add_book()
        
        # Edit Book Tab
        with book_tabs[2]:
            self._show_edit_book()
        
        # Delete Book Tab
        with book_tabs[3]:
            self._show_delete_book()
    





    def _show_all_books(self):
        st.markdown("<h4>All Books</h4>", unsafe_allow_html=True)
        
        books = self.file_handler.read_json_file('books.json')
        
        if not books:
            st.info("No books found")
            return
        
        # Search and filter
        search_col, filter_col = st.columns(2)
        
        with search_col:
            search_term = st.text_input("Search by title or author")
        
        with filter_col:
            genre_filter = st.selectbox(
                "Filter by genre",
                ["All"] + sorted(list(set(book['genre'] for book in books)))
            )
        
        # Apply filters
        filtered_books = books
        
        if search_term:
            filtered_books = [
                book for book in filtered_books
                if search_term.lower() in book['title'].lower() or search_term.lower() in book['author'].lower()
            ]
        
        if genre_filter != "All":
            filtered_books = [book for book in filtered_books if book['genre'] == genre_filter]
        
        # Display books
        if filtered_books:
            books_data = []
            
            for book in filtered_books:
                books_data.append({
                    "ID": book['id'],
                    "Title": book['title'],
                    "Author": book['author'],
                    "Genre": book['genre'],
                    "Total Copies": book.get('total_copies', 1),
                    "Available Copies": book.get('available_copies', 1 if book['available'] else 0),
                    "Status": "Available" if book['available'] else "Not Available",
                    "Added On": book['added_at']
                })
            
            books_df = pd.DataFrame(books_data)
            st.dataframe(books_df, use_container_width=True)
        else:
            st.info("No books match your search criteria")
    

















    def _show_add_book(self):
        st.markdown("<h4>Add New Book</h4>", unsafe_allow_html=True)
        
        with st.form("add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            genre = st.text_input("Genre")
            copies = st.number_input("Number of Copies", min_value=1, value=1)
            
            submit_button = st.form_submit_button("Add Book")
            
            if submit_button:
                if not title or not author or not genre:
                    st.error("Please fill in all fields")
                else:
                    success, result = self.file_handler.add_book(title, author, genre, copies)
                    
                    if success:
                        # Log the action
                        self.file_handler.log_action(
                            st.session_state.user_id,
                            st.session_state.user_role,
                            "add_book",
                            f"Added book: {title} by {author} ({copies} copies)"
                        )
                        
                        st.success(f"Book added successfully with ID: {result}")
                    else:
                        st.error(result)




    def _show_edit_book(self):
        st.markdown("<h4>Edit Book</h4>", unsafe_allow_html=True)
        
        books = self.file_handler.read_json_file('books.json')
        
        if not books:
            st.info("No books found")
            return
        
        # Book selection
        book_options = {f"{book['title']} ({book['id']})": book['id'] for book in books}
        selected_book_name = st.selectbox("Select Book", list(book_options.keys()))
        selected_book_id = book_options[selected_book_name]
        
        # Get selected book details
        selected_book = next((book for book in books if book['id'] == selected_book_id), None)
        
        if selected_book:
            with st.form("edit_book_form"):
                title = st.text_input("Title", value=selected_book['title'])
                author = st.text_input("Author", value=selected_book['author'])
                genre = st.text_input("Genre", value=selected_book['genre'])
                total_copies = st.number_input("Total Copies", min_value=1, value=selected_book.get('total_copies', 1))
                available_copies = st.number_input("Available Copies", min_value=0, max_value=total_copies, value=selected_book.get('available_copies', 1 if selected_book['available'] else 0))
                
                submit_button = st.form_submit_button("Update Book")
                
                if submit_button:
                    if not title or not author or not genre:
                        st.error("Please fill in all fields")
                    else:
                        success, message = self.file_handler.update_book(
                            selected_book_id, title, author, genre, total_copies, available_copies
                        )
                        
                        if success:
                            # Log the action
                            self.file_handler.log_action(
                                st.session_state.user_id,
                                st.session_state.user_role,
                                "update_book",
                                f"Updated book: {title} ({selected_book_id})"
                            )
                            
                            st.success(message)
                        else:
                            st.error(message)


    
    






    def _show_delete_book(self):
        st.markdown("<h4>Delete Book</h4>", unsafe_allow_html=True)
        
        books = self.file_handler.read_json_file('books.json')
        
        if not books:
            st.info("No books found")
            return
        
        # Book selection
        book_options = {f"{book['title']} ({book['id']})": book['id'] for book in books}
        selected_book_name = st.selectbox("Select Book to Delete", list(book_options.keys()))
        selected_book_id = book_options[selected_book_name]
        
        # Get selected book details
        selected_book = next((book for book in books if book['id'] == selected_book_id), None)
        
        if selected_book:
            st.markdown(f"""
            <div class='card'>
                <h4>{selected_book['title']}</h4>
                <p><strong>Author:</strong> {selected_book['author']}</p>
                <p><strong>Genre:</strong> {selected_book['genre']}</p>
                <p><strong>Status:</strong> {'Available' if selected_book['available'] else 'Issued'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if not selected_book['available']:
                st.warning("This book is currently issued and cannot be deleted")
            else:
                confirm = st.checkbox("I confirm that I want to delete this book")
                
                if confirm:
                    if st.button("Delete Book"):
                        success, message = self.file_handler.delete_book(selected_book_id)
                        
                        if success:
                            # Log the action
                            self.file_handler.log_action(
                                st.session_state.user_id,
                                st.session_state.user_role,
                                "delete_book",
                                f"Deleted book: {selected_book['title']} ({selected_book_id})"
                            )
                            
                            st.success(message)
                        else:
                            st.error(message)
    
    def _show_students_management(self):
        st.markdown("<h3>Students Management</h3>", unsafe_allow_html=True)
        
        # Tabs for different student operations
        student_tabs = st.tabs(["All Students", "Pending Approvals", "Flagged Students"])
        
        # All Students Tab
        with student_tabs[0]:
            self._show_all_students()
        
        # Pending Approvals Tab
        with student_tabs[1]:
            self._show_pending_students()
        
        # Flagged Students Tab
        with student_tabs[2]:
            self._show_flagged_students()
    
    def _show_all_students(self):
        st.markdown("<h4>All Students</h4>", unsafe_allow_html=True)
        
        students = self.file_handler.read_json_file('students.json')
        
        if not students:
            st.info("No students found")
            return
        
        # Search
        search_term = st.text_input("Search by name or email", key="search_all_students")
        
        # Apply filter
        filtered_students = students
        
        if search_term:
            filtered_students = [
                student for student in filtered_students
                if search_term.lower() in student['name'].lower() or search_term.lower() in student['email'].lower()
            ]
        
        # Display students
        if filtered_students:
            students_data = []
            
            for student in filtered_students:
                students_data.append({
                    "ID": student['id'],
                    "Name": student['name'],
                    "Email": student['email'],
                    "Status": "Approved" if student.get('approved', False) else "Pending",
                    "Flagged": "Yes" if student.get('flagged', False) else "No",
                    "Registered On": student['created_at']
                })
            
            students_df = pd.DataFrame(students_data)
            st.dataframe(students_df, use_container_width=True)
            
            # Student actions
            st.markdown("<h4>Student Actions</h4>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                student_options = {f"{student['name']} ({student['id']})": student['id'] for student in filtered_students}
                selected_student_name = st.selectbox("Select Student", list(student_options.keys()))
                selected_student_id = student_options[selected_student_name]
            
            with col2:
                action = st.selectbox("Action", ["Approve", "Block", "Flag", "Unflag"])
            
            # Get selected student details
            selected_student = next((student for student in students if student['id'] == selected_student_id), None)
            
            if selected_student:
                st.markdown(f"""
                <div class='card'>
                    <h4>{selected_student['name']}</h4>
                    <p><strong>Email:</strong> {selected_student['email']}</p>
                    <p><strong>Status:</strong> {'Approved' if selected_student.get('approved', False) else 'Pending'}</p>
                    <p><strong>Flagged:</strong> {'Yes' if selected_student.get('flagged', False) else 'No'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Perform Action"):
                    if action == "Approve":
                        success, message = self.file_handler.approve_student(selected_student_id)
                    elif action == "Block":
                        success, message = self.file_handler.block_student(selected_student_id)
                    elif action == "Flag":
                        success, message = self.file_handler.flag_student(selected_student_id, True)
                    elif action == "Unflag":
                        success, message = self.file_handler.flag_student(selected_student_id, False)
                    
                    if success:
                        # Log the action
                        self.file_handler.log_action(
                            st.session_state.user_id,
                            st.session_state.user_role,
                            f"student_{action.lower()}",
                            f"{action}ed student: {selected_student['name']} ({selected_student_id})"
                        )
                        
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.info("No students match your search criteria")





    def _show_pending_requests(self):
        st.markdown("<h3>Pending Requests</h3>", unsafe_allow_html=True)
        
        requests = self.file_handler.read_json_file('requests.json')
        books = self.file_handler.read_json_file('books.json')
        students = self.file_handler.read_json_file('students.json')
        
        # Filter for pending requests
        pending_requests = [req for req in requests if req['status'] == "pending"]
        
        if not pending_requests:
            st.info("No pending requests")
            return
        
        # Tabs for different request types
        request_tabs = st.tabs(["Issue Requests", "Return Requests"])
        
        # Issue Requests Tab
        with request_tabs[0]:
            issue_requests = [req for req in pending_requests if req['type'] == "issue"]
            
            if not issue_requests:
                st.info("No pending issue requests")
            else:
                request_data = []
                
                for req in issue_requests:
                    book = next((b for b in books if b['id'] == req['book_id']), None)
                    student = next((s for s in students if s['id'] == req['student_id']), None)
                    
                    if book and student:
                        request_data.append({
                            "Request ID": req['id'],
                            "Student": student['name'],
                            "Book": book['title'],
                            "Requested At": req['requested_at']
                        })
                
                if request_data:
                    st.dataframe(pd.DataFrame(request_data), use_container_width=True)
                    
                    # Request approval
                    request_options = {
                        f"{req['id']} - {next((b['title'] for b in books if b['id'] == req['book_id']), 'Unknown')} by {next((s['name'] for s in students if s['id'] == req['student_id']), 'Unknown')}": req['id'] 
                        for req in issue_requests
                    }
                    
                    selected_request_name = st.selectbox("Select issue request to approve", list(request_options.keys()))
                    selected_request_id = request_options[selected_request_name]
                    
                    if st.button("Approve Issue Request"):
                        success, message = self.file_handler.approve_book_request(selected_request_id)
                        
                        if success:
                            # Log the action
                            self.file_handler.log_action(
                                st.session_state.user_id,
                                st.session_state.user_role,
                                "approve_issue_request",
                                f"Approved issue request: {selected_request_name}"
                            )
                            
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        
        # Return Requests Tab
        with request_tabs[1]:
            return_requests = [req for req in pending_requests if req['type'] == "return"]
            
            if not return_requests:
                st.info("No pending return requests")
            else:
                request_data = []
                
                for req in return_requests:
                    book = next((b for b in books if b['id'] == req['book_id']), None)
                    student = next((s for s in students if s['id'] == req['student_id']), None)
                    
                    if book and student:
                        request_data.append({
                            "Request ID": req['id'],
                            "Student": student['name'],
                            "Book": book['title'],
                            "Issue ID": req['issue_id'],
                            "Requested At": req['requested_at']
                        })
                
                if request_data:
                    st.dataframe(pd.DataFrame(request_data), use_container_width=True)
                    
                    # Request approval
                    request_options = {
                        f"{req['id']} - {next((b['title'] for b in books if b['id'] == req['book_id']), 'Unknown')} by {next((s['name'] for s in students if s['id'] == req['student_id']), 'Unknown')}": req['id'] 
                        for req in return_requests
                    }
                    
                    selected_request_name = st.selectbox("Select return request to approve", list(request_options.keys()))
                    selected_request_id = request_options[selected_request_name]
                    
                    if st.button("Approve Return Request"):
                        success, message = self.file_handler.approve_book_request(selected_request_id)
                        
                        if success:
                            # Log the action
                            self.file_handler.log_action(
                                st.session_state.user_id,
                                st.session_state.user_role,
                                "approve_return_request",
                                f"Approved return request: {selected_request_name}"
                            )
                            
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)








    
    def _show_pending_students(self):
        st.markdown("<h4>Pending Approvals</h4>", unsafe_allow_html=True)
        
        students = self.file_handler.read_json_file('students.json')
        
        # Filter for pending students
        pending_students = [student for student in students if not student.get('approved', False)]
        
        if not pending_students:
            st.info("No pending student approvals")
            return
        
        # Display pending students
        students_data = []
        
        for student in pending_students:
            students_data.append({
                "ID": student['id'],
                "Name": student['name'],
                "Email": student['email'],
                "Registered On": student['created_at']
            })
        
        students_df = pd.DataFrame(students_data)
        st.dataframe(students_df, use_container_width=True)
        
        # Approval actions
        st.markdown("<h4>Approve Students</h4>", unsafe_allow_html=True)
        
        student_options = {f"{student['name']} ({student['id']})": student['id'] for student in pending_students}
        selected_student_name = st.selectbox("Select Student to Approve", list(student_options.keys()))
        selected_student_id = student_options[selected_student_name]
        
        if st.button("Approve Selected Student"):
            success, message = self.file_handler.approve_student(selected_student_id)
            
            if success:
                # Log the action
                selected_student = next((student for student in students if student['id'] == selected_student_id), None)
                
                self.file_handler.log_action(
                    st.session_state.user_id,
                    st.session_state.user_role,
                    "student_approve",
                    f"Approved student: {selected_student['name']} ({selected_student_id})"
                )
                
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    def _show_flagged_students(self):
        st.markdown("<h4>Flagged Students</h4>", unsafe_allow_html=True)
        
        students = self.file_handler.read_json_file('students.json')
        
        # Filter for flagged students
        flagged_students = [student for student in students if student.get('flagged', False)]
        
        if not flagged_students:
            st.info("No flagged students")
            return
        
        # Display flagged students
        students_data = []
        
        for student in flagged_students:
            students_data.append({
                "ID": student['id'],
                "Name": student['name'],
                "Email": student['email'],
                "Status": "Approved" if student.get('approved', False) else "Pending"
            })
        
        students_df = pd.DataFrame(students_data)
        st.dataframe(students_df, use_container_width=True)
        
        # Unflag actions
        st.markdown("<h4>Unflag Students</h4>", unsafe_allow_html=True)
        
        student_options = {f"{student['name']} ({student['id']})": student['id'] for student in flagged_students}
        selected_student_name = st.selectbox("Select Student to Unflag", list(student_options.keys()))
        selected_student_id = student_options[selected_student_name]
        
        if st.button("Unflag Selected Student"):
            success, message = self.file_handler.flag_student(selected_student_id, False)
            
            if success:
                # Log the action
                selected_student = next((student for student in students if student['id'] == selected_student_id), None)
                
                self.file_handler.log_action(
                    st.session_state.user_id,
                    st.session_state.user_role,
                    "student_unflag",
                    f"Unflagged student: {selected_student['name']} ({selected_student_id})"
                )
                
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    def _show_issue_return(self):
        st.markdown("<h3>Issue and Return Books</h3>", unsafe_allow_html=True)
        
        # Tabs for issue and return
        issue_return_tabs = st.tabs(["Issue Book", "Return Book", "Currently Issued"])
        
        # Issue Book Tab
        with issue_return_tabs[0]:
            self._show_issue_book()
        
        # Return Book Tab
        with issue_return_tabs[1]:
            self._show_return_book()
        
        # Currently Issued Tab
        with issue_return_tabs[2]:
            self._show_currently_issued()
    
    def _show_issue_book(self):
        st.markdown("<h4>Issue Book to Student</h4>", unsafe_allow_html=True)
        
        books = self.file_handler.read_json_file('books.json')
        students = self.file_handler.read_json_file('students.json')
        
        # Filter for available books and approved students
        available_books = [book for book in books if book['available']]
        approved_students = [student for student in students if student.get('approved', False)]
        
        if not available_books:
            st.warning("No books available for issue")
            return
        
        if not approved_students:
            st.warning("No approved students found")
            return
        
        # Book and student selection
        col1, col2 = st.columns(2)
        
        with col1:
            book_options = {f"{book['title']} ({book['id']})": book['id'] for book in available_books}
            selected_book_name = st.selectbox("Select Book", list(book_options.keys()))
            selected_book_id = book_options[selected_book_name]
        
        with col2:
            student_options = {f"{student['name']} ({student['id']})": student['id'] for student in approved_students}
            selected_student_name = st.selectbox(
                "Select Student",
                list(student_options.keys()),
                key="selectbox_issue_student"
            )
            selected_student_id = student_options[selected_student_name]

        
        # Get selected book and student details
        selected_book = next((book for book in books if book['id'] == selected_book_id), None)
        selected_student = next((student for student in students if student['id'] == selected_student_id), None)
        
        if selected_book and selected_student:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class='card'>
                    <h4>{selected_book['title']}</h4>
                    <p><strong>Author:</strong> {selected_book['author']}</p>
                    <p><strong>Genre:</strong> {selected_book['genre']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='card'>
                    <h4>{selected_student['name']}</h4>
                    <p><strong>Email:</strong> {selected_student['email']}</p>
                    <p><strong>Flagged:</strong> {'Yes' if selected_student.get('flagged', False) else 'No'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if selected_student.get('flagged', False):
                    st.warning("This student is flagged for late returns")
            
            # Issue duration
            days = st.slider("Issue Duration (Days)", min_value=1, max_value=30, value=7)
            
            if st.button("Issue Book"):
                success, message = self.file_handler.issue_book(selected_student_id, selected_book_id, days)
                
                if success:
                    # Log the action
                    self.file_handler.log_action(
                        st.session_state.user_id,
                        st.session_state.user_role,
                        "issue_book",
                        f"Issued book: {selected_book['title']} to {selected_student['name']} for {days} days"
                    )
                    
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    def _show_return_book(self):
        st.markdown("<h4>Return Book</h4>", unsafe_allow_html=True)
        
        issued_books = self.file_handler.read_json_file('issued_books.json')
        books = self.file_handler.read_json_file('books.json')
        students = self.file_handler.read_json_file('students.json')
        
        # Filter for books that are currently issued
        current_issues = [issue for issue in issued_books if not issue.get('returned', False)]
        
        if not current_issues:
            st.warning("No books are currently issued")
            return
        
        # Create issue options
        issue_options = {}
        
        for issue in current_issues:
            book = next((b for b in books if b['id'] == issue['book_id']), None)
            student = next((s for s in students if s['id'] == issue['student_id']), None)
            
            if book and student:
                issue_options[f"{book['title']} - {student['name']} ({issue['id']})"] = issue['id']
        
        # Issue selection
        selected_issue_name = st.selectbox("Select Book to Return", list(issue_options.keys()))
        selected_issue_id = issue_options[selected_issue_name]
        
        # Get selected issue details
        selected_issue = next((issue for issue in issued_books if issue['id'] == selected_issue_id), None)
        
        if selected_issue:
            book = next((b for b in books if b['id'] == selected_issue['book_id']), None)
            student = next((s for s in students if s['id'] == selected_issue['student_id']), None)
            
            if book and student:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class='card'>
                        <h4>{book['title']}</h4>
                        <p><strong>Author:</strong> {book['author']}</p>
                        <p><strong>Genre:</strong> {book['genre']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class='card'>
                        <h4>{student['name']}</h4>
                        <p><strong>Email:</strong> {student['email']}</p>
                        <p><strong>Issue Date:</strong> {selected_issue['issue_date']}</p>
                        <p><strong>Due Date:</strong> {selected_issue['due_date']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Check if return is late
                current_date = datetime.now()
                due_date = datetime.strptime(selected_issue['due_date'], "%Y-%m-%d %H:%M:%S")
                
                if current_date > due_date:
                    st.warning("This book is being returned late. The student will be flagged.")
                
                if st.button("Return Book"):
                    success, message = self.file_handler.return_book(selected_issue_id)
                    
                    if success:
                        # Log the action
                        self.file_handler.log_action(
                            st.session_state.user_id,
                            st.session_state.user_role,
                            "return_book",
                            f"Returned book: {book['title']} from {student['name']}"
                        )
                        
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    
    def _show_currently_issued(self):
        st.markdown("<h4>Currently Issued Books</h4>", unsafe_allow_html=True)
        
        issued_books = self.file_handler.read_json_file('issued_books.json')
        books = self.file_handler.read_json_file('books.json')
        students = self.file_handler.read_json_file('students.json')
        
        # Filter for books that are currently issued
        current_issues = [issue for issue in issued_books if not issue.get('returned', False)]
        
        if not current_issues:
            st.info("No books are currently issued")
            return
        
        # Display currently issued books
        issued_data = []
        
        for issue in current_issues:
            book = next((b for b in books if b['id'] == issue['book_id']), None)
            student = next((s for s in students if s['id'] == issue['student_id']), None)
            
            if book and student:
                # Calculate days left
                current_date = datetime.now()
                due_date = datetime.strptime(issue['due_date'], "%Y-%m-%d %H:%M:%S")
                days_left = (due_date - current_date).days
                
                issued_data.append({
                    "Issue ID": issue['id'],
                    "Book": book['title'],
                    "Student": student['name'],
                    "Issue Date": issue['issue_date'],
                    "Due Date": issue['due_date'],
                    "Days Left": days_left,
                    "Status": "Overdue" if days_left < 0 else "Active"
                })
        
        if issued_data:
            issued_df = pd.DataFrame(issued_data)
            st.dataframe(issued_df, use_container_width=True)
    
    def _show_logs(self):
        st.markdown("<h3>System Logs</h3>", unsafe_allow_html=True)
        
        # Get logs
        logs = self.file_handler.get_logs()
        
        if logs.empty:
            st.info("No logs found")
            return
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            action_filter = st.selectbox(
                "Filter by action",
                ["All"] + sorted(list(set(logs['action'])))
            )
        
        with col2:
            role_filter = st.selectbox(
                "Filter by role",
                ["All"] + sorted(list(set(logs['user_role'])))
            )
        
        # Apply filters
        filtered_logs = logs
        
        if action_filter != "All":
            filtered_logs = filtered_logs[filtered_logs['action'] == action_filter]
        
        if role_filter != "All":
            filtered_logs = filtered_logs[filtered_logs['user_role'] == role_filter]
        
        # Display logs
        if not filtered_logs.empty:
            st.dataframe(filtered_logs, use_container_width=True)
        else:
            st.info("No logs match your filter criteria")