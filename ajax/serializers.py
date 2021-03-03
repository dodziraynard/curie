from rest_framework import serializers
from students.models import Student, Subject, Klass
from staff.models import Staff


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
