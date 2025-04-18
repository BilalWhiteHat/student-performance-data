import csv
import tkinter as tk
from tkinter import filedialog, messagebox

class Student:
    def __init__(self, data):
        """
        Initialize a Student object from a dictionary of CSV data.

        The dictionary should contain the following keys:
        - gender
        - race/ethnicity
        - parental level of education
        - lunch
        - test preparation course
        - math score
        - reading score
        - writing score

        The scores are converted to floats and the average score is calculated
        using the calculate_average_score method.

        :param data: A dictionary of CSV data
        :type data: dict
        """
        self.gender = data['gender']
        self.ethnicity = data['race/ethnicity']
        self.parental_education = data['parental level of education']
        self.lunch = data['lunch']
        self.test_prep = data['test preparation course']
        self.math_score = float(data['math score'])
        self.reading_score = float(data['reading score'])
        self.writing_score = float(data['writing score'])
        self.average_score = self.calculate_average_score()

    def calculate_average_score(self):
        """
        Calculate the average score of a student by adding the math, reading,
        and writing scores and dividing by 3.

        :return: The average score of a student
        :rtype: float
        """
        return (self.math_score + self.reading_score + self.writing_score) / 3

    def determine_performance_feedback(self):
        """
        Determine the performance feedback based on the average score.

        This method categorizes the student's performance into one of five
        qualitative descriptors: "Outstanding", "Excellent", "Good", "Satisfactory",
        or "Needs Improvement", based on the student's average score.

        :return: A string representing the performance feedback
        :rtype: str
        """

        if self.average_score >= 90:
            return "Outstanding"
        elif self.average_score >= 80:
            return "Excellent"
        elif self.average_score >= 70:
            return "Good"
        elif self.average_score >= 60:
            return "Satisfactory"
        else:
            return "Needs Improvement"

class StudentPerformanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Calculator")
        self.root.geometry("700x600")

        # Title Label
        self.title_label = tk.Label(root, text="Student Performance Calculator", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Load CSV Button
        self.load_button = tk.Button(root, text="Load CSV File", command=self.load_file)
        self.load_button.pack(pady=5)

        # Entry for number of records
        self.limit_label = tk.Label(root, text="Number of records to display:")
        self.limit_label.pack(pady=5)
        self.limit_entry = tk.Entry(root)
        self.limit_entry.pack(pady=5)
        self.limit_entry.insert(0, "10")  # Default to show 10 records
        self.limit_entry.bind("<Return>", lambda _: self.refresh_display())  # Trigger refresh on Enter key

        # Dropdown for performance filter
        self.filter_label = tk.Label(root, text="Filter by Performance Level:")
        self.filter_label.pack(pady=5)
        self.performance_filter = tk.StringVar(root)
        self.performance_filter.set("All")  # Default filter
        self.filter_options = ["All", "Outstanding", "Excellent", "Good", "Satisfactory", "Needs Improvement"]
        self.filter_menu = tk.OptionMenu(root, self.performance_filter, *self.filter_options, command=lambda _: self.refresh_display())
        self.filter_menu.pack(pady=5)

        # Sorting options
        self.sort_label = tk.Label(root, text="Sort by Average Score:")
        self.sort_label.pack(pady=5)
        self.sort_order = tk.StringVar(root)
        self.sort_order.set("Descending")  # Default sort order
        self.sort_options = ["Ascending", "Descending"]
        self.sort_menu = tk.OptionMenu(root, self.sort_order, *self.sort_options, command=lambda _: self.refresh_display())
        self.sort_menu.pack(pady=5)

        # Export button
        self.export_button = tk.Button(root, text="Export Filtered Data", command=self.export_filtered_data)
        self.export_button.pack(pady=5)

        # Frame to display statistics
        self.stats_frame = tk.Frame(root)
        self.stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame to display student records
        self.student_frame = tk.Frame(root)
        self.student_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initialize variables
        self.students = []  # Store loaded data here

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.students = self.load_students_from_csv(file_path)
                self.refresh_display()  # Initial display after loading
                self.display_statistics()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def load_students_from_csv(self, file_path):
        students = []
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                student = Student(row)
                students.append(student)
        return students

    def apply_filters(self):
        # Filter by performance level
        selected_filter = self.performance_filter.get()
        if selected_filter != "All":
            filtered_students = [s for s in self.students if s.determine_performance_feedback() == selected_filter]
        else:
            filtered_students = self.students[:]

        # Sort by average score
        if self.sort_order.get() == "Descending":
            filtered_students.sort(key=lambda x: x.average_score, reverse=True)
        else:
            filtered_students.sort(key=lambda x: x.average_score)

        return filtered_students

    def refresh_display(self):
        try:
            limit = int(self.limit_entry.get())
        except ValueError:
            limit = 10  # Default to 10 if input is invalid

        # Apply filters and limit the number of students displayed
        filtered_students = self.apply_filters()[:limit]
        self.display_students(filtered_students)

    def display_students(self, students):
        # Clear previous student frames
        for widget in self.student_frame.winfo_children():
            widget.destroy()

        for student in students:
            frame = tk.Frame(self.student_frame, relief=tk.RAISED, borderwidth=1)
            frame.pack(fill=tk.X, padx=5, pady=5)

            info = (
                f"Gender: {student.gender}\n"
                f"Race/Ethnicity: {student.ethnicity}\n"
                f"Parental Education: {student.parental_education}\n"
                f"Lunch: {student.lunch}\n"
                f"Test Preparation: {student.test_prep}\n"
                f"Math Score: {student.math_score}\n"
                f"Reading Score: {student.reading_score}\n"
                f"Writing Score: {student.writing_score}\n"
                f"Average Score: {student.average_score:.2f}\n"
                f"Feedback: {student.determine_performance_feedback()}"
            )
            label = tk.Label(frame, text=info, justify=tk.LEFT, padx=10)
            label.pack(anchor="w")

            # Visualize the average score with a bar
            canvas = tk.Canvas(frame, height=20, width=300)
            canvas.pack()
            bar_length = int(student.average_score * 3)  # scale factor for the bar length
            canvas.create_rectangle(0, 0, bar_length, 20, fill="blue")
            canvas.create_text(bar_length + 10, 10, anchor="w", text=f"{student.average_score:.2f}")

    def display_statistics(self):
        # Clear previous statistics
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        if self.students:
            avg_scores = [s.average_score for s in self.students]
            highest_score = max(avg_scores)
            lowest_score = min(avg_scores)
            overall_avg = sum(avg_scores) / len(avg_scores)

            stats_text = (
                f"Highest Average Score: {highest_score:.2f}\n"
                f"Lowest Average Score: {lowest_score:.2f}\n"
                f"Overall Average Score: {overall_avg:.2f}"
            )
            stats_label = tk.Label(self.stats_frame, text=stats_text, font=("Arial", 12), justify=tk.LEFT)
            stats_label.pack()

    def export_filtered_data(self):
        filtered_students = self.apply_filters()
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if save_path:
            try:
                with open(save_path, "w", newline='') as csvfile:
                    fieldnames = ["gender", "race/ethnicity", "parental level of education", "lunch",
                                  "test preparation course", "math score", "reading score", "writing score", "average score", "performance"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for student in filtered_students:
                        writer.writerow({
                            "gender": student.gender,
                            "race/ethnicity": student.ethnicity,
                            "parental level of education": student.parental_education,
                            "lunch": student.lunch,
                            "test preparation course": student.test_prep,
                            "math score": student.math_score,
                            "reading score": student.reading_score,
                            "writing score": student.writing_score,
                            "average score": student.average_score,
                            "performance": student.determine_performance_feedback()
                        })
                messagebox.showinfo("Export Successful", "Filtered data exported successfully.")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export data:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentPerformanceApp(root)
    root.mainloop()
