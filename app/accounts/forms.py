from django import forms

from .models import User


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "username",
            "surname",
            "other_names",
            "phone",
            "title",
            "photo",
            "gender",
        ]
