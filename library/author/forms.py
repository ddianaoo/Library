from django import forms
from .models import Author
from book.models import Book


class AuthorForm(forms.ModelForm):
    books = forms.ModelMultipleChoiceField(label='Книги', queryset=Book.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.fields['books'].required = False

    class Meta:
        model = Author
        fields = ['name', 'surname', 'patronymic', 'date_of_birth', 'date_of_death', 'books']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'date_of_death': forms.DateTimeInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': "Ім'я",
            'surname': "Прізвище",
            'patronymic': "По батькові",
            'date_of_birth': 'Дата народження',
            'date_of_death': 'Дата смерті',
        }


class AuthorUpdateForm(forms.ModelForm):
    books = forms.ModelMultipleChoiceField(label='Книги', queryset=Book.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(AuthorUpdateForm, self).__init__(*args, **kwargs)
        self.fields['books'].required = False

    class Meta:
        model = Author
        fields = ['name', 'surname', 'patronymic', 'date_of_birth', 'date_of_death', 'books']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'date_of_death': forms.DateTimeInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': "Ім'я",
            'surname': "Прізвище",
            'patronymic': "По батькові",
            'date_of_birth': 'Дата народження',
            'date_of_death': 'Дата смерті',
        }