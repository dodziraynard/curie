from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.forms import UserForm
from lms.utils.functions import make_model_key_value
from django.utils.html import strip_tags

from accounts.models import User


class ProfileView(View):
    """View the profile of currently logged in user. Uses the same base template as the dashboard."""
    template_name = 'accounts/profile.html'

    def get(self, request):
        return render(request, self.template_name, {'user': request.user})


class UsersView(PermissionRequiredMixin, View):
    template_name = 'accounts/users/users.html'
    permission_required = [
        "accounts.view_user",
    ]

    def get(self, request):
        users = User.objects.all()
        context = {
            'users': users,
        }
        return render(request, self.template_name, context)


class CreateUpdatUserView(PermissionRequiredMixin, View):
    template_name = "accounts/users/edit_user.html"
    form_class = UserForm
    object_id_field = "id"
    model_class = User
    object_name = "user"
    redirect_url = "accounts:users"
    permission_required = (
        "accounts.add_user",
        "accounts.change_user",
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
        object_id = request.POST.get(self.object_id_field) or -1
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.danger(request, "Passwords do not match.")
            return render(request, self.template_name, context)

        obj = self.model_class.objects.filter(id=object_id).first()
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            user = form.save()
            user.changed_password = True
            user.set_password(password)
            user.save()
            return redirect(self.redirect_url or "dashboard:index")
        else:
            for field, error in form.errors.items():
                message = f"{field.title()}: {strip_tags(error)}"
                break
            context = {k: v for k, v in request.POST.items()}
            if hasattr(self, "get_context_data"):
                context.update(self.get_context_data())
            messages.warning(request, message)
            return render(request, self.template_name, context)


class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_ = request.GET.get('next')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_ or "dashboard:index")
        else:
            message = 'Invalid credentials. Please try again.'
            messages.error(request, message)
            context = {k: v for k, v in request.POST.items()}
            return render(request, self.template_name, context)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('accounts:login')
