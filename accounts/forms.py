from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CreateAccountForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "username",
                "class": "form-control",
            }
        ),
        label="Username",
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"type": "email", "id": "email", "class": "form-control"}
        ),
        label="Email Address",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        min_length=8,
        max_length=25,
        help_text="Password must be at least 8 characters",
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "id": "email",
                "class": "form-control",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "id": "password",
                "class": "form-control",
            }
        ),
    )
