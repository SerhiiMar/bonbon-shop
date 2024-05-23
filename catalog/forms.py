from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter a valid username"
            }
        )
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password"
            }
        )
    )


class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "city")


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        label="",
        coerce=int
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
    redirect_url = forms.CharField(
        required=False,
        widget=forms.HiddenInput
    )

    class Meta:
        fields = ("quantity", "override")
