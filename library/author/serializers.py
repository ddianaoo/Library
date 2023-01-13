from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['url', 'id', 'name', 'surname', 'patronymic', 'date_of_birth', 'date_of_death', 'books']
