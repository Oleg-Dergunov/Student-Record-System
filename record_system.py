# Python application that simulates a Student Record System. The system uses Object-Oriented Programming (OOP)
# concepts to manage student data (e.g., name, ID, subjects, and marks), includes file handling to store and retrieve
# records (in JSON format), and integrate external tabulate libraries to enhance output formatting and data processing.

# Name: Oleg Dergunov
# Email: Oleg.Dergunov@outlook.com
# 04/2025

import json # Import a module for work with files in json format
from tabulate import tabulate # Import a module for making table to show student data

# Class for storing student info
class Student:
    def __init__(self, student_id, name, subjects, marks):
        # Constructor make new student object
        self.student_id = student_id # ID of student, must be unique
        self.name = name # Name of student
        self.subjects = subjects # List of subjects for student
        self.marks = marks # Marks for all subjects

    def calculate_average(self):
        # Calculate and return the average rounded to 2 decimal places
        return round(sum(self.marks.values()) / len(self.marks), 2)


# Class for controlling all students
class StudentRecordSystem:
    def __init__(self):
        self.records = [] # Here all student objects are stored

    def add_student(self):
        # Adding new student
        try:
            student_id = input("Enter Student ID: ") # Ask ID of student
            # Check if ID already exist
            if any(record.student_id == student_id for record in self.records):
                print("Error: Student ID must be unique.") # ID not unique, show error
                return # Stop adding
            name = input("Enter Name: ") # Ask name of student
            # Ask list of subjects, split them into list
            subjects = input("Enter Subjects (comma-separated): ").split(',')
            marks = {} # Create empty dictionary for marks
            for subject in subjects: # Loop over all subjects
                while True: # Infinite loop for mark validation
                    try:
                        # Ask marks for current subject
                        print("Enter marks for ", subject.strip(), ": ", sep="", end="")
                        mark = int(input())
                        if mark < 0: # Check if mark is negative
                            raise ValueError("Marks cannot be negative.") # Raise error for bad input
                        elif mark > 100: # Check if mark is greater then 100
                            raise ValueError("Marks cannot be greater than 100.") # Raise error for mark inappropriate in Ireland
                        marks[subject.strip()] = mark # Add mark to marks dictionary
                        break # Break loop if mark is good
                    except ValueError as e:
                        print(e) # Show error message
            # Make new student and add to records
            self.records.append(Student(student_id, name, subjects, marks))
            print("Student added successfully!") # Print success message
        except Exception as e:
            print("Error: ", str(e), sep="") # Catch all unexpected errors

    def view_students(self):
        # View all students in the system
        if not self.records:  # Check if there are no records
            print("No student records found.") # Print message if empty
            return # Exit function

        # Prepare table data with formatted marks
        table = []
        for s in self.records:
            # Format marks with subjects in a single column
            marks_lines = [f"{subject}: {mark}" for subject, mark in s.marks.items()]
            formatted_marks = "\n".join(marks_lines) # Combine into multiline string
            table.append([s.student_id, s.name, formatted_marks, s.calculate_average()])

        # Define headers for the table
        headers = ["ID", "Name", "Marks", "Average"]
        # Print table using tabulate
        print(tabulate(table, headers=headers, tablefmt="grid"))


    def search_student(self):
        # Search student by ID
        student_id = input("Enter Student ID to search: ") # Ask ID to search
        for record in self.records: # Go through all records
            if record.student_id == student_id: # Check if ID matches
                # Prepare table data for the found student
                marks_lines = [f"{subject}: {mark}" for subject, mark in record.marks.items()]
                formatted_marks = "\n".join(marks_lines) # Format marks for table
                table = [[record.student_id, record.name, formatted_marks, record.calculate_average()]]
                headers = ["ID", "Name", "Marks", "Average"] # Define headers
                # Print the table using tabulate
                print(tabulate(table, headers=headers, tablefmt="grid"))
                return # Exit function
        print("Student not found.") # Print message if ID not found


    def top_performing_students(self):
        # Find and show student(s) with best average marks
        # If more then one student share the highest average marks all of them will be shown
        if not self.records: # Check if no records exist
            print("No student records to analyze.") # Print error message
            return # Exit function

        # Find highest average marks
        max_avg = max(record.calculate_average() for record in self.records)
        # Get all students with highest average marks
        top_students = [record for record in self.records if record.calculate_average() == max_avg]

        # Prepare table data for top-performing students
        table = []
        for student in top_students:
            marks_lines = [f"{subject}: {mark}" for subject, mark in student.marks.items()]
            formatted_marks = "\n".join(marks_lines) # Format marks for table
            table.append([student.student_id, student.name, formatted_marks, student.calculate_average()])

        headers = ["ID", "Name", "Marks", "Average"] # Define headers
        # Print the table using tabulate
        print("Top Performing Student(s):")
        print(tabulate(table, headers=headers, tablefmt="grid"))



    def save_to_file(self):
        # Save all records to json file
        try:
            filename = input("Enter the filename to save records (e.g., students.json): ").strip() # Ask filename
            # Check if filename is valid (not empty, ends with .json)
            if not filename.endswith(".json") or len(filename) <= 5:
                print("Error: Filename must end with '.json' and can not be empty.") # Print error message
                return # Exit function
            stream = open(filename, "w") # Open file in write mode
            try:
                # Convert records to json format and write to file
                json.dump([{
                    "student_id": s.student_id,
                    "name": s.name,
                    "subjects": s.subjects,
                    "marks": s.marks
                } for s in self.records], stream, indent=4)
                # Print success message
                print("Records successfully saved to ", filename, ".", sep="")
            finally:
                stream.close() # Close the file
        except Exception as e:
            print("Error saving to file: ", str(e), sep="") # Catch errors and print error message

    def load_from_file(self):
        # Load records from json file
        try:
            filename = input("Enter the filename to load records from (e.g., students.json): ").strip() # Ask filename
            # Check if filename is valid (not empty, ends with .json)
            if not filename.endswith(".json") or len(filename) <= 5:
                print("Error: Filename must end with '.json' and can not be empty.") # Print error message
                return # Exit function
            stream = open(filename, "r") # Open file in read mode
            try:
                # Read json data from file
                data = json.load(stream)
                # Convert json data to student objects
                self.records = [Student(d["student_id"], d["name"], d["subjects"], d["marks"]) for d in data]
                # Print success message
                print("Records successfully loaded from ", filename, ".", sep="")
            finally:
                stream.close() # Close the file
        except Exception as e:
            print("Error loading from file: ", str(e), sep="") # Catch unexpected errors

