from django.shortcuts import render
from django.views import View


class IndexView(View):
    template_name = "website/index.html"

    def get(self, request):
        return render(request, self.template_name)


class AboutView(View):
    template_name = "website/about_us.html"

    def get(self, request):
        return render(request, self.template_name)


class ContactView(View):
    template_name = "website/contact.html"

    def get(self, request):
        return render(request, self.template_name)


class EnrollmentView(View):
    template_name = "website/enrollment.html"

    def get(self, request):
        return render(request, self.template_name)
