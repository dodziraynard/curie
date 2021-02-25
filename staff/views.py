from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from staff.models import Staff
from sheet_engine.functions import *
from django.db.utils import IntegrityError
from logger.utils import log_system_error


def staff(request):
    template_name = "staff/staff.html"
    context = {

    }
    return render(request, template_name, context)


def staff_admission(request):
    template_name = "staff/staff_admission.html"
    last_staff = Staff.objects.last()
    next_id = int(last_staff.staff_id) + \
        1 if last_staff and last_staff.staff_id.isnumeric() else ""
    context = {
        "last_id": last_staff.staff_id if last_staff else "",
        "next_id": next_id
    }
    if request.method == "GET":
        return render(request, template_name, context)

    elif request.method == "POST":
        post_data = request.POST.copy()
        post_data.pop("csrfmiddlewaretoken")
        has_class = isinstance(post_data.pop("has_class", False), list)

        # Is the staff info being edited?
        editing = post_data.pop("editing")[0]

        staff_data = {k: v.strip() for k, v in post_data.items()}
        staff_data.update({"has_class": has_class})
        staff_id = staff_data.get("staff_id")

        try:
            if editing:
                Staff.objects.filter(
                    staff_id=staff_id).update(**staff_data)
                new_staff = get_object_or_404(Staff, staff_id=staff_id)
            else:
                new_staff = Staff.objects.create(**staff_data)
        except IntegrityError as err:
            if "UNIQUE constraint failed" in str(err):
                context.update(
                    {"error_message": f"Staff with {staff_id} already exists."})
            else:
                log_system_error("staff_admission", str(err))
                context.update(
                    {"error_message": "Oops, an unknown error occurred."})
            context.update({
                k: v for k, v in request.POST.items()
            })
            return render(request, template_name, context)
        return redirect("staff:staff")


def staff_admission_sheet(request):
    template_name = "staff/staff_admission_sheet.html"
    context = {}
    if request.method == "GET":
        return render(request, template_name, context)
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            context.update({"error_message": "No file selected"})
            return render(request, template_name, context)

        # Returns True for success and string if error.
        res = insert_staff(file.file)
        if res == True:
            request.session["message"] = "Sucessfully added staff."
            return redirect("staff:staff")
        elif isinstance(res, str):
            context.update({"error_message": res})
        else:
            context.update({"error_message": "An unknown error occured."})
        return render(request, template_name, context)


def edit_staff(request, staff_id):
    template_name = "staff/staff_admission.html"
    staff = Staff.objects.values().get(staff_id=staff_id)
    context = {**staff}
    context.update({"editing": True})
    return render(request, template_name, context)
