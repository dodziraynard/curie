from django.shortcuts import get_list_or_404, render, redirect, reverse, HttpResponse, get_object_or_404
from django.utils import timezone
from django.views import View
from dashboard.models import Student, Record, Klass
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from setup.models import SchoolSession
from .utils import render_to_pdf


class AcademicRecordReportView(PermissionRequiredMixin, View):
    template_name = "pdf_processor/report_per_session.html"
    permission_required = [
        "dashboard.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, session_id):
        classes = request.GET.getlist("classes")
        student_ids = request.GET.get("students")

        session = get_object_or_404(SchoolSession, pk=session_id)
        classes = Klass.objects.filter(class_id__in=classes)

        records = Record.objects.filter(session=session)
        if classes:
            records = records.filter(klass__class_id__in=classes)

        if student_ids:
            records = records.union(
                Record.objects.filter(session=session,
                                      student__student_id__in=student_ids))

        context = {
            "session": session,
            "records": records,
        }

        pdf = render_to_pdf(self.template_name, context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s.pdf" % ("Award Letter")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found", status=404)
