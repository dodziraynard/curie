from django import forms

from dashboard.models import Course, Department, House, Klass, Subject, Inventory, Issuance


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


class InventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory
        exclude = [
            "id",
            "created_at",
            "updated_at",
            "created_by",
        ]


class IssuanceForm(forms.ModelForm):

    class Meta:
        model = Issuance
        exclude = [
            "id",
            "recipient",
            "created_at",
            "updated_by",
            "issued_by",
            "updated_at",
        ]
