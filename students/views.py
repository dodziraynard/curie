from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from students.models import Student, Klass, Subject, Course
from staff.models import Staff
from sheet_engine.functions import *
from django.db.utils import IntegrityError
from logger.utils import log_system_error


def students(request):
    template_name = "students/students.html"
    context = {

    }
    return render(request, template_name, context)


def new_student(request):
    template_name = "students/new_student.html"
    last_student = Student.objects.last()
    next_id = int(last_student.student_id) + \
        1 if last_student and last_student.student_id.isnumeric() else ""
    context = {
        "classes": Klass.objects.all(),
        "last_id": last_student.student_id if last_student else "",
        "next_id": next_id
    }
    if request.method == "GET":
        return render(request, template_name, context)

    elif request.method == "POST":
        post_data = request.POST.copy()
        post_data.pop("csrfmiddlewaretoken")
        electives = post_data.pop("electives")

        # Is the student info being edited?
        editing = post_data.pop("editing")[0]

        klass = get_object_or_404(Klass, class_id=post_data.pop("klass")[0])
        student_data = {k: v.strip() for k, v in post_data.items()}
        student_data.update({"klass": klass})
        electives = Subject.objects.filter(subject_id__in=electives)
        student_id = student_data.get("student_id")

        try:
            if editing:
                Student.objects.filter(
                    student_id=student_id).update(**student_data)
                n_student = get_object_or_404(Student, student_id=student_id)
            else:
                n_student = Student.objects.create(**student_data)
        except IntegrityError as err:
            if "UNIQUE constraint failed" in str(err):
                context.update(
                    {"error_message": f"Student with {student_id} already exists."})
            else:
                log_system_error("new_student", str(err))
                context.update(
                    {"error_message": "Oops, an unknown error occurred."})
            context.update({
                k: v for k, v in request.POST.items()
            })
            return render(request, template_name, context)
        n_student.electives.set(electives)
        return redirect("students:students")


def new_student_sheet(request):
    template_name = "students/new_student_sheet.html"
    context = {}
    if request.method == "GET":
        return render(request, template_name, context)
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            context.update({"error_message": "No file selected"})
            return render(request, template_name, context)

        # Returns True for success and string if error.
        res = insert_students(file.file)
        if res == True:
            request.session["message"] = "Sucessfully added students."
            return redirect("students:students")
        elif isinstance(res, str):
            context.update({"error_message": res})
        else:
            context.update({"error_message": "An unknown error occured."})
        return render(request, template_name, context)


def edit_student(request, student_id):
    template_name = "students/new_student.html"
    student = Student.objects.values().get(student_id=student_id)
    student_electives = Student.objects.get(
        student_id=student_id).electives.all()
    electives = Student.objects.get(
        student_id=student_id).klass.course.subjects.filter(is_elective=True)
    context = {**student}
    context.update({
        "editing": True,
        "classes": Klass.objects.all(),
        "student_electives": student_electives,
        "electives": electives,
    })
    return render(request, template_name, context)


def delete_student(request):
    student_id = request.POST.get("student_id")
    if not student_id:
        request.session["error_message"] = "No student ID found."
        return redirect("students:students")
    Student.objects.filter(student_id=student_id).delete()
    request.session["message"] = "Deleted successfully"
    return redirect("students:students")


def student_detail(request, student_id):
    template_name = "students/student_details.html"
    student = get_object_or_404(Student, student_id=student_id)
    context = {
        "student": student
    }
    return render(request, template_name, context)


def classes(request):
    template_name = "classes/classes.html"
    context = {
    }
    return render(request, template_name, context)


def new_class(request):
    template_name = "classes/new_class.html"
    
    context = {
        "teachers":Staff.objects.filter(has_left=False, klass=None),
        "courses":Course.objects.all(),
    }
    if request.method == "GET":
        return render(request, template_name, context)

    elif request.method == "POST":
        post_data = request.POST.copy()
        post_data.pop("csrfmiddlewaretoken")

        # Is the class info being edited?
        editing = post_data.pop("editing")[0]

        staff = get_object_or_404(Staff, staff_id=post_data.pop("staff_id")[0])
        course = get_object_or_404(Course, course_id=post_data.pop("course_id")[0])
        
        class_data = {k: v.strip() for k, v in post_data.items()}
        class_data.update({"class_teacher": staff})
        class_data.update({"course": course})
        
        class_id = class_data.get("class_id")
        try:
            if editing:
                Klass.objects.filter(class_id=class_id).update(**class_data)
            else:
                Klass.objects.create(**class_data)
        except IntegrityError as err:
            if "UNIQUE constraint failed" in str(err):
                context.update({"error_message": f"Class with {class_id} already exists. {str(err)}"})
            else:
                log_system_error("new_student", str(err))
                context.update({"error_message": "Oops, an unknown error occurred."})
            context.update({k: v for k, v in request.POST.items()})
            return render(request, template_name, context)
        return redirect("students:classes")

