from django.shortcuts import render, reverse, HttpResponse, get_object_or_404
from django.utils import timezone
import pdfkit
from students.models import Student, Record


def student_transcript(request, student_id):
    template_name = "pdf_engine/student_transcript.html"
    student = get_object_or_404(Student, student_id=student_id)
    records = Record.objects.filter(student=student)
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


def index(request):
    options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        # "footer-center": "hello footer-center",
    }
    urls = []
    for id in range(3):
        url = "https://" if request.is_secure() else "http://"
        url += request.get_host()
        url += reverse("pdf_engine:student_transcript", args=["111"])
        urls.append(url)
    pdf = pdfkit.from_url(urls, False, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="Student Transcript.pdf"'
    return response