# Menu function for user interaction
    def menu(self):
        while True: # Infinite loop for menu
            print("\nMenu:") # Print menu header
            # Display the menu options to the user
            print("1. Add Student Record")
            print("2. View All Student Records")
            print("3. Search Student by ID")
            print("4. View Top-Performing Student(s)")
            print("5. Save Records to File")
            print("6. Load Records from File")
            print("7. Exit")
            
            try:
                # Ask user to choose an option from the menu
                choice = int(input("Choose an option: "))
                
                if choice == 1:
                    # Call the add_student method to add a new student record
                    self.add_student()
                elif choice == 2:
                    # Call the view_students method to display all student records
                    self.view_students()
                elif choice == 3:
                    # Call the search_student method to search for a student by ID
                    self.search_student()
                elif choice == 4:
                    # Call the top_performing_students method to find top-performing students
                    self.top_performing_students()
                elif choice == 5:
                    # Call the save_to_file method to save records to a JSON file
                    self.save_to_file()
                elif choice == 6:
                    # Call the load_from_file method to load records from a JSON file
                    self.load_from_file()
                elif choice == 7:
                    # Exit the program when the user selects this option
                    print("Exiting the program. Goodbye!")
                    break  # Exit the loop and end the program
                else:
                    # Handle invalid menu choices (e.g., numbers outside the range)
                    print("Invalid choice, please try again.")
                    
            except ValueError:
                # Handle the case when the user inputs non-integer values
                print("Please enter a valid number.")
            
            input("Press enter to continue. ") # Pause for the user to read the response

# Program body
if __name__ == "__main__":
    print("\nWelcome to Smart Student Record System!") # Print welcome message
    system = StudentRecordSystem() # Create instance of system
    system.menu() # Call menu function to start
