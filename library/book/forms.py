from django import forms
from .models import Book
from author.models import Author
from django.forms import inlineformset_factory
from authentication.models import CustomUser
from django.db.utils import OperationalError, ProgrammingError

# class CreateBookForm(forms.Form):
#     name = forms.CharField(max_length=128, required=True, label='Назва книги')
#     description = forms.CharField(max_length=256, required=True, label='Опис книги')
#     count = forms.IntegerField(label='Кількість книг', initial=10)
#     authors = forms.ModelMultipleChoiceField(Author.get_all(), label='Автори',
#                                              widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
#     year_publication = forms.IntegerField(required=False, initial=2002, label='Рік видавництва')
#     relized_at = forms.DateField(initial=None, required=False, label='Дата виходу')

class CreateBookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(Author.get_all(), label='Автори',
                                             widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors', 'year_publication', 'relized_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'count': forms.TextInput(attrs={'class': 'form-control'}),
            'year_publication': forms.TextInput(attrs={'class': 'form-control'}),
            'relized_at': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Назва книги',
            'description': "Опис книги",
            'count': "Кількість книг",
            'year_publication': 'Рік видавництва',
            'relized_at': 'Дата виходу',
        }


class UpdateBookForm(CreateBookForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['authors']


try:
    USER_CHOICES = [(user.pk, user.email) for user in CustomUser.objects.filter(role=0)]
except (OperationalError, ProgrammingError):
    USER_CHOICES = []


class UserBooksForm(forms.Form):
    user = forms.ChoiceField(choices=USER_CHOICES, label='Оберіть користувача')


class FilterBooksForm(forms.Form):
    books = forms.ModelMultipleChoiceField(Book.objects.all(), label='Обрати книги за назвою',
                                           widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
                                           required=False)
    authors = forms.ModelMultipleChoiceField(Author.objects.all(), label='Обрати авторів за назвою',
                                             widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
                                             required=False)
