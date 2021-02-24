from django.shortcuts import render, redirect, get_object_or_404
from students.models import Student, Klass, Subject
from django.db.utils import IntegrityError
from logger.utils import log_system_error


def dashboard(request):
    template_name = "school/dashboard.html"
    context = {

    }
    return render(request, template_name, context)


def students(request):
    template_name = "school/students.html"
    context = {

    }
    return render(request, template_name, context)


def student_admission(request):
    template_name = "school/student_admission.html"
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

        klass = get_object_or_404(Klass,class_id=post_data.pop("klass")[0])
        student_data = {k:v.strip() for k,v in post_data.items()}
        student_data.update({"klass":klass})
        electives = Subject.objects.filter(subject_id__in=electives)

        try:
            new_student = Student.objects.create(**student_data)
        except IntegrityError as err:
            if "UNIQUE constraint failed" in str(err):
                id = student_data.get("student_id")
                context.update({"error_message": f"Student with {id} already exists."})
            else:
                log_system_error("student_admission", str(err))
                context.update({"error_message": "Oops, an unknown error occurred."})
            context.update({
                k:v for k,v in request.POST.items()
            })
            return render(request, template_name, context)
        new_student.electives.set(electives)
        return redirect("school:student_admission")

def student_admission_sheet(request):
    template_name = "school/student_admission_sheet.html"
    last_student = Student.objects.last()
    context = {
           
        }
    if request.method == "GET":
        return render(request, template_name, context)