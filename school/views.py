from django.shortcuts import render


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
    if request.method == "GET":
        context = {

        }
        return render(request, template_name, context)