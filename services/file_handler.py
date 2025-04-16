import json
import os
import csv
import pandas as pd
from datetime import datetime, timedelta
import traceback

class FileHandler:
    def __init__(self):
        self.data_dir = 'data'
        self.students_file = os.path.join(self.data_dir, 'students.json')
        self.books_file = os.path.join(self.data_dir, 'books.json')
        self.issued_books_file = os.path.join(self.data_dir, 'issued_books.json')
        self.logs_file = os.path.join(self.data_dir, 'logs.csv')
        self.requests_file = os.path.join(self.data_dir, 'requests.json')
        self.admin_file = os.path.join(self.data_dir, 'admin.json')
        
        # Ensure data integrity on initialization
        self.ensure_data_integrity()
    
    def ensure_data_integrity(self):
        """Ensure all data files have consistent structure"""
        if os.path.exists(self.books_file):
            try:
                books = self.read_json_file('books.json')
                updated = False
                
                for book in books:
                    # Ensure all books have total_copies and available_copies fields
                    if 'total_copies' not in book:
                        book['total_copies'] = 1
                        updated = True
                    
                    if 'available_copies' not in book:
                        # If book is available, set available_copies to 1 or total_copies
                        if book.get('available', True):
                            book['available_copies'] = book.get('total_copies', 1)
                        else:
                            book['available_copies'] = 0
                        updated = True
                
                if updated:
                    self.write_json_file('books.json', books)
                    print("Book data integrity fixed - added missing fields")
            except Exception as e:
                print(f"Error ensuring data integrity: {str(e)}")
    
    def initialize_data_files(self):
        """Initialize all data files with default structure if they don't exist"""
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Initialize students.json
        if not os.path.exists(self.students_file):
            self._create_file_with_data(self.students_file, self._get_mock_students())
        
        # Initialize books.json
        if not os.path.exists(self.books_file):
            self._create_file_with_data(self.books_file, self._get_mock_books())
        
        # Initialize issued_books.json
        if not os.path.exists(self.issued_books_file):
            self._create_file_with_data(self.issued_books_file, [])
        
        # Initialize requests.json
        if not os.path.exists(self.requests_file):
            self._create_file_with_data(self.requests_file, [])
        
        # Initialize logs.csv
        if not os.path.exists(self.logs_file):
            self._create_logs_file()
        
        # Ensure data integrity after initialization
        self.ensure_data_integrity()
    
    def _create_file_with_data(self, file_path, data):
        """Create a JSON file with the given data"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error creating {file_path}: {str(e)}")
    
    def _create_logs_file(self):
        """Create the logs CSV file with headers"""
        try:
            with open(self.logs_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'user_id', 'user_role', 'action', 'details'])
        except Exception as e:
            print(f"Error creating logs file: {str(e)}")
    
    def _get_mock_students(self):
        """Generate mock student data"""
        return [
            {
                "id": "STU-A1B2C3",
                "name": "John Doe",
                "email": "john@example.com",
                "password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",  # 123456
                "role": "student",
                "approved": True,
                "flagged": False,
                "created_at": "2023-01-01 10:00:00"
            },
            {
                "id": "STU-D4E5F6",
                "name": "Jane Smith",
                "email": "jane@example.com",
                "password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",  # 123456
                "role": "student",
                "approved": True,
                "flagged": False,
                "created_at": "2023-01-02 11:00:00"
            },
            {
                "id": "STU-G7H8I9",
                "name": "Bob Johnson",
                "email": "bob@example.com",
                "password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",  # 123456
                "role": "student",
                "approved": True,
                "flagged": True,
                "created_at": "2023-01-03 12:00:00"
            },
            {
                "id": "STU-J1K2L3",
                "name": "Alice Brown",
                "email": "alice@example.com",
                "password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",  # 123456
                "role": "student",
                "approved": False,
                "flagged": False,
                "created_at": "2023-01-04 13:00:00"
            },
            {
                "id": "STU-M4N5O6",
                "name": "Charlie Wilson",
                "email": "charlie@example.com",
                "password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",  # 123456
                "role": "student",
                "approved": True,
                "flagged": True,
                "created_at": "2023-01-05 14:00:00"
            }
        ]
    
    def _get_mock_books(self):
        """Generate mock book data with multiple copies"""
        return [
            {
                "id": "BK-001",
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "genre": "Fiction",
                "available": True,
                "total_copies": 3,
                "available_copies": 3,
                "added_at": "2023-01-01 10:00:00"
            },
            {
                "id": "BK-002",
                "title": "1984",
                "author": "George Orwell",
                "genre": "Science Fiction",
                "available": True,
                "total_copies": 2,
                "available_copies": 2,
                "added_at": "2023-01-01 10:05:00"
            },
            {
                "id": "BK-003",
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "genre": "Fiction",
                "available": False,
                "total_copies": 1,
                "available_copies": 0,
                "added_at": "2023-01-01 10:10:00"
            },
            {
                "id": "BK-004",
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "genre": "Romance",
                "available": True,
                "total_copies": 2,
                "available_copies": 2,
                "added_at": "2023-01-01 10:15:00"
            },
            {
                "id": "BK-005",
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "genre": "Fantasy",
                "available": True,
                "total_copies": 3,
                "available_copies": 3,
                "added_at": "2023-01-01 10:20:00"
            },
            {
                "id": "BK-006",
                "title": "Harry Potter and the Philosopher's Stone",
                "author": "J.K. Rowling",
                "genre": "Fantasy",
                "available": False,
                "total_copies": 4,
                "available_copies": 0,
                "added_at": "2023-01-01 10:25:00"
            },
            {
                "id": "BK-007",
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "genre": "Fiction",
                "available": True,
                "total_copies": 2,
                "available_copies": 2,
                "added_at": "2023-01-01 10:30:00"
            },
            {
                "id": "BK-008",
                "title": "The Lord of the Rings",
                "author": "J.R.R. Tolkien",
                "genre": "Fantasy",
                "available": True,
                "total_copies": 3,
                "available_copies": 3,
                "added_at": "2023-01-01 10:35:00"
            },
            {
                "id": "BK-009",
                "title": "Brave New World",
                "author": "Aldous Huxley",
                "genre": "Science Fiction",
                "available": True,
                "total_copies": 2,
                "available_copies": 2,
                "added_at": "2023-01-01 10:40:00"
            },
            {
                "id": "BK-010",
                "title": "The Alchemist",
                "author": "Paulo Coelho",
                "genre": "Fiction",
                "available": True,
                "total_copies": 3,
                "available_copies": 3,
                "added_at": "2023-01-01 10:45:00"
            }
        ]
    
    def read_json_file(self, file_name):
        """Read and return data from a JSON file"""
        try:
            file_path = os.path.join(self.data_dir, file_name)
            if not os.path.exists(file_path):
                return []
            
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading {file_name}: {str(e)}")
            return []
    
    def write_json_file(self, file_name, data):
        """Write data to a JSON file"""
        try:
            file_path = os.path.join(self.data_dir, file_name)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error writing to {file_name}: {str(e)}")
            return False
    
    def log_action(self, user_id, user_role, action, details):
        """Log an action to the logs.csv file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.logs_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, user_id, user_role, action, details])
            return True
        except Exception as e:
            print(f"Error logging action: {str(e)}")
            return False
    
    def get_logs(self, limit=None):
        """Get logs from the logs.csv file"""
        try:
            if not os.path.exists(self.logs_file):
                return pd.DataFrame(columns=['timestamp', 'user_id', 'user_role', 'action', 'details'])
            
            logs_df = pd.read_csv(self.logs_file)
            
            if limit and not logs_df.empty:
                return logs_df.tail(limit)
            
            return logs_df
        except Exception as e:
            print(f"Error getting logs: {str(e)}")
            return pd.DataFrame(columns=['timestamp', 'user_id', 'user_role', 'action', 'details'])
    
    def add_book(self, title, author, genre, copies=1):
        """Add a new book to the books.json file with multiple copies"""
        try:
            books = self.read_json_file('books.json')
            
            # Generate a new book ID
            book_id = f"BK-{str(len(books) + 1).zfill(3)}"
            
            new_book = {
                "id": book_id,
                "title": title,
                "author": author,
                "genre": genre,
                "available": True,
                "total_copies": copies,
                "available_copies": copies,
                "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            books.append(new_book)
            
            if self.write_json_file('books.json', books):
                return True, book_id
            else:
                return False, "Error writing to books file"
        except Exception as e:
            return False, f"Error adding book: {str(e)}"
    
    def update_book(self, book_id, title, author, genre, total_copies, available_copies):
        """Update a book in the books.json file"""
        try:
            books = self.read_json_file('books.json')
            
            for book in books:
                if book['id'] == book_id:
                    book['title'] = title
                    book['author'] = author
                    book['genre'] = genre
                    book['total_copies'] = total_copies
                    book['available_copies'] = available_copies
                    book['available'] = available_copies > 0
                    
                    if self.write_json_file('books.json', books):
                        return True, "Book updated successfully"
                    else:
                        return False, "Error writing to books file"
            
            return False, "Book not found"
        except Exception as e:
            return False, f"Error updating book: {str(e)}"
    
    def delete_book(self, book_id):
        """Delete a book from the books.json file"""
        try:
            books = self.read_json_file('books.json')
            issued_books = self.read_json_file('issued_books.json')
            
            # Check if book is currently issued
            for issued_book in issued_books:
                if issued_book['book_id'] == book_id and not issued_book.get('returned', False):
                    return False, "Cannot delete book that is currently issued"
            
            # Filter out the book to delete
            updated_books = [book for book in books if book['id'] != book_id]
            
            if len(updated_books) == len(books):
                return False, "Book not found"
            
            if self.write_json_file('books.json', updated_books):
                return True, "Book deleted successfully"
            else:
                return False, "Error writing to books file"
        except Exception as e:
            return False, f"Error deleting book: {str(e)}"
    
    def request_book_issue(self, student_id, book_id):
        """Student requests to borrow a book"""
        try:
            books = self.read_json_file('books.json')
            students = self.read_json_file('students.json')
            requests = self.read_json_file('requests.json')
            
            # Check if book exists and has available copies
            book_found = False
            book_available = False
            book_title = ""
            
            for book in books:
                if book['id'] == book_id:
                    book_found = True
                    book_available = book.get('available_copies', 0) > 0
                    book_title = book['title']
                    break
            
            if not book_found:
                return False, "Book not found"
            
            if not book_available:
                return False, "No copies of this book are available"
            
            # Check if student exists and is approved
            student_found = False
            student_approved = False
            student_flagged = False
            student_name = ""
            
            for student in students:
                if student['id'] == student_id:
                    student_found = True
                    student_approved = student.get('approved', False)
                    student_flagged = student.get('flagged', False)
                    student_name = student['name']
                    break
            
            if not student_found:
                return False, "Student not found"
            
            if not student_approved:
                return False, "Your account is not approved yet"
            
            # Check if flagged student already has a book
            if student_flagged:
                issued_books = self.read_json_file('issued_books.json')
                current_issues = [
                    issue for issue in issued_books 
                    if issue['student_id'] == student_id and not issue.get('returned', False)
                ]
                
                if len(current_issues) >= 1:
                    return False, "Flagged students can only have one book at a time"
            
            # Create a book issue request
            new_request = {
                "id": f"REQ-{len(requests) + 1}",
                "type": "issue",
                "student_id": student_id,
                "book_id": book_id,
                "requested_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "pending"
            }
            
            requests.append(new_request)
            
            # Save changes
            if self.write_json_file('requests.json', requests):
                return True, f"Request to borrow '{book_title}' submitted successfully. Waiting for admin approval."
            else:
                return False, "Error writing to files"
        except Exception as e:
            return False, f"Error requesting book: {str(e)}"
    
    def request_book_return(self, student_id, issue_id):
        """Student requests to return a book"""
        try:
            issued_books = self.read_json_file('issued_books.json')
            requests = self.read_json_file('requests.json')
            
            # Find the issue record
            issue_found = False
            book_id = ""
            
            for issue in issued_books:
                if issue['id'] == issue_id and issue['student_id'] == student_id:
                    issue_found = True
                    book_id = issue['book_id']
                    
                    if issue.get('returned', False):
                        return False, "Book already returned"
                    
                    if issue.get('return_requested', False):
                        return False, "Return already requested"
                    
                    # Mark as return requested
                    issue['return_requested'] = True
                    break
            
            if not issue_found:
                return False, "Issue record not found or not issued to you"
            
            # Create a return request
            new_request = {
                "id": f"REQ-{len(requests) + 1}",
                "type": "return",
                "student_id": student_id,
                "book_id": book_id,
                "issue_id": issue_id,
                "requested_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "pending"
            }
            
            requests.append(new_request)
            
            # Save changes
            if self.write_json_file('issued_books.json', issued_books) and self.write_json_file('requests.json', requests):
                return True, "Return request submitted successfully"
            else:
                return False, "Error writing to files"
        except Exception as e:
            return False, f"Error requesting return: {str(e)}"
    
    def approve_book_request(self, request_id):
        """Admin approves a book issue request"""
        try:
            requests = self.read_json_file('requests.json')
            
            # Find the request
            request_found = False
            request_type = ""
            student_id = ""
            book_id = ""
            issue_id = ""
            
            for request in requests:
                if request['id'] == request_id:
                    request_found = True
                    request_type = request['type']
                    student_id = request['student_id']
                    book_id = request['book_id']
                    issue_id = request.get('issue_id', "")
                    
                    if request['status'] != "pending":
                        return False, "Request is not pending"
                    
                    # Mark as approved
                    request['status'] = "approved"
                    request['approved_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    break
            
            if not request_found:
                return False, "Request not found"
            
            # Save request changes first to avoid data inconsistency
            self.write_json_file('requests.json', requests)
            
            # Process based on request type
            if request_type == "issue":
                # Issue the book
                success, message = self.issue_book_after_approval(student_id, book_id)
            elif request_type == "return":
                # Return the book
                success, message = self.return_book_after_approval(issue_id)
            else:
                return False, "Unknown request type"
            
            return success, message
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Detailed error in approve_book_request: {error_details}")
            return False, f"Error approving request: {str(e)}"
    
    def issue_book_after_approval(self, student_id, book_id, days=7):
        """Issue a book after admin approval"""
        try:
            books = self.read_json_file('books.json')
            students = self.read_json_file('students.json')
            issued_books = self.read_json_file('issued_books.json')
            
            # Check if book exists and has available copies
            book_found = False
            book_available = False
            book_title = ""
            
            for book in books:
                if book['id'] == book_id:
                    book_found = True
                    # Ensure available_copies exists
                    if 'available_copies' not in book:
                        book['available_copies'] = 1 if book.get('available', True) else 0
                    
                    if book['available_copies'] > 0:
                        book_available = True
                        book['available_copies'] -= 1
                        if book['available_copies'] == 0:
                            book['available'] = False
                    book_title = book['title']
                    break
            
            if not book_found:
                return False, "Book not found"
            
            if not book_available:
                return False, "No copies of this book are available"
            
            # Check if student exists
            student_found = False
            student_name = ""
            
            for student in students:
                if student['id'] == student_id:
                    student_found = True
                    student_name = student['name']
                    break
            
            if not student_found:
                return False, "Student not found"
            
            # Issue the book
            issue_date = datetime.now()
            due_date = issue_date + timedelta(days=days)
            
            new_issue = {
                "id": f"ISS-{len(issued_books) + 1}",
                "student_id": student_id,
                "book_id": book_id,
                "issue_date": issue_date.strftime("%Y-%m-%d %H:%M:%S"),
                "due_date": due_date.strftime("%Y-%m-%d %H:%M:%S"),
                "returned": False,
                "return_date": None
            }
            
            issued_books.append(new_issue)
            
            # Save changes
            if self.write_json_file('issued_books.json', issued_books) and self.write_json_file('books.json', books):
                return True, f"Book '{book_title}' issued to {student_name} successfully"
            else:
                return False, "Error writing to files"
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Detailed error in issue_book_after_approval: {error_details}")
            return False, f"Error issuing book: {str(e)}"
    
    def return_book_after_approval(self, issue_id):
        """Return a book after admin approval"""
        try:
            books = self.read_json_file('books.json')
            students = self.read_json_file('students.json')
            issued_books = self.read_json_file('issued_books.json')
            
            # Find the issue record
            issue_found = False
            book_id = ""
            student_id = ""
            due_date = None
            
            for issue in issued_books:
                if issue['id'] == issue_id:
                    issue_found = True
                    book_id = issue['book_id']
                    student_id = issue['student_id']
                    
                    # Handle missing due_date
                    if 'due_date' in issue:
                        due_date = datetime.strptime(issue['due_date'], "%Y-%m-%d %H:%M:%S")
                    else:
                        # If due_date is missing, set it to issue_date + 7 days
                        if 'issue_date' in issue:
                            issue_date = datetime.strptime(issue['issue_date'], "%Y-%m-%d %H:%M:%S")
                            due_date = issue_date + timedelta(days=7)
                        else:
                            # If both are missing, use current date (no late penalty)
                            due_date = datetime.now()
                    
                    if issue.get('returned', False):
                        return False, "Book already returned"
                    
                    # Mark as returned
                    issue['returned'] = True
                    issue['return_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    issue['return_requested'] = False
                    break
            
            if not issue_found:
                return False, "Issue record not found"
            
            # Find and update the book
            book_found = False
            for i, book in enumerate(books):
                if book['id'] == book_id:
                    book_found = True
                    
                    # Ensure total_copies exists
                    if 'total_copies' not in book:
                        book['total_copies'] = 1
                    
                    # Ensure available_copies exists and is an integer
                    if 'available_copies' not in book:
                        book['available_copies'] = 0
                    
                    # Convert to integer if it's a string
                    try:
                        available_copies = int(book['available_copies'])
                    except (ValueError, TypeError):
                        available_copies = 0
                    
                    # Increment available copies
                    book['available_copies'] = available_copies + 1
                    
                    # Set available flag
                    book['available'] = True
                    break
            
            # If book not found, create a placeholder
            if not book_found:
                print(f"Book {book_id} not found in database, creating placeholder")
                books.append({
                    "id": book_id,
                    "title": f"Book {book_id}",
                    "author": "Unknown",
                    "genre": "Unknown",
                    "available": True,
                    "total_copies": 1,
                    "available_copies": 1,
                    "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            # Check if return is late and flag student if needed
            current_date = datetime.now()
            is_late = current_date > due_date
            
            if is_late:
                student_found = False
                for student in students:
                    if student['id'] == student_id:
                        student_found = True
                        student['flagged'] = True
                        break
            
            # Save changes
            if (self.write_json_file('issued_books.json', issued_books) and 
                self.write_json_file('books.json', books) and 
                self.write_json_file('students.json', students)):
                
                message = "Book returned successfully"
                if is_late:
                    message += " (Late return - Student flagged)"
                
                return True, message
            else:
                return False, "Error writing to files"
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Detailed error in return_book_after_approval: {error_details}")
            return False, f"Error returning book: {str(e)}"
    
    def issue_book(self, student_id, book_id, days=7):
        """Direct issue book function (for admin use only)"""
        try:
            books = self.read_json_file('books.json')
            students = self.read_json_file('students.json')
            issued_books = self.read_json_file('issued_books.json')
            
            # Check if book exists and has available copies
            book_found = False
            book_available = False
            book_title = ""
            
            for book in books:
                if book['id'] == book_id:
                    book_found = True
                    # Ensure available_copies exists
                    if 'available_copies' not in book:
                        book['available_copies'] = 1 if book.get('available', True) else 0
                    
                    book_available = book['available_copies'] > 0
                    book_title = book['title']
                    break

            
            if not book_found:
                return False, "Book not found"
            
            if not book_available:
                return False, "No copies of this book are available"
            
            # Check if student exists and is approved
            student_found = False
            student_approved = False
            student_name = ""
            student_flagged = False
            
            for student in students:
                if student['id'] == student_id:
                    student_found = True
                    student_approved = student.get('approved', False)
                    student_name = student['name']
                    student_flagged = student.get('flagged', False)
                    break
            
            if not student_found:
                return False, "Student not found"
            
            if not student_approved:
                return False, "Student is not approved"
            
            # Check if flagged student already has a book
            if student_flagged:
                current_issues = [
                    issue for issue in issued_books 
                    if issue['student_id'] == student_id and not issue.get('returned', False)
                ]
                
                if len(current_issues) >= 1:
                    return False, "Flagged students can only have one book at a time"
            
            # Issue the book
            issue_date = datetime.now()
            due_date = issue_date + timedelta(days=days)
            
            new_issue = {
                "id": f"ISS-{len(issued_books) + 1}",
                "student_id": student_id,
                "book_id": book_id,
                "issue_date": issue_date.strftime("%Y-%m-%d %H:%M:%S"),
                "due_date": due_date.strftime("%Y-%m-%d %H:%M:%S"),
                "returned": False,
                "return_date": None
            }
            
            issued_books.append(new_issue)
            
            # Update book availability
            for book in books:
                if book['id'] == book_id:
                    # Ensure available_copies exists
                    if 'available_copies' not in book:
                        book['available_copies'] = 1 if book.get('available', True) else 0
                    
                    book['available_copies'] -= 1
                    if book['available_copies'] == 0:
                        book['available'] = False
                    break
            
            # Save changes
            if self.write_json_file('issued_books.json', issued_books) and self.write_json_file('books.json', books):
                return True, f"Book '{book_title}' issued to {student_name} successfully"
            else:
                return False, "Error writing to files"
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Detailed error in issue_book: {error_details}")
            return False, f"Error issuing book: {str(e)}"
    
    def return_book(self, issue_id):
        """Direct return book function (for admin use only)"""
        try:
            books = self.read_json_file('books.json')
            students = self.read_json_file('students.json')
            issued_books = self.read_json_file('issued_books.json')
            
            # Find the issue record
            issue_found = False
            book_id = ""
            student_id = ""
            due_date = None
            
            for issue in issued_books:
                if issue['id'] == issue_id:
                    issue_found = True
                    book_id = issue['book_id']
                    student_id = issue['student_id']
                    
                    # Handle missing due_date
                    if 'due_date' in issue:
                        due_date = datetime.strptime(issue['due_date'], "%Y-%m-%d %H:%M:%S")
                    else:
                        # If due_date is missing, set it to issue_date + 7 days
                        if 'issue_date' in issue:
                            issue_date = datetime.strptime(issue['issue_date'], "%Y-%m-%d %H:%M:%S")
                            due_date = issue_date + timedelta(days=7)
                        else:
                            # If both are missing, use current date (no late penalty)
                            due_date = datetime.now()
                    
                    if issue.get('returned', False):
                        return False, "Book already returned"
                    
                    # Mark as returned
                    issue['returned'] = True
                    issue['return_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    break
            
            if not issue_found:
                return False, "Issue record not found"
            
            # Find and update the book
            book_found = False
            for book in books:
                if book['id'] == book_id:
                    book_found = True
                    
                    # Ensure total_copies exists
                    if 'total_copies' not in book:
                        book['total_copies'] = 1
                    
                    # Ensure available_copies exists and is an integer
                    if 'available_copies' not in book:
                        book['available_copies'] = 0
                    
                    # Convert to integer if it's a string
                    try:
                        available_copies = int(book['available_copies'])
                    except (ValueError, TypeError):
                        available_copies = 0
                    
                    # Increment available copies
                    book['available_copies'] = available_copies + 1
                    
                    # Set available flag
                    book['available'] = True
                    break
            
            # If book not found, create a placeholder
            if not book_found:
                print(f"Book {book_id} not found in database, creating placeholder")
                books.append({
                    "id": book_id,
                    "title": f"Book {book_id}",
                    "author": "Unknown",
                    "genre": "Unknown",
                    "available": True,
                    "total_copies": 1,
                    "available_copies": 1,
                    "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            # Check if return is late and flag student if needed
            current_date = datetime.now()
            is_late = current_date > due_date
            
            if is_late:
                student_found = False
                for student in students:
                    if student['id'] == student_id:
                        student_found = True
                        student['flagged'] = True
                        break
            
            # Save changes
            if (self.write_json_file('issued_books.json', issued_books) and 
                self.write_json_file('books.json', books) and 
                self.write_json_file('students.json', students)):
                
                message = "Book returned successfully"
                if is_late:
                    message += " (Late return - Student flagged)"
                
                return True, message
            else:
                return False, "Error writing to files"
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Detailed error in return_book: {error_details}")
            return False, f"Error returning book: {str(e)}"
    
    def approve_student(self, student_id):
        """Approve a student's library card application"""
        try:
            students = self.read_json_file('students.json')
            
            for student in students:
                if student['id'] == student_id:
                    if student.get('approved', False):
                        return False, "Student already approved"
                    
                    student['approved'] = True
                    
                    if self.write_json_file('students.json', students):
                        return True, "Student approved successfully"
                    else:
                        return False, "Error writing to students file"
            
            return False, "Student not found"
        except Exception as e:
            return False, f"Error approving student: {str(e)}"
    
    def block_student(self, student_id):
        """Block a student's library access"""
        try:
            students = self.read_json_file('students.json')
            
            for student in students:
                if student['id'] == student_id:
                    student['approved'] = False
                    
                    if self.write_json_file('students.json', students):
                        return True, "Student blocked successfully"
                    else:
                        return False, "Error writing to students file"
            
            return False, "Student not found"
        except Exception as e:
            return False, f"Error blocking student: {str(e)}"
    
    def flag_student(self, student_id, flag_status=True):
        """Flag or unflag a student for late returns"""
        try:
            students = self.read_json_file('students.json')
            
            for student in students:
                if student['id'] == student_id:
                    student['flagged'] = flag_status
                    
                    if self.write_json_file('students.json', students):
                        action = "flagged" if flag_status else "unflagged"
                        return True, f"Student {action} successfully"
                    else:
                        return False, "Error writing to students file"
            
            return False, "Student not found"
        except Exception as e:
            return False, f"Error updating student flag status: {str(e)}"
    
    def get_analytics(self):
        """Get library analytics"""
        try:
            books = self.read_json_file('books.json')
            students = self.read_json_file('students.json')
            issued_books = self.read_json_file('issued_books.json')
            
            total_books = sum(book.get('total_copies', 1) for book in books)
            available_books = sum(book.get('available_copies', 1 if book['available'] else 0) for book in books)
            issued_books_count = total_books - available_books
            
            total_students = len(students)
            approved_students = sum(1 for student in students if student.get('approved', False))
            pending_students = total_students - approved_students
            
            flagged_students = sum(1 for student in students if student.get('flagged', False))
            
            currently_issued = sum(1 for issue in issued_books if not issue.get('returned', False))
            
            return {
                "total_books": total_books,
                "available_books": available_books,
                "issued_books": issued_books_count,
                "total_students": total_students,
                "approved_students": approved_students,
                "pending_students": pending_students,
                "flagged_students": flagged_students,
                "currently_issued": currently_issued
            }
        except Exception as e:
            print(f"Error getting analytics: {str(e)}")
            return {}