def edit_class(request, class_id):
    template_name = "classes/new_class.html"
    klass = Klass.objects.values().get(class_id=class_id)
    klass.update({"course_id": Course.objects.get(id=klass.get("course_id")).course_id})
    klass.update({"staff_id": Staff.objects.get(id=klass.get("class_teacher_id")).staff_id})
    context = {**klass}
    context.update({
        "editing": True,
        "classes": Klass.objects.all(),
        "courses": Course.objects.all(),
        "teachers": Staff.objects.filter(id=klass.get("class_teacher_id")),
    })
    return render(request, template_name, context)

def delete_class(request):
    class_id = request.POST.get("class_id")
    if not class_id:
        request.session["error_message"] = "No class ID found."
        return redirect("students:classes")
    Klass.objects.filter(class_id=class_id).delete()
    request.session["message"] = "Deleted successfully"
    return redirect("students:classes")


def class_detail(request, class_id):
    template_name = "classes/class_details.html"
    klass = get_object_or_404(Klass, class_id=class_id)
    context = {
        "class": klass
    }
    return render(request, template_name, context)


def subjects(request):
    template_name = "subjects/subjects.html"
    context = {
    }
    return render(request, template_name, context)


def new_subject(request):
    template_name = "subjects/new_subject.html"
    
    context = {
    }
    if request.method == "GET":
        return render(request, template_name, context)

    elif request.method == "POST":
        post_data = request.POST.copy()
        post_data.pop("csrfmiddlewaretoken")
        is_elective = "on" in post_data.pop("is_elective","") 

        # Is the subject info being edited?
        editing = post_data.pop("editing")[0]

        subject_data = {k: v.strip() for k, v in post_data.items()}
        subject_data.update({"is_elective": is_elective})
        subject_id = subject_data.get("subject_id")

        try:
            if editing:
                Subject.objects.filter(subject_id=subject_id).update(**subject_data)
            else:
                Subject.objects.create(**subject_data)
        except IntegrityError as err:
            if "UNIQUE constraint failed" in str(err):
                context.update(
                    {"error_message": f"Subject with {subject_id} already exists."})
            else:
                log_system_error("new_subject", str(err))
                context.update(
                    {"error_message": "Oops, an unknown error occurred."})
            context.update({
                k: v for k, v in request.POST.items()
            })
            return render(request, template_name, context)
        return redirect("students:subjects")


def new_subject_sheet(request):
    template_name = "subjects/new_subject_sheet.html"
    context = {}
    if request.method == "GET":
        return render(request, template_name, context)
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            context.update({"error_message": "No file selected"})
            return render(request, template_name, context)

        # Returns True for success and string if error.
        res = insert_subjects(file.file)
        if res == True:
            request.session["message"] = "Sucessfully added subjects."
            return redirect("students:subjects")
        elif isinstance(res, str):
            context.update({"error_message": res})
        else:
            context.update({"error_message": "An unknown error occured."})
        return render(request, template_name, context)

def edit_subject(request, subject_id):
    template_name = "subjects/new_subject.html"
    subject = Subject.objects.values().get(subject_id=subject_id)
    context = {**subject}
    context.update({
        "editing": True,
    })
    return render(request, template_name, context)

def delete_subject(request):
    subject_id = request.POST.get("subject_id")
    if not subject_id:
        request.session["error_message"] = "No subject ID found."
        return redirect("students:subjects")
    Subject.objects.filter(subject_id=subject_id).delete()
    request.session["message"] = "Deleted successfully"
    return redirect("students:subjects")


def subject_detail(request, subject_id):
    template_name = "subjects/subject_details.html"
    subject = get_object_or_404(Subject, subject_id=subject_id)
    teaches = TeacherClassSubjectCombination.objects.filter(subject=subject)
    context = {
        "subject": subject,
        "teaches": teaches,
    }
    return render(request, template_name, context)