from django.forms import ModelForm
from .models import Order


class CreateOrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].empty_label = 'Книга не обрана'
        self.fields['book'].label = 'Оберіть книгу'

    class Meta:
        model = Order
        fields = ("book",)
