from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from dashboard.mixins import CreateUpdateMixin
from setup.forms import AttitudeForm, GroupForm, InterestForm, ConductForm, GradingSystemForm, SchoolSessionForm, TrackForm
from setup.models import Attitude, Conduct, GradingSystem, Interest, SchoolSession, Track


class IndexView(View):
    template_name = 'setup/index.html'
    permission_required = ('setup.can_setup_system')

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        users = get_user_model().objects.all()
        roles = Group.objects.all()
        interests = Interest.objects.all()
        conducts = Conduct.objects.all()
        attitudes = Attitude.objects.all()
        tracks = Track.objects.all()
        grading_systems = GradingSystem.objects.all()
        school_sessions = SchoolSession.objects.all()
        context = {
            'roles': roles,
            'users': users,
            'interests': interests,
            'conducts': conducts,
            'attitudes': attitudes,
            'tracks': tracks,
            'grading_systems': grading_systems,
            'school_sessions': school_sessions,
        }
        return render(request, self.template_name, context)


class RoleManagementView(PermissionRequiredMixin, View):
    template_name = 'setup/roles_management.html'
    permission_required = ('setup.can_setup_system', 'setup.can_manage_roles')

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, role_id):
        role = get_object_or_404(Group, id=role_id)
        permissions = Permission.objects.all()
        permissions = permissions.exclude(codename__contains='_session')
        permissions = permissions.exclude(codename__contains='_log')
        permissions = permissions.exclude(codename__contains='_permission')
        permissions = permissions.exclude(codename__contains='_content')

        context = {
            "role": role,
            "permissions": permissions.order_by('codename'),
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, role_id):
        role = get_object_or_404(Group, id=role_id)
        permissions_codes = request.POST.getlist("permissions")
        permissions = Permission.objects.filter(codename__in=permissions_codes)
        role.permissions.set(permissions)
        return redirect(request.META.get("HTTP_REFERER") or "setup:index")


class CreateUpdateGroup(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "setup/edit_role.html"
    form_class = GroupForm
    object_id_field = "role_id"
    model_class = Group
    redirect_url = "setup:index"
    object_name = "role"
    permission_required = (
        "setup.manage_setup",
        "auth.add_group",
        "auth.change_group",
    )


class CreateUpdateAttitudeView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "setup/edit_attitude.html"
    form_class = AttitudeForm
    object_id_field = "attitude_id"
    model_class = Attitude
    redirect_url = "setup:index"
    object_name = "attitude"
    permission_required = (
        "setup.manage_setup",
        "setup.add_attitude",
        "setup.change_attitude",
    )


class CreateUpdateConductView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "setup/edit_conduct.html"
    form_class = ConductForm
    object_id_field = "conduct_id"
    model_class = Conduct
    redirect_url = "setup:index"
    object_name = "conduct"
    permission_required = (
        "setup.manage_setup",
        "setup.add_conduct",
        "setup.change_conduct",
    )


class CreateUpdateInterestView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "setup/edit_interest.html"
    form_class = InterestForm
    object_id_field = "interest_id"
    model_class = Interest
    redirect_url = "setup:index"
    object_name = "interest"
    permission_required = (
        "setup.manage_setup",
        "setup.add_interest",
        "setup.change_interest",
    )


class CreateUpdateTrackView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "setup/edit_track.html"
    form_class = TrackForm
    object_id_field = "track_id"
    model_class = Track
    redirect_url = "setup:index"
    object_name = "track"
    permission_required = (
        "setup.manage_setup",
        "setup.add_track",
        "setup.change_track",
    )


class CreateUpdateSchoolSessionView(PermissionRequiredMixin,
                                    CreateUpdateMixin):
    template_name = "setup/edit_school_session.html"
    form_class = SchoolSessionForm
    object_id_field = "school_session_id"
    model_class = SchoolSession
    redirect_url = "setup:index"
    object_name = "school_session"
    permission_required = (
        "setup.manage_setup",
        "setup.add_schoolsession",
        "setup.change_schoolsession",
    )


class CreateUpdateGradingSystemView(PermissionRequiredMixin,
                                    CreateUpdateMixin):
    template_name = "setup/edit_grading_system.html"
    form_class = GradingSystemForm
    object_id_field = "grading_system_id"
    model_class = GradingSystem
    redirect_url = "setup:index"
    object_name = "grading_system"
    permission_required = (
        "setup.manage_setup",
        "setup.add_gradingsystem",
        "setup.change_gradingsystem",
    )


# class FormSimpleModelsView(PermissionRequiredMixin, View):
#     permission_required = [
#         "setup.manage_setup",
#     ]

#     @method_decorator(login_required(login_url="accounts:login"))
#     def post(self, request, model_name):
#         instance_id = request.POST.get("instance_id")
#         text = request.POST.get("text")

#         # Get the model
#         content_type = ContentType.objects.filter(model=model_name).first()
#         if not content_type:
#             raise PermissionDenied("Model not found")

#         model_class = content_type.model_class()
#         instance = model_class.objects.filter(id=instance_id).first()
#         if not instance:
#             instance = model_class.objects.create(text=text)
#         else:
#             instance.text = text
#         instance.save()

#         return redirect(request.META.get("HTTP_REFERER") or "setup:index")
