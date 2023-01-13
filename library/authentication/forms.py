from django import forms
from .models import CustomUser, ROLE_CHOICES
from django.contrib.auth.forms import UserCreationForm
from .signin import EmailAuthBackend


class UserLoginForm(forms.ModelForm):
    email = forms.EmailField(label='Електронна пошта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(label='Роль', widget=forms.Select(attrs={'class': 'form-control'}), choices=ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'role']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            role = self.cleaned_data.get('role')
            self.user_cache = EmailAuthBackend().authenticate(email=email, password=password, role=role)

    def get_user(self):
        return self.user_cache


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'middle_name', 'password', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'first_name': "Ім'я",
            'last_name': "Прізвище",
            'middle_name': "По батькові",
            'password': 'Пароль',
            'role': 'Роль'
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['middle_name'].required = False

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        middle_name = self.cleaned_data['middle_name']
        password = self.cleaned_data['password']
        role = self.cleaned_data['role']
        if commit:
            user.update(first_name=first_name,
                        last_name=last_name,
                        middle_name=middle_name,
                        password=password,
                        role=role,
                        )
        return user


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторіть введення пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'role')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'first_name': "Ім'я",
            'last_name': "Прізвище",
            'middle_name': "По батькові",
            'email': 'Електронна пошта',
            'role': 'Роль'
        }



