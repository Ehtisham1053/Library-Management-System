import streamlit as st
import pandas as pd
from datetime import datetime

class StudentDashboard:
    def __init__(self, file_handler):
        self.file_handler = file_handler
    
    def show(self):
        st.markdown("<h2 class='sub-header'>Student Dashboard</h2>", unsafe_allow_html=True)
        
        # Check if student is flagged
        students = self.file_handler.read_json_file('students.json')
        current_student = next((s for s in students if s['id'] == st.session_state.user_id), None)
        
        if current_student and current_student.get('flagged', False):
            st.markdown("""
            <div class='warning-msg'>
                <strong>Warning:</strong> Your account has been flagged for late returns. 
                Please return any overdue books as soon as possible.
            </div>
            """, unsafe_allow_html=True)
        
        # Tabs for different student functions
        tabs = st.tabs(["Dashboard", "Browse Books", "My Books", "Book Requests", "My Requests"])
        
        # Dashboard Tab
        with tabs[0]:
            self._show_dashboard()
        
        # Browse Books Tab
        with tabs[1]:
            self._show_browse_books()
        
        # My Books Tab
        with tabs[2]:
            self._show_my_books()
        
        # Book Requests Tab
        with tabs[3]:
            self._show_book_requests()
            
        # My Requests Tab
        with tabs[4]:
            self._show_my_requests()
    
    def _show_dashboard(self):
        st.markdown("<h3>My Library Overview</h3>", unsafe_allow_html=True)
        
        # Get student's issued books
        issued_books = self.file_handler.read_json_file('issued_books.json')
        books = self.file_handler.read_json_file('books.json')
        
        # Filter for books issued to the current student
        my_issues = [
            issue for issue in issued_books 
            if issue['student_id'] == st.session_state.user_id
        ]
        
        current_issues = [issue for issue in my_issues if not issue.get('returned', False)]
        past_issues = [issue for issue in my_issues if issue.get('returned', False)]
        
        # Display stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='card'>
                <h4>Currently Borrowed</h4>
                <p class='text-4xl font-bold'>{len(current_issues)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='card'>
                <h4>Total Books Borrowed</h4>
                <p class='text-4xl font-bold'>{len(my_issues)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='card'>
                <h4>Books Returned</h4>
                <p class='text-4xl font-bold'>{len(past_issues)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Books due soon
        st.markdown("<h3>Books Due Soon</h3>", unsafe_allow_html=True)
        
        if current_issues:
            due_soon = []
            current_date = datetime.now()
            
            for issue in current_issues:
                book = next((b for b in books if b['id'] == issue['book_id']), None)
                
                if book:
                    due_date = datetime.strptime(issue['due_date'], "%Y-%m-%d %H:%M:%S")
                    days_left = (due_date - current_date).days
                    
                    due_soon.append({
                        "Book": book['title'],
                        "Author": book['author'],
                        "Due Date": issue['due_date'],
                        "Days Left": days_left,
                        "Status": "Overdue" if days_left < 0 else "Due Soon" if days_left <= 3 else "Active"
                    })
            
            if due_soon:
                due_soon_df = pd.DataFrame(due_soon)
                st.dataframe(due_soon_df, use_container_width=True)
            else:
                st.info("You don't have any books due soon")
        else:
            st.info("You don't have any borrowed books")
        
        # Recent activity
        st.markdown("<h3>Recent Activity</h3>", unsafe_allow_html=True)
        
        logs = self.file_handler.get_logs()
        
        # Filter logs for current student
        my_logs = logs[logs['user_id'] == st.session_state.user_id].tail(10)
        
        if not my_logs.empty:
            st.dataframe(my_logs, use_container_width=True)
        else:
            st.info("No recent activity")
    
    def _show_browse_books(self):
        st.markdown("<h3>Browse Books</h3>", unsafe_allow_html=True)
        
        books = self.file_handler.read_json_file('books.json')
        
        if not books:
            st.info("No books found in the library")
            return
        
        # Search and filter
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("Search by title or author")
        
        with col2:
            genre_filter = st.selectbox(
                "Filter by genre",
                ["All"] + sorted(list(set(book['genre'] for book in books)))
            )
        
        with col3:
            availability_filter = st.selectbox(
                "Availability",
                ["All", "Available", "Not Available"]
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
        
        if availability_filter == "Available":
            filtered_books = [book for book in filtered_books if book['available']]
        elif availability_filter == "Not Available":
            filtered_books = [book for book in filtered_books if not book['available']]
        
        # Display books
        if filtered_books:
            # Create a grid of book cards
            cols = st.columns(3)
            
            for i, book in enumerate(filtered_books):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class='card'>
                        <h4>{book['title']}</h4>
                        <p><strong>Author:</strong> {book['author']}</p>
                        <p><strong>Genre:</strong> {book['genre']}</p>
                        <p><strong>Total Copies:</strong> {book.get('total_copies', 1)}</p>
                        <p><strong>Available Copies:</strong> {book.get('available_copies', 1 if book['available'] else 0)}</p>
                        <p><strong>Status:</strong> {'Available' if book['available'] else 'Not Available'}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No books match your search criteria")
    
    def _show_my_books(self):
        st.markdown("<h3>My Books</h3>", unsafe_allow_html=True)
        
        # Get student's issued books
        issued_books = self.file_handler.read_json_file('issued_books.json')
        books = self.file_handler.read_json_file('books.json')
        
        # Filter for books issued to the current student
        my_issues = [
            issue for issue in issued_books 
            if issue['student_id'] == st.session_state.user_id
        ]
        
        if not my_issues:
            st.info("You haven't borrowed any books yet")
            return
        
        # Tabs for current and past books
        my_books_tabs = st.tabs(["Currently Borrowed", "Return History"])
        
        # Currently Borrowed Tab
        with my_books_tabs[0]:
            current_issues = [issue for issue in my_issues if not issue.get('returned', False)]
            
            if current_issues:
                current_data = []
                current_date = datetime.now()
                
                for issue in current_issues:
                    book = next((b for b in books if b['id'] == issue['book_id']), None)
                    
                    if book:
                        due_date = datetime.strptime(issue['due_date'], "%Y-%m-%d %H:%M:%S")
                        days_left = (due_date - current_date).days
                        
                        current_data.append({
                            "Issue ID": issue['id'],
                            "Book": book['title'],
                            "Author": book['author'],
                            "Genre": book['genre'],
                            "Issue Date": issue['issue_date'],
                            "Due Date": issue['due_date'],
                            "Days Left": days_left,
                            "Status": "Overdue" if days_left < 0 else "Due Soon" if days_left <= 3 else "Active",
                            "Return Requested": "Yes" if issue.get('return_requested', False) else "No"
                        })
                
                if current_data:
                    current_df = pd.DataFrame(current_data)
                    st.dataframe(current_df, use_container_width=True)
                    
                    # Return request section
                    st.markdown("<h4>Request Book Return</h4>", unsafe_allow_html=True)
                    
                    # Filter out books that already have return requests
                    available_for_return = [issue for issue in current_issues if not issue.get('return_requested', False)]
                    
                    if available_for_return:
                        issue_options = {
                            f"{next((b['title'] for b in books if b['id'] == issue['book_id']), 'Unknown')} ({issue['id']})": issue['id'] 
                            for issue in available_for_return
                        }
                        
                        selected_issue_name = st.selectbox("Select book to return", list(issue_options.keys()))
                        selected_issue_id = issue_options[selected_issue_name]
                        
                        if st.button("Request Return"):
                            success, message = self.file_handler.request_book_return(st.session_state.user_id, selected_issue_id)
                            
                            if success:
                                # Log the action
                                self.file_handler.log_action(
                                    st.session_state.user_id,
                                    st.session_state.user_role,
                                    "request_return",
                                    f"Requested return for book: {selected_issue_name.split(' (')[0]}"
                                )
                                
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                    else:
                        st.info("You have already requested returns for all your borrowed books")
            else:
                st.info("You don't have any books currently borrowed")
        
        # Return History Tab
        with my_books_tabs[1]:
            past_issues = [issue for issue in my_issues if issue.get('returned', False)]
            
            if past_issues:
                past_data = []
                
                for issue in past_issues:
                    book = next((b for b in books if b['id'] == issue['book_id']), None)
                    
                    if book:
                        issue_date = datetime.strptime(issue['issue_date'], "%Y-%m-%d %H:%M:%S")
                        due_date = datetime.strptime(issue['due_date'], "%Y-%m-%d %H:%M:%S")
                        return_date = datetime.strptime(issue['return_date'], "%Y-%m-%d %H:%M:%S")
                        
                        # Check if return was late
                        was_late = return_date > due_date
                        
                        past_data.append({
                            "Book": book['title'],
                            "Author": book['author'],
                            "Genre": book['genre'],
                            "Issue Date": issue['issue_date'],
                            "Due Date": issue['due_date'],
                            "Return Date": issue['return_date'],
                            "Status": "Late Return" if was_late else "On Time"
                        })
                
                if past_data:
                    past_df = pd.DataFrame(past_data)
                    st.dataframe(past_df, use_container_width=True)
            else:
                st.info("You don't have any return history")
    
    def _show_book_requests(self):
        st.markdown("<h3>Book Requests</h3>", unsafe_allow_html=True)
        
        # Check if student is approved
        students = self.file_handler.read_json_file('students.json')
        current_student = next((s for s in students if s['id'] == st.session_state.user_id), None)
        
        if not current_student or not current_student.get('approved', False):
            st.warning("Your account needs to be approved by the admin before you can request books")
            return
        
        # Get available books
        books = self.file_handler.read_json_file('books.json')
        available_books = [book for book in books if book.get('available_copies', 0) > 0]

        
        if not available_books:
            st.warning("No books are currently available for request")
            return
        
        # Book request form
        st.markdown("<h4>Request a Book</h4>", unsafe_allow_html=True)
        
        book_options = {f"{book['title']} by {book['author']}": book['id'] for book in available_books}
        selected_book_name = st.selectbox("Select Book", list(book_options.keys()))
        selected_book_id = book_options[selected_book_name]
        
        # Get selected book details
        selected_book = next((book for book in books if book['id'] == selected_book_id), None)
        
        if selected_book:
            st.markdown(f"""
            <div class='card'>
                <h4>{selected_book['title']}</h4>
                <p><strong>Author:</strong> {selected_book['author']}</p>
                <p><strong>Genre:</strong> {selected_book['genre']}</p>
                <p><strong>Available Copies:</strong> {selected_book.get('available_copies', 1)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Request Book"):
                success, message = self.file_handler.request_book_issue(st.session_state.user_id, selected_book_id)
                
                if success:
                    # Log the action
                    self.file_handler.log_action(
                        st.session_state.user_id,
                        st.session_state.user_role,
                        "request_book",
                        f"Requested book: {selected_book['title']}"
                    )
                    
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    def _show_my_requests(self):
        st.markdown("<h3>My Pending Requests</h3>", unsafe_allow_html=True)
        
        requests = self.file_handler.read_json_file('requests.json')
        books = self.file_handler.read_json_file('books.json')
        
        # Filter for this student's pending requests
        my_requests = [
            req for req in requests 
            if req['student_id'] == st.session_state.user_id and req['status'] == "pending"
        ]
        
        if not my_requests:
            st.info("You don't have any pending requests")
            return
        
        # Display pending requests
        request_data = []
        
        for req in my_requests:
            book = next((b for b in books if b['id'] == req['book_id']), None)
            
            if book:
                request_data.append({
                    "Request ID": req['id'],
                    "Type": req['type'].capitalize(),
                    "Book": book['title'],
                    "Requested At": req['requested_at']
                })
        
        if request_data:
            request_df = pd.DataFrame(request_data)
            st.dataframe(request_df, use_container_width=True)
            st.info("Your requests are pending admin approval. Please check back later.")