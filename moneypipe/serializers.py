from rest_framework import serializers
from .models import MoneyUser


class MoneyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyUser
        fields = ('id', 'name', 'lastname', 'INN', 'balance')


class MoneyPipeSerializer(serializers.Serializer):
    source = serializers.PrimaryKeyRelatedField(queryset=MoneyUser.objects.all())
    destination = serializers.ListField(child=serializers.CharField())
    value = serializers.DecimalField(decimal_places=2, max_digits=20)
