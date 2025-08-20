from django import forms


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
