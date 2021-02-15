from django.shortcuts import render, reverse, HttpResponse

import pdfkit


def student_transcript(request, student_id):
    template_name = "pdf_engine/student_transcript.html"
    context = {"student_id": student_id}
    return render(request, template_name, context)


def index(request):
    options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        "footer-center": "hello footer-center",
    }
    urls = []
    for id in range(3):
        url = "https://" if request.is_secure() else "http://"
        url += request.get_host()
        url += reverse("pdf_engine:student_transcript", args=[str(id)])
        urls.append(url)

    pdf = pdfkit.from_url(urls, False, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Student Transcript.pdf"'
    return response
