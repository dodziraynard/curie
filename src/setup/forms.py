from django import forms
from django.contrib.auth.models import Group

from .models import (Attitude, Conduct, GradingSystem, Interest, SchoolSession,
                     Track)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            'name',
        ]


class AttitudeForm(forms.ModelForm):
    class Meta:
        model = Attitude
        exclude = [
            'id',
            'created_at',
            'updated_at',
        ]


class InterestFrom(forms.ModelForm):
    class Meta:
        model = Interest
        exclude = [
            'id',
            'created_at',
            'updated_at',
        ]


class ConductForm(forms.ModelForm):
    class Meta:
        model = Conduct
        exclude = [
            'id',
            'created_at',
            'updated_at',
        ]


class GradingSystemForm(forms.ModelForm):
    class Meta:
        model = GradingSystem
        exclude = [
            'id',
            'created_at',
            'updated_at',
        ]


class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        exclude = [
            'id',
            'created_at',
            'updated_at',
        ]


class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        exclude = [
            'id',
            'created_at',
            'updated_at',
        ]


class SchoolSessionForm(forms.ModelForm):
    class Meta:
        model = SchoolSession
        exclude = [
            'id',
            'created_at',
            'updated_at',
        ]
