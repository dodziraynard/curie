from rest_framework import serializers
from students.models import Student, Subject


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["student_id", "surname", "other_names",
                  "sms_number", "my_class", "house"]


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ["subject_id", "name"]
