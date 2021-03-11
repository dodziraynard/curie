from django.http import JsonResponse
from students.models import Student, Klass, Subject, Course, TeacherClassSubjectCombination
from staff.models import Staff, HouseMaster
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import *


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


class ListClassSubjectsAPI(APIView):
    def get(self, request):
        filters = {k: v for k, v in request.GET.items()}
        klass = Klass.objects.get(**filters)
        subjects = klass.course.subjects.filter(is_elective=True)
        data = SubjectSerializer(subjects, many=True).data
        return Response({"subjects": data})

class ListAllSubjectsAPI(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        data = SubjectSerializer(subjects, many=True).data
        return Response({"subjects": data})

class ListClassesAPI(APIView):
    def get(self, request):
        classes = Klass.objects.exclude(class_teacher=None)
        data = ClassSerializer(classes, many=True).data
        return Response({"classes": data})

class ListCoursesAPI(APIView):
    def get(self, request):
        courses = Course.objects.all()
        data = CourseSerializer(courses, many=True).data
        return Response({"courses": data})

        
class LisHouseMastersAPI(APIView):
    def get(self, request):
        house_masters = HouseMaster.objects.all()
        data = HouseMasterSerializer(house_masters, many=True).data
        return Response({"house_masters": data})


class TeacherClassSubjectCombinationsAPI(APIView):
    def get(self, request):
        teachers_subjects = TeacherClassSubjectCombination.objects.all()
        data = TeacherClassSubjectCombinationSerializer(teachers_subjects, many=True).data
        return Response({"teachers_subjects": data})
