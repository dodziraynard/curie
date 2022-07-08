from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.models import User

from dashboard.mixins import CreateUpdateMixin
from dashboard.models import Staff
from lms.utils.functions import make_model_key_value
from django.contrib import messages


class StaffView(PermissionRequiredMixin, View):
    template_name = "dashboard/staff/staff.html"
    permission_required = [
        "dashboard.view_staff",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        staff = Staff.objects.all()
        context = {
            "staff": staff,
        }
        return render(request, self.template_name, context)


class CreateUpdateStaffView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "dashboard/staff/edit_staff.html"
    object_id_field = "staff_id"
    model_class = Staff
    object_name = "staff"
    redirect_url = "dashboard:staff"
    permission_required = (
        "dashboard.add_staff",
        "dashboard.change_staff",
    )

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        object_id = request.GET.get(self.object_id_field)
        obj = get_object_or_404(self.model_class, id=object_id)
        context = {
            self.object_name: obj,
        }
        if hasattr(self, "get_context_data"):
            context.update(self.get_context_data())
        context.update(make_model_key_value(obj))
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        staff_id = request.POST.get("staff_id") or -1
        username = request.POST.get("username")
        if not username:
            messages.error(request, "Username is required.")
        staff = Staff.objects.filter(id=staff_id).first()

        if not staff:
            user, _ = User.objects.get_or_create(username=username)
            user.set_password(user.temporal_pin)
            user.save()
            staff, _ = Staff.objects.get_or_create(staff_id=username, user=user)
        else:
            user = staff.user

        for key, value in request.POST.items():
            if key in ["staff_id"]: continue
            if hasattr(staff, key):
                setattr(staff, key, value)
                staff.save()
            elif hasattr(user, key):
                setattr(user, key, value)
                user.save()
        return redirect(self.redirect_url or "dashboard:index")