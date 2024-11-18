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


class DeliveryEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryEquipment
        fields = '__all__'


class DeliveryTransactionSerializer(serializers.ModelSerializer):
    items = DeliveryItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = DeliveryTransaction
        fields = ['id', 'pickup_location_address', 'delivery_location_address', 'request_delivery_timestamp',
                  'request_pickup_timestamp', 'actual_delivery_timestamp', 'actual_pickup_timestamp', 'customer',
                  'driver', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        driver_data = validated_data.pop('driver', None)
        user_id = self.context['request'].user.id
        customer = Customer.objects.get(truk_it_user_id=user_id)
        validated_data['customer'] = customer

        transaction = DeliveryTransaction.objects.create(
            **validated_data
        )

        if items_data:
            DeliveryTransactionItem.objects.bulk_create([
                DeliveryTransactionItem(transaction=transaction, item=item, quantity=q)
                for item, q in items_data
            ])

        if driver_data:
            Driver.objects.get_or_create(user__id=driver_data['id'], defaults=driver_data)
            transaction.driver = Driver.objects.get(id=driver_data['id'])

        transaction.save()
        return transaction

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        driver_data = validated_data.pop('driver', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if items_data:
            DeliveryTransactionItem.objects.filter(transaction=instance).exclude(
                id__in=[item['id'] for item in items_data]).delete()
            DeliveryTransactionItem.objects.bulk_create([
                DeliveryTransactionItem(transaction=instance, item=item, quantity=q)
                for item, q in items_data
            ])

        if driver_data:
            Driver.objects.get_or_create(user__id=driver_data['id'], defaults=driver_data)
            instance.driver = Driver.objects.get(id=driver_data['id'])

        instance.save()
        return instance
