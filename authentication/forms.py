from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(label=_('Email Address'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    def clean(self):
        user = User.objects.filter(email=self.cleaned_data['email']).first()

        if user is None:
            raise forms.ValidationError("Unknown user or password")

        if not user.check_password(self.cleaned_data['password']):
            raise forms.ValidationError("Unknown user or password")


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password2 != password:
            raise forms.ValidationError('Passwords mismatch')
        return password2

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user
