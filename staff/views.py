from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from staff.models import Staff
from sheet_engine.functions import *
from django.db.utils import IntegrityError
from logger.utils import log_system_error
from sheet_engine.functions import (generate_subject_staff_combinations,
                                    insert_subject_staff_combination,
                            )
from students.models import TeacherClassSubjectCombination

def staff(request):
    template_name = "staff/staff.html"
    context = {

    }
    return render(request, template_name, context)


def new_staff(request):
    template_name = "staff/new_staff.html"
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
                log_system_error("new_staff", str(err))
                context.update(
                    {"error_message": "Oops, an unknown error occurred."})
            context.update({
                k: v for k, v in request.POST.items()
            })
            return render(request, template_name, context)
        return redirect("staff:staff")


def new_staff_sheet(request):
    template_name = "staff/new_staff_sheet.html"
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
    template_name = "staff/new_staff.html"
    staff = Staff.objects.values().get(staff_id=staff_id)
    context = {**staff}
    context.update({"editing": True})
    return render(request, template_name, context)


def delete_staff(request):
    staff_id = request.POST.get("staff_id")
    if not staff_id:
        request.session["error_message"] = "No staff ID found."
        return redirect("staff:staff")
    Staff.objects.filter(staff_id=staff_id).delete()
    request.session["message"] = "Deleted successfully"
    return redirect("staff:staff")


def staff_detail(request, staff_id):
    template_name = "staff/staff_details.html"
    staff = get_object_or_404(Staff, staff_id=staff_id)
    context = {
        "staff": staff
    }
    return render(request, template_name, context)

def teachers_subjects(request):
    template_name = "staff/teachers_subjects.html"
    if request.method == "GET":
        url = generate_subject_staff_combinations()
        context = {
            "url":url,
        }
        return render(request, template_name, context)
    elif request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            request.session["error_message"] = "No file selected."
            return redirect("staff:teachers_subjects")

        res = insert_subject_staff_combination(file.file)
        if isinstance(res, str):
            request.session["error_message"] = res
        elif res == False:
            request.session['error_message'] = "Something went wrong. We will fix it."
        else:
            request.session["message"] = "Records updated successfully."
        return redirect("staff:teachers_subjects")

def edit_teacher_subject(request, id):
    template_name = "staff/edit_teacher_subject.html"
    teacher_subject = get_object_or_404(TeacherClassSubjectCombination, id=id)
    teachers = Staff.objects.filter(has_left=False)
    context = {
        "teacher_subject":teacher_subject,
        'teachers':teachers
    }
    if request.method == "GET":
        return render(request, template_name, context)
    elif request.method == "POST":
        staff_id = request.POST.get("staff_id")
        staff = get_object_or_404(Staff, staff_id=staff_id)
        teacher_subject.staff = staff
        teacher_subject.save()
        request.session['message'] = "Update successful."
        return redirect("staff:teachers_subjects")

    

def delete_teacher_subject(request):
    id = request.POST.get("id")
    TeacherClassSubjectCombination.objects.filter(id=id).delete()
    return redirect("staff:teachers_subjects")