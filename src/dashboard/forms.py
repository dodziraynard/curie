from django import forms

from dashboard.models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = [
            "id",
            "created_at",
            "updated_at",
        ]
