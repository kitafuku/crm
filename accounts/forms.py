from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput(attrs={'placeholder': 'example@email.com', 'autofocus': True}),
    )
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
    )


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput, min_length=8)
    password_confirm = forms.CharField(label='パスワード（確認）', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'role', 'is_active']
        labels = {
            'email': 'メールアドレス',
            'name': '氏名',
            'role': '権限',
            'is_active': '有効',
        }

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        pw2 = cleaned_data.get('password_confirm')
        if pw and pw2 and pw != pw2:
            self.add_error('password_confirm', 'パスワードが一致しません')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    password = forms.CharField(
        label='新しいパスワード',
        widget=forms.PasswordInput,
        required=False,
        min_length=8,
        help_text='変更しない場合は空欄のままにしてください',
    )
    password_confirm = forms.CharField(label='パスワード（確認）', widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'role', 'is_active']
        labels = {
            'email': 'メールアドレス',
            'name': '氏名',
            'role': '権限',
            'is_active': '有効',
        }

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        pw2 = cleaned_data.get('password_confirm')
        if pw and pw != pw2:
            self.add_error('password_confirm', 'パスワードが一致しません')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        pw = self.cleaned_data.get('password')
        if pw:
            user.set_password(pw)
        if commit:
            user.save()
        return user
