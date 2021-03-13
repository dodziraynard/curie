from rest_framework import serializers
from students.models import *
from sms.models import SMS
from staff.models import Staff, HouseMaster


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["student_id", "surname", "other_names",
                  "sms_number", "my_class", "house"]


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = ["staff_id", "surname", "other_names",
                  "sms_number", "gender"]


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ["subject_id", "name", "is_elective", "student_count"]

class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Klass
        fields = ["class_id", "name", "stream", "form", "course_name", "class_teacher_name"]

class CourseSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Course
        fields = ["course_id", "name", "subjects"]


class HouseMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseMaster
        fields = ["id", "house", "house_master"]


class TeacherClassSubjectCombinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherClassSubjectCombination
        fields = ["id", "subject_name", "class_name", 'teacher']

class GradingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingSystem
        fields = "__all__"

class SMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMS
        fields = ['id', 'number', 'message', 'status', 'f_date']