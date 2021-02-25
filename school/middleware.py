from school.models import School
from staff.models import Staff


class CustomMiddleWares(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        school = School.objects.first()
        request.school = school
        request.message = request.session.pop("message", "")
        request.error_message = request.session.pop("error_message", "")
        return self.get_response(request)
