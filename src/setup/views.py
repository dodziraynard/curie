from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View

# Create your views here.

class IndexView(View):
    template_name = 'setup/index.html'
    permission_required = ('setup.can_setup_system')
    def get(self, request):
        users = get_user_model().objects.all()
        roles = Group.objects.all()
        context = {
            'roles':roles,
            'users':users,
        }
        return render(request, self.template_name, context)

class RoleManagementView(PermissionRequiredMixin, View):
    template_name = 'setup/roles_management.html'
    permission_required = ('setup.can_setup_system', 'setup.can_manage_roles' )

    @method_decorator(login_required())
    def get(self, request, role_id):
        role = get_object_or_404(Group, id=role_id)
        permissions = Permission.objects.all()
        user_permissions = permissions.filter(codename__contains = 'user')
        roles_permissions = permissions.filter(codename__contains = 'roles')
        group_permissions = permissions.filter(codename__contains = 'group')
        log_permissions = permissions.filter(codename__contains = 'log')
        permission_permission = permissions.filter(codename__contains = 'permission')
        contenttype_permission = permissions.filter(codename__contains = 'content')
        
        context = {
            "role": role,
            "permissions": permissions,
            'user_permissions':user_permissions,
            'roles_permissions':roles_permissions,
            'group_permissions':group_permissions,
            'log_permissions':log_permissions,
            'permission_permission':permission_permission,
            'contenttype_permission':contenttype_permission

        }
        return render(request, self.template_name, context)

    