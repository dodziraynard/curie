from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from dashboard.forms import HouseForm

from dashboard.mixins import CreateUpdateMixin
from dashboard.models import Staff, House


class HousesView(PermissionRequiredMixin, View):
    template_name = "dashboard/houses/houses.html"
    permission_required = [
        "dashboard.view_house",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        houses = House.objects.all()
        staff = Staff.objects.filter(has_left=False, user__is_active=True)
        print('staff', staff)
        context = {
            "houses": houses,
            "staff": staff,
        }
        return render(request, self.template_name, context)


class CreateUpdateHouseView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "dashboard/houses/edit_house.html"
    form_class = HouseForm
    object_id_field = "house_id"
    model_class = House
    object_name = "house"
    redirect_url = "dashboard:houses"
    permission_required = (
        "dashboard.add_house",
        "dashboard.change_house",
    )

    def get_context_data(self):
        return {
            "staff": Staff.objects.filter(has_left=False,
                                          user__is_active=True),
        }