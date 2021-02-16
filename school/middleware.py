from school.models import School
from staff.models import Staff


class CustomMiddleWares(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        school = School.objects.first()
        # staff = Staff.objects.filter(has_left=False)
        # user_type = request.session.get("user_type", None)
        # alert = request.session.get("alert")
        request.school = school
        # request.alert = alert

        # if request.user.is_superuser:
        #     request.staff = staff
        # request.user_type = "".join(user_type.split()) if user_type else None
        return self.get_response(request)
