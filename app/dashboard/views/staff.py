from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q

from dashboard.mixins import CreateUpdateMixin
from dashboard.models import Staff
from lms.utils.functions import make_model_key_value

User = get_user_model()


class StaffView(PermissionRequiredMixin, View):
    template_name = "dashboard/staff/staff.html"
    permission_required = [
        "setup.view_staff",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        staff = Staff.objects.filter(deleted=False)
        query = request.GET.get("query")

        if query:
            staff = staff.filter(
                Q(staff_id__icontains=query)
                | Q(user__surname__icontains=query)
                | Q(user__other_names__icontains=query))

        context = {
            "staff": staff,
            **{k: v
               for k, v in request.GET.items()},
        }
        return render(request, self.template_name, context)


class CreateUpdateStaffView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "dashboard/staff/edit_staff.html"
    object_id_field = "staff_id"
    model_class = Staff
    object_name = "staff"
    redirect_url = "dashboard:staff"
    permission_required = (
        "setup.add_staff",
        "setup.change_staff",
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
        context.update(make_model_key_value(obj.user))
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        staff_id = request.POST.get("staff_id") or -1
        username = request.POST.get("username")
        if not username:
            messages.error(request, "Username is required.")
            return redirect(self.redirect_url or "dashboard:index")

        staff = Staff.objects.filter(id=staff_id).first()

        if not staff:
            user, _ = User.objects.get_or_create(username=username)
            user.set_password(user.temporal_pin)
            user.save()
            staff, _ = Staff.objects.get_or_create(staff_id=username,
                                                   user=user)
        else:
            user = staff.user

        for key, value in [*request.POST.items(), *request.FILES.items()]:
            if key in ["staff_id"]: continue
            if hasattr(staff, key):
                setattr(staff, key, value)
                staff.save()
            elif hasattr(user, key):
                setattr(user, key, value)
                user.save()
        return redirect(self.redirect_url or "dashboard:index")