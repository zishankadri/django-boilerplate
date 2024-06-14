from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccount
from .utils import generate_ref_code

class UserAccountForm(UserCreationForm):
    # password1 = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ['email', 'password1', 'password2', 'subject']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Add custome css class to all input widgets.
        for field_name, field in self.fields.items():
            current_class = field.widget.attrs.get('class') or ''
            field.widget.attrs['class'] = current_class+" "+'regular-input'

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email_auth_token = generate_ref_code()

        if commit:
            user.save()
        return user
