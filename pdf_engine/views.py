from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.utils import timezone
import pdfkit
from students.models import Student, Record, Klass
import urllib


def generate_semester_report(request, student_id):
    template_name = "reports/semester_report.html"
    student = get_object_or_404(Student, student_id=student_id)
    semester = request.GET.get("semester")
    academic_year = request.GET.get("academic_year")

    records = Record.objects.filter(student=student, semester=semester, academic_year=academic_year)
    # forms = set([record.klass.form for record in records.distinct()])
    # semesters = set([record.semester for record in records.distinct()])
    if records:
        context = {
            "student": student,
            "records": records,
            "form": records.first().klass.form,
            "semester": semester,
            "current_time": timezone.now(),
        }
        return render(request, template_name, context)
    return HttpResponse(f"No records found for {academic_year} Academic Year, Semester {semester}")


def generate_semester_reports(request):
    if request.method == "GET":
        return redirect("pdf_engine:semester_reports")

    options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        # "footer-center": "hello footer-center",
    }

    class_id = request.POST.get("class_id")
    student_id = request.POST.get("student_id")
    academic_year = request.POST.get("academic_year")
    semester = request.POST.get("semester")

    pdf_urls = []
    if student_id:
        students = Student.objects.filter(student_id=student_id, completed=False)
    elif class_id:
        klass = get_object_or_404(Klass, class_id=class_id)
        students = Student.objects.filter(klass=klass, completed=False)

    for student in students:
        url = "https://" if request.is_secure() else "http://"
        url += request.get_host()
        url += reverse("pdf_engine:generate_semester_report", args=[student.student_id])
        url += '?' + urllib.parse.urlencode({"semester":semester, "academic_year":academic_year})
        pdf_urls.append(url)
    
    if len(pdf_urls) < 1:
        request.session['message'] = 'No students found.'
        return redirect("pdf_engine:semester_reports")

    pdf = pdfkit.from_url(pdf_urls, False, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="Student Transcript.pdf"'
    return response









def student_transcript(request, student_id):
    template_name = "pdf_engine/student_transcript.html"
    student = get_object_or_404(Student, student_id=student_id)
    semester = request.GET.get("semester")
    academic_year = request.GET.get("academic_year")

    records = Record.objects.filter(student=student, semester=semester, academic_year=academic_year)
    forms = set([record.klass.form for record in records.distinct()])
    semesters = set([record.semester for record in records.distinct()])
    context = {
        "student": student,
        "records": records,
        "forms": forms,
        "semesters": semesters,
        "current_time": timezone.now(),
    }
    return render(request, template_name, context)


def semester_reports(request):
    template_name = "reports/home.html"
    context = {
        "classes":Klass.objects.all(),
    }
    return render(request, template_name, context)