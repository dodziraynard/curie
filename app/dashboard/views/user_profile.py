from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from accounts.models import User

from lms.utils.functions import make_model_key_value


class UserProfileIndexView(PermissionRequiredMixin, View):
    template_name = "dashboard/user_profile/profile.html"
    permission_required = []

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()
        context = {}
        context.update(make_model_key_value(user))
        return render(request, self.template_name, context)
    
    def post(self, request):
        gender = request.POST.get("gender")
        surname = request.POST.get("surname")
        other_names = request.POST.get("other_names")
        phone = request.POST.get("phone")
        
        user = User.objects.filter(id=request.user.id).first()
        user.gender = gender
        user.surname = surname
        user.other_names = other_names
        user.phone = phone
        user.save()
        return redirect(request.META.get("HTTP_REFERER"))

class UserProfilePhotoView(PermissionRequiredMixin, View):
    template_name = "dashboard/user_profile/photo.html"
    permission_required = []

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):

        context = {

        }

        return render(request, self.template_name, context)
