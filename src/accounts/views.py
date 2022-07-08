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


class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            other_name = request.POST['last_name']
            email = request.POST['username']
            phone = request.POST['phone']
            gender = request.POST['gender']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:

                if User.objects.filter(phone=phone).exists():
                    messages.error(request, 'Phone number already exists.')
                    return redirect('create_user')
                else:
                    user = User(
                        first_name=first_name,
                        last_name=last_name,
                        other_name=other_name,
                        email=email,
                        phone=phone,
                        gender=gender,
                        password=password1,
                    )
            user.photo = request.FILES.get('photo')
            user.save()
            print(user)
            messages.success(request, 'user created successfully.')
            return redirect('dashboard:index')
