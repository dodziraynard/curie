from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View

from accounts.models import User


class ProfileView(View):
    """View the profile of currently logged in user. Uses the same base template as the dashboard."""
    template_name = 'accounts/profile.html'

    def get(self, request):
        return render(request, self.template_name, {'user': request.user})


class UsersView(View):
    template_name = 'accounts/users/users.html'

    def get(self, request):
        users = User.objects.all()
        context = {
            'users': users,
        }
        return render(request, self.template_name, context)


class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard:index")
        else:
            message = 'Invalid credentials. Please try again.'
            messages.error(request, message)
            context = {k: v for k, v in request.POST.items()}
            return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')
