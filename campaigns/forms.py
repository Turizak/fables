from django import forms
from django.core.exceptions import ValidationError


class CreateCampaignForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "name",
                "placeholder": "Enter campaign name",
                "class": "form-control",
                "required": True,
            }
        ),
        label="Campaign Name",
    )

    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "date", "id": "start_date", "class": "form-control"}
        ),
        label="Start Date",
    )

    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "date", "id": "end_date", "class": "form-control"}
        ),
        label="End Date",
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date.")

        return cleaned_data
