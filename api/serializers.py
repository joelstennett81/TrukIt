from rest_framework import serializers
from .models import *


class TrukItUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrukItUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = TrukItUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):
    truk_it_user = TrukItUserSerializer()

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        truk_it_user_data = validated_data.pop('truk_it_user')
        truk_it_user = TrukItUserSerializer.create(TrukItUserSerializer(),
                                                   validated_data=truk_it_user_data)
        customer, created = Customer.objects.update_or_create(truk_it_user=truk_it_user, **validated_data)
        return customer


class DriverSerializer(serializers.ModelSerializer):
    truk_it_user = TrukItUserSerializer()

    class Meta:
        model = Driver
        fields = '__all__'

    def create(self, validated_data):
        truk_it_user_data = validated_data.pop('truk_it_user')
        truk_it_user = TrukItUserSerializer.create(TrukItUserSerializer(),
                                                   validated_data=truk_it_user_data)
        driver, created = Driver.objects.update_or_create(truk_it_user=truk_it_user, **validated_data)
        return driver


class DeliveryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryItem
        fields = '__all__'


class DeliveryTransactionSerializer(serializers.ModelSerializer):
    items = DeliveryItemSerializer(many=True, read_only=True)

    class Meta:
        model = DeliveryTransaction
        fields = ['id', 'pickup_location_address', 'delivery_location_address', 'request_delivery_timestamp',
                  'request_pickup_timestamp', 'items']
