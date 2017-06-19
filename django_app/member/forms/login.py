from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError('로그인 실패.')

        return self.cleaned_data
