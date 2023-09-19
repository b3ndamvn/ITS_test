from rest_framework import generics
from rest_framework.response import Response
import decimal
import math

from .models import MoneyUser
from .serializers import MoneyUserSerializer, MoneyPipeSerializer


class ListMoneyUserAPIView(generics.ListCreateAPIView):
    queryset = MoneyUser.objects.all()
    serializer_class = MoneyUserSerializer


class MoneyPipeAPIView(generics.GenericAPIView):
    serializer_class = MoneyPipeSerializer

    def post(self, request, *args, **kwargs):
        # TODO: узнать, необходимо ли добавить понятную обработку ошибки на случай отсутствия id отправителя в базе
        if "destination" not in request.data:
            return Response({"Error": "Ошибка! Укажите получателя денег"}, status=400)
        if not request.data['value'].isdecimal():
            return Response({"Error": "Ошибка! Неверный формат ввода суммы перевода"}, status=400)
        if not MoneyPipeSerializer(data=request.data).is_valid(raise_exception=False):
            return Response({"Error": "Ошибка! Проверьте правильность введенных данных"}, status=400)

        user = MoneyUser.objects.filter(pk=request.data['source']).first()
        dest_users = MoneyUser.objects.filter(INN__in=request.data['destination'])

        if not dest_users:
            return Response({"Error": "Ошибка! Пользователей с указанным ИНН нет"}, status=400)
        if user in dest_users:
            return Response({"Error": "Ошибка! Вы не можете отправлять деньги на этот же счет"}, status=400)
        if not user.check_enough_balance(request.data['value']):
            return Response({"Error": "Ошибка! Не хватает средств"}, status=400)

        for dest_user in dest_users:
            operation_balance = decimal.Decimal(math.floor(float(request.data['value']) / len(dest_users) * 100) / 100)
            dest_user.balance += operation_balance
            user.balance -= operation_balance
            dest_user.save()
            user.save()
        return Response({"Успех": "Сделано!"}, status=201)
