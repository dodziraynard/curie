from django import forms

from accounts.models import Charge, Promotion, Store


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        exclude = [
            "logo",
            "approved_by",
            "created_by",
            "updated_by",
            "notified",
            "live",
            "approved",
            "created_at",
            "updated_at",
        ]


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
        exclude = [
            "created_at",
            "updated_at",
        ]


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        exclude = [
            "created_at",
            "updated_at",
            "approved",
        ]
