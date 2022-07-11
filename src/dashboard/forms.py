from django import forms

from dashboard.models import Course, Department, House, Klass, Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = [
            "id",
            "created_at",
            "updated_at",
        ]


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = [
            "id",
            "created_at",
            "updated_at",
        ]


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        exclude = [
            "id",
            "created_at",
            "updated_at",
        ]


class ClassForm(forms.ModelForm):
    class Meta:
        model = Klass
        exclude = [
            "id",
            "created_at",
            "updated_at",
        ]


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        exclude = [
            "id",
            "created_at",
            "updated_at",
        ]
