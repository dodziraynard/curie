from django.shortcuts import render, redirect
from school.models import School


def dashboard(request):
    template_name = "school/dashboard.html"
    context = {

    }
    return render(request, template_name, context)

def school(request):
    template_name = "school/school.html"
    if request.method == "POST":
        crest = request.FILES.get("crest")
        post_data = request.POST.copy()
        post_data.pop("csrfmiddlewaretoken")
        post_data.pop("crest", None)
        school_data = {k:v for k, v in post_data.items()}
        School.objects.all().update(**school_data)

        if crest:
            instance = School.objects.first()
            instance.crest = crest
            instance.save()

        return redirect("school:school")
      
    return render(request, template_name)