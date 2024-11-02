from rest_framework import serializers
from .models import PersonalInformation, Customer, Driver


class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInformation
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = PersonalInformation(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):
    personal_information = PersonalInformationSerializer()

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        personal_info_data = validated_data.pop('personal_information')
        personal_info = PersonalInformationSerializer.create(PersonalInformationSerializer(),
                                                             validated_data=personal_info_data)
        customer, created = Customer.objects.update_or_create(personal_information=personal_info, **validated_data)
        return customer


class DriverSerializer(serializers.ModelSerializer):
    personal_information = PersonalInformationSerializer()

    class Meta:
        model = Driver
        fields = '__all__'

    def create(self, validated_data):
        personal_info_data = validated_data.pop('personal_information')
        personal_info = PersonalInformationSerializer.create(PersonalInformationSerializer(),
                                                             validated_data=personal_info_data)
        driver, created = Driver.objects.update_or_create(personal_information=personal_info, **validated_data)
        return driver
