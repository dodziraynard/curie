from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View


class IndexView(PermissionRequiredMixin, View):
    template_name = "dashboard/index.html"
    permission_required = [
        "setup.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return render(request, self.template_name)


class DeleteModelView(PermissionRequiredMixin, View):
    permission_required = [
        "setup.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, model_name, instance_id):
        return redirect("dashboard:index")

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, model_name, instance_id):
        # Get the model
        content_type = ContentType.objects.filter(model=model_name).first()
        if not content_type:
            raise PermissionDenied("Model not found")

        model_class = content_type.model_class()

        permission_name = f"{content_type.app_label}.delete_{model_name}"
        if not request.user.has_perm(permission_name):
            raise PermissionDenied()

        # Get the model instance
        res = model_class.objects.filter(id=instance_id).delete()
        if res and res[0]:
            messages.success(request, "Successfully deleted.")
        else:
            messages.info(request, "Item not found")

        return redirect(request.META.get("HTTP_REFERER"))
