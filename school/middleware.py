from school.models import School
from staff.models import Staff


class CustomMiddleWares(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        school = School.objects.first()
        request.school = school
        request.message =  request.session.get("message", "")
        return self.get_response(request)
