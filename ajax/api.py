from django.http import JsonResponse
from students.models import Student, Klass, Subject
from staff.models import Staff
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import StudentSerializer, SubjectSerializer, StaffSerializer


def get_student_teacher_count(request):
    students = Student.objects.filter(completed=False).count()
    teachers = Staff.objects.filter(has_left=False).count()
    return JsonResponse({"students": students, "teachers": teachers})


class ListStudentsAPI(APIView):
    def get(self, request):
        students = Student.objects.filter(completed=False)
        data = StudentSerializer(students, many=True).data
        return Response({"students": data})


class ListTeachersAPI(APIView):
    def get(self, request):
        teachers = Staff.objects.filter(has_left=False)
        data = StaffSerializer(teachers, many=True).data
        return Response({"teachers": data})


class ListSubjectsAPI(APIView):
    def get(self, request):
        filters = {k: v for k, v in request.GET.items()}
        klass = Klass.objects.get(**filters)
        subjects = klass.course.subjects.filter(is_elective=True)
        data = SubjectSerializer(subjects, many=True).data
        return Response({"subjects": data})
