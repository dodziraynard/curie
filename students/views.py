from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from students.models import Student, Klass, Subject
from sheet_engine.functions import *
from django.db.utils import IntegrityError
from logger.utils import log_system_error

def students(request):
    template_name = "students/students.html"
    context = {

    }
    return render(request, template_name, context)


def student_admission(request):
    template_name = "students/student_admission.html"
    last_student = Student.objects.last()
    next_id = int(last_student.student_id) + 1 if last_student and last_student.student_id.isnumeric() else ""
    context = {
            "classes": Klass.objects.all(),
            "last_id": last_student.student_id if last_student else "",
            "next_id":next_id
        }
    if request.method == "GET":
        return render(request, template_name, context)

    elif request.method == "POST":
        post_data = request.POST.copy()
        post_data.pop("csrfmiddlewaretoken")
        electives = post_data.pop("electives")

        # Is the student info being edited?
        editing = post_data.pop("editing")[0]

        klass = get_object_or_404(Klass,class_id=post_data.pop("klass")[0])
        student_data = {k:v.strip() for k,v in post_data.items()}
        student_data.update({"klass":klass})
        electives = Subject.objects.filter(subject_id__in=electives)
        student_id = student_data.get("student_id")

        try:
            if editing:
                Student.objects.filter(student_id=student_id).update(**student_data)
                new_student = get_object_or_404(Student,student_id=student_id)
            else:
                new_student = Student.objects.create(**student_data)
        except IntegrityError as err:
            if "UNIQUE constraint failed" in str(err):
                context.update({"error_message": f"Student with {student_id} already exists."})
            else:
                log_system_error("student_admission", str(err))
                context.update({"error_message": "Oops, an unknown error occurred."})
            context.update({
                k:v for k,v in request.POST.items()
            })
            return render(request, template_name, context)
        new_student.electives.set(electives)
        return redirect("students:students")

def student_admission_sheet(request):
    template_name = "students/student_admission_sheet.html"
    context = {}
    if request.method == "GET":
        return render(request, template_name, context)
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            context.update({"error_message":"No file selected"})
            return render(request, template_name, context)
        
        # Returns True for success and string if error.
        res = insert_students(file.file)
        if res == True:
            request.session["message"] = "Sucessfully added students."
            return redirect("students:students")
        elif isinstance(res, str):
            context.update({"error_message": res})
        else:
            context.update({"error_message":"An unknown error occured."})
        return render(request, template_name, context)

def edit_student(request, student_id):
    template_name = "students/student_admission.html"
    student = Student.objects.values().get(student_id=student_id)
    student_electives = Student.objects.get(student_id=student_id).electives.all()
    electives = Student.objects.get(student_id=student_id).klass.course.subjects.filter(is_elective=True)
    context = {**student}
    context.update({
        "editing":True,
        "classes": Klass.objects.all(),
        "student_electives":student_electives,
        "electives":electives,
    })
    return render(request, template_name, context)