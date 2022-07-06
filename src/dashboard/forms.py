from django import forms

from dashboard.models import Programme


class ProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        exclude = [
            "id",
            "created_at",
            "projects",
            "updated_at",
        ]
