# MADE BY PARTH ADSUL

import streamlit as st
import os
import datetime
from openpyxl import Workbook
st.markdown("""
<style>
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)
# ================= FILES =================
STUDENT_FILE = "students3.txt"
GRADE_FILE = "grades3.txt"

# ================= Validation =================
def validate_student_id(sid):
    return sid.startswith("STU") and sid[3:].isdigit() and len(sid) == 6

def validate_dob(d):
    try:
        datetime.datetime.strptime(d, "%d/%m/%Y")
        return True
    except:
        return False
    
def validate_marks(marks,max_marks):
    try:
        marks = float(marks)
        max_marks = float(max_marks)
        return 0 <= marks <= max_marks
    except:
        return False    

def exam_type(assessment_type):
    exam=["quiz","class assesment","case study","report","project","presentation"]
    if assessment_type in exam:
        return True
    else:
        return False

def grade_point(p):
    if p >= 90: return 4.0
    if p >= 85: return 3.7
    if p >= 80: return 3.3
    if p >= 75: return 3.0
    if p >= 70: return 2.7
    if p >= 65: return 2.3
    if p >= 60: return 2.0
    return 0.0

# ================= FILE HANDLING =================
def load_students():
    students = []
    if not os.path.exists(STUDENT_FILE):
        open(STUDENT_FILE, "w").close()
    with open(STUDENT_FILE) as f:
        for line in f:
            d = line.strip().split("|")
            if len(d) == 8:
                students.append({
                    "student_id": d[0],
                    "first_name": d[1],
                    "last_name": d[2],
                    "email": d[3],
                    "dob": d[4],
                    "program": d[5],
                    "enrollment_year": d[6],
                    "status": d[7]
                })
    return students

def save_students(students):
    with open(STUDENT_FILE, "w") as f:
        for s in students:
            f.write("|".join(s.values()) + "\n")

def load_grades():
    grades = []
    if not os.path.exists(GRADE_FILE):
        open(GRADE_FILE, "w").close()
    with open(GRADE_FILE) as f:
        for line in f:
            d = line.strip().split("|")
            if len(d) == 7:
                grades.append({
                    "student_id": d[0],
                    "subject": d[1],
                    "assessment_type": d[2],
                    "marks_obtained": float(d[3]),
                    "maximum_marks": float(d[4]),
                    "date": d[5],
                    "semester": d[6]
                })
    return grades

def save_grades(grades):
    with open(GRADE_FILE, "w") as f:
        for g in grades:
            f.write("|".join([
                g["student_id"], g["subject"], g["assessment_type"],
                str(g["marks_obtained"]), str(g["maximum_marks"]),
                g["date"], g["semester"]
            ]) + "\n")



# ================= STREAMLIT UI =================
st.set_page_config("Student Grade System", layout="wide")
st.title("🎓 Student Grade Management System")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Add Student",
        "View Students",
        "Upadate Student",
        "Delete Student",
        "Add Grade",
        "View Grades",
        "Upgrade Grades",
        "Delete Grades",
        "Calculate GPA",
        "Export to Excel",
        "Import from Excel****"
    ]
)

students = load_students()
grades = load_grades()

# ================= ADD STUDENT =================
if menu == "Add Student":
    st.subheader("➕ Add Student")

    with st.form("add_student", clear_on_submit=True):
        sid = st.text_input("Student ID (STU001)")
        fn = st.text_input("First Name")
        ln = st.text_input("Last Name")
        email = st.text_input("Email")
        dob = st.text_input("DOB (DD/MM/YYYY)")
        program = st.text_input("Program")
        year = st.text_input("Enrollment Year")
        submit = st.form_submit_button("Add Student")

    if submit:
        if not validate_student_id(sid):
            st.error("Invalid Student ID")
        elif any(s["student_id"] == sid for s in students):
            st.warning("Student already exists")
        elif not validate_dob(dob):
            st.error("Invalid DOB")
        else:
            students.append({
                "student_id": sid,
                "first_name": fn,
                "last_name": ln,
                "email": email,
                "dob": dob,
                "program": program,
                "enrollment_year": year,
                "status": "Active"
            })
            save_students(students)
            st.success("Student added successfully 🎉")

# ================= VIEW STUDENTS =================
elif menu == "View Students":
    st.subheader("📋 All Students")
    st.dataframe(students, use_container_width=True)#<<<--displays data in table format

 # ================= UPDATE STUDENT =================
elif menu=="Upadate Student":
   
    st.subheader("✏️ Update Student")

    sid = st.selectbox(
        "Select Student ID",
        [s["student_id"] for s in students]
    )

    # find student using for loop
    student = None
    for s in students:
        if s["student_id"] == sid:
            student = s
            break

    if student is None:
        st.error("Student not found")
    else:
        with st.form("update_student"):
            fn = st.text_input("First Name", student["first_name"])
            ln = st.text_input("Last Name", student["last_name"])
            email = st.text_input("Email", student["email"])
            dob = st.text_input("DOB (DD/MM/YYYY)", student["dob"])
            program = st.text_input("Program", student["program"])
            year = st.text_input("Enrollment Year", student["enrollment_year"])
            status = st.selectbox(
                "Status",
                ["Active", "Inactive"],
                index=0 if student["status"] == "Active" else 1
            )

            submit = st.form_submit_button("Update Student")

        if submit:
            if not validate_dob(dob):
                st.error("Invalid DOB")
            else:
                for s in students:
                    if s["student_id"] == sid:
                        s["first_name"] = fn
                        s["last_name"] = ln
                        s["email"] = email
                        s["dob"] = dob
                        s["program"] = program
                        s["enrollment_year"] = year
                        s["status"] = status

                save_students(students)
                st.success("Student updated successfully ✅")
                st.rerun()

# ================= DELETE STUDENT =================
elif menu == "Delete Student":
    st.subheader("🗑️ Delete Student")

    sid = st.selectbox(
        "Select Student ID to Delete",
        [s["student_id"] for s in students]
    )

    # find student using for loop
    student = None
    for s in students:
        if s["student_id"] == sid:
            student = s
            break

    if student is None:
        st.error("Student not found")
    else:
        st.warning(
            f"Are you sure you want to delete "
            f"{student['first_name']} {student['last_name']} ?"
        )

        if st.button("❌ Confirm Delete"):
            # remove student
            new_students = []
            for s in students:
                if s["student_id"] != sid:
                    new_students.append(s)

            save_students(new_students)

            # also remove grades
            new_grades = []
            for g in grades:
                if g["student_id"] != sid:
                    new_grades.append(g)

            save_grades(new_grades)

            st.success("Student deleted successfully 🗑️")
            st.rerun()


# ================= ADD GRADE =================
elif menu == "Add Grade":
    st.subheader("📝 Add Grade")

    with st.form("add_grade", clear_on_submit=True):
        sid = st.selectbox("Student ID", [s["student_id"] for s in students])
        subject = st.text_input("Subject")
        atype = st.text_input("Assessment Type")
        marks = st.number_input("Marks Obtained", 0.0)
        max_marks = st.number_input("Maximum Marks", 0.0)
        date = st.text_input("Date (DD/MM/YYYY)")
        sem = st.selectbox("Semester", ["1st","2nd","3rd","4th","5th","6th","7th","8th"])
        submit = st.form_submit_button("Add Grade")

    if submit:
         if not validate_marks(marks,max_marks):
             st.error("Enter Validate Marks!!!") 
         elif not validate_dob(date):
             st.error("Add date in format(DD/MM/YYYY)")
         elif not exam_type(atype):
             st.error("Assessment type should be (quiz, class assesment, presentation, report, project, case study)")   

         else:

            grades.append({
                "student_id": sid,
                "subject": subject,
                "assessment_type": atype,
                "marks_obtained": marks,
                "maximum_marks": max_marks,
                "date": date,
                "semester": sem
            })
            save_grades(grades)
            st.success("Grade added successfully ✅")

# ================= VIEW GRADES =================
elif menu == "View Grades":
    st.subheader("📊 Student Grades")
    sid = st.selectbox("Student ID", [s["student_id"] for s in students])
    filtered = [g for g in grades if g["student_id"] == sid]
    st.dataframe(filtered, use_container_width=True)

# ================= GPA =================
elif menu == "Calculate GPA":
    st.subheader("📐 GPA Calculator")

    with st.form("gpa_form"):
        sid = st.selectbox("Student ID", [s["student_id"] for s in students])
        sem = st.selectbox("Semester", ["1st","2nd","3rd","4th","5th","6th","7th","8th"])
        calc = st.form_submit_button("Calculate GPA")

    if calc:
        sg = [g for g in grades if g["student_id"] == sid and g["semester"] == sem]
        if not sg:
            st.warning("No grades found")
        else:
            gpa = sum(grade_point((g["marks_obtained"]/g["maximum_marks"])*100) for g in sg) / len(sg)
            st.success(f"GPA = {gpa:.2f}")

# ================= EXCEL =================
elif menu == "Export to Excel":

    st.subheader("📊 Export Grades to Excel")

    if st.button("Export Grades to Excel"):
        from openpyxl import Workbook

        wb = Workbook()
        sh = wb.active
        sh.title = "Grades Report"

       
        sh.append([
            "Student ID",
            "Subject",
            "Assessment Type",
            "Marks ",
            "Maximim Marks",
            "Date ",
            "Semester "
        ])

       
        for g in grades:
            sh.append(list(g.values()))

        
        file_name = "SGMS_Report.xlsx"
        wb.save(file_name)

        st.success("Excel file created successfully ✅")

        
        with open(file_name, "rb") as file:
            st.download_button(
                label="⬇️ Download Excel Report",
                data=file,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    
elif menu == "Upgrade Grades":

    st.subheader("✏️ Upgrade Grades")

    sid = st.selectbox(
        "Select Student ID",
        [s["student_id"] for s in students]
    )

    # collect grades of that student
    student_grades = []
    for g in grades:
        if g["student_id"] == sid:
            student_grades.append(g)

    if len(student_grades) == 0:
        st.warning("No grades found for this student")
    else:
        options = []
        for g in student_grades:
            options.append(
                g["subject"] + " | " + g["assessment_type"] + " | " + g["semester"]
            )

        selected = st.selectbox("Select Grade to Update", options)

        # find selected grade
        selected_grade = None
        for g in student_grades:
            label = g["subject"] + " | " + g["assessment_type"] + " | " + g["semester"]
            if label == selected:
                selected_grade = g
                break

        with st.form("update_grade"):
            subject = st.text_input("Subject", selected_grade["subject"])
            atype = st.text_input("Assessment Type", selected_grade["assessment_type"])
            marks = st.number_input(
                "Marks Obtained",
                value=float(selected_grade["marks_obtained"])
            )
            max_marks = st.number_input(
                "Maximum Marks",
                value=float(selected_grade["maximum_marks"])
            )
            date = st.text_input("Date (DD/MM/YYYY)", selected_grade["date"])
            sem = st.selectbox(
                "Semester",
                ["1st","2nd","3rd","4th","5th","6th","7th","8th"],
                index=["1st","2nd","3rd","4th","5th","6th","7th","8th"]
                .index(selected_grade["semester"])
            )

            submit = st.form_submit_button("Update Grade")

        if submit:
            if not validate_marks(marks, max_marks):
                st.error("Invalid Marks")
            elif not validate_dob(date):
                st.error("Invalid Date")
            elif not exam_type(atype):
                st.error("Invalid Assessment Type")
            else:
                for g in grades:
                    if (
                        g["student_id"] == sid and
                        g["subject"] == selected_grade["subject"] and
                        g["assessment_type"] == selected_grade["assessment_type"] and
                        g["semester"] == selected_grade["semester"]
                    ):
                        g["subject"] = subject
                        g["assessment_type"] = atype
                        g["marks_obtained"] = marks
                        g["maximum_marks"] = max_marks
                        g["date"] = date
                        g["semester"] = sem

                save_grades(grades)
                st.success("Grade updated successfully ✅")
                st.rerun()


elif menu == "Delete Grades":

    st.subheader("🗑️ Delete Grade")

    sid = st.selectbox(
        "Select Student ID",
        [s["student_id"] for s in students]
    )

    # collect grades of selected student
    student_grades = []
    for g in grades:
        if g["student_id"] == sid:
            student_grades.append(g)

    if len(student_grades) == 0:
        st.warning("No grades found for this student")
    else:
        options = []
        for g in student_grades:
            options.append(
                g["subject"] + " | " + g["assessment_type"] + " | " + g["semester"]
            )

        selected = st.selectbox("Select Grade to Delete", options)

        # find selected grade
        selected_grade = None
        for g in student_grades:
            label = g["subject"] + " | " + g["assessment_type"] + " | " + g["semester"]
            if label == selected:
                selected_grade = g
                break

        st.warning("⚠️ This action cannot be undone")

        if st.button("❌ Confirm Delete Grade"):
            new_grades = []

            for g in grades:
                if not (
                    g["student_id"] == sid and
                    g["subject"] == selected_grade["subject"] and
                    g["assessment_type"] == selected_grade["assessment_type"] and
                    g["semester"] == selected_grade["semester"]
                ):
                    new_grades.append(g)

            save_grades(new_grades)
            st.success("Grade deleted successfully 🗑️")
            st.rerun()


elif menu == "Import from Excel****":
    st.write("Sorry we are working on this feature!! Stay Tuned")
