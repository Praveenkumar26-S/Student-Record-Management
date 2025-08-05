import json

class Student:
    def __init__(self, student_id, name, batch):
        self.student_id = student_id
        self.name = name
        self.batch = batch
        self.attendance = {"total_days": 0, "present_days": 0}
        self.terms = {}

    def add_term_result(self, term_name, subject_marks):
        self.terms[term_name] = subject_marks

    def update_subject_mark(self, term, subject, new_mark):
        if term in self.terms and subject in self.terms[term]:
            self.terms[term][subject] = new_mark

    def record_attendance(self, present_days, total_days):
        self.attendance["present_days"] += present_days
        self.attendance["total_days"] += total_days

    def calculate_average(self):
        total_marks = 0
        total_subjects = 0
        for marks in self.terms.values():
            total_marks += sum(marks.values())
            total_subjects += len(marks)
        if total_subjects > 0:
            return round(total_marks / total_subjects, 2)
        else:  
            return 0.0

    def attendance_percentage(self):
        total = self.attendance["total_days"]
        present = self.attendance["present_days"]
        if total :
            return round((present / total) * 100, 2)
        else:
            return 0.0

    def generate_report(self):
        print(f"\nStudent Report: {self.name} ({self.student_id})")
        print(f"Batch: {self.batch}")
        print(f"Attendance: {self.attendance_percentage()}%")
        for term, marks in self.terms.items():
            avg = round(sum(marks.values()) / len(marks), 2)
            print(f"{term} Average: {avg}")
        print(f"Overall Average: {self.calculate_average()}\n")

class StudentManagementSystem:
    def __init__(self):
        self.students = {}

    def register_student(self, student_id, name, batch):
        self.students[student_id] = Student(student_id, name, batch)

    def get_student(self, student_id):
        return self.students.get(student_id)

    def get_topper_by_term(self, term):
        topper = None
        highest_avg = 0
        for student in self.students.values():
            if term in student.terms:
                avg = sum(student.terms[term].values()) / len(student.terms[term])
                if avg > highest_avg:
                    highest_avg = avg
                    topper = student
        if topper:
            return topper, round(highest_avg, 2)
        else:
            return None

    def rank_students_by_average(self, batch):
        batch_students = [s for s in self.students.values() if s.batch == batch]
        ranked = sorted(batch_students, key=lambda s: -s.calculate_average())
        return ranked

    def export_to_json(self, filename):
        data = {}
        for sid, s in self.students.items():
            data[sid] = {
                "name": s.name,
                "batch": s.batch,
                "attendance": s.attendance,
                "terms": s.terms
            }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data exported to {filename}")

    def import_from_json(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        for sid, d in data.items():
            s = Student(sid, d["name"], d["batch"])
            s.attendance = d["attendance"]
            s.terms = d["terms"]
            self.students[sid] = s
        print(f"Data imported from {filename}")

def main():
    system = StudentManagementSystem()

    while True:
        print("\n--- Student Management System ---")
        print("1. Register Student")
        print("2. Add Term Result")
        print("3. Update Subject Mark")
        print("4. Record Attendance")
        print("5. Generate Report")
        print("6. Get Topper by Term")
        print("7. Rank Students by Batch")
        print("8. Export to JSON")
        print("9. Import from JSON")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            sid = input("Student ID: ")
            name = input("Name: ")
            batch = input("Batch: ")
            system.register_student(sid, name, batch)

        elif choice == "2":
            sid = input("Student ID: ")
            term = input("Term Name: ")
            subjects = {}
            n = int(input("How many subjects? "))
            for _ in range(n):
                sub = input("Subject: ")
                mark = float(input("Mark: "))
                subjects[sub] = mark
            student = system.get_student(sid)
            if student:
                student.add_term_result(term, subjects)

        elif choice == "3":
            sid = input("Student ID: ")
            term = input("Term: ")
            subject = input("Subject: ")
            new_mark = float(input("New Mark: "))
            student = system.get_student(sid)
            if student:
                student.update_subject_mark(term, subject, new_mark)

        elif choice == "4":
            sid = input("Student ID: ")
            present = int(input("Present Days: "))
            total = int(input("Total Days: "))
            student = system.get_student(sid)
            if student:
                student.record_attendance(present, total)

        elif choice == "5":
            sid = input("Student ID: ")
            student = system.get_student(sid)
            if student:
                student.generate_report()
            else:
                print("Student not found.")

        elif choice == "6":
            term = input("Enter term name: ")
            topper, avg = system.get_topper_by_term(term)
            if topper:
                print(f"Topper in {term}: {topper.name} ({topper.student_id}) with average {avg}")
            else:
                print("No topper found.")

        elif choice == "7":
            batch = input("Enter batch: ")
            ranked = system.rank_students_by_average(batch)
            print(f"\nRanking for Batch {batch}:")
            for i, s in enumerate(ranked, 1):
                print(f"{i}. {s.name} ({s.student_id}) - Average: {s.calculate_average()}")

        elif choice == "8":
            filename = input("Filename to export : ")
            system.export_to_json(filename)

        elif choice == "9":
            filename = input("Filename to import : ")
            system.import_from_json(filename)

        elif choice == "10":
            print("Exiting system.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
