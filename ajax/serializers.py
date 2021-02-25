from rest_framework import serializers
from students.models import Student, Subject
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
        fields = ["subject_id", "name"]
