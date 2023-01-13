from rest_framework import serializers
from datetime import datetime as dt, timedelta
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()
        fields['book'].initial = 3
        if self.instance:
            fields['user'].read_only = True
            fields['book'].read_only = True
            fields['plated_end_at'].read_only = True
        return fields
