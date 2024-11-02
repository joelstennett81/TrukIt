from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.hashers import make_password
from api.enums import *


class PersonalInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in GenderType])
    mailing_address = models.TextField()
    mailing_address_two = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    registration_date = models.DateField()
    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in UserType])

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return self.password == make_password(raw_password)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Customer(models.Model):
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.PROTECT)


class Driver(models.Model):
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.PROTECT)


class DriverInsurance(models.Model):
    driver = models.ForeignKey(PersonalInformation, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    policy_name = models.CharField(max_length=200)
    policy_number = models.CharField(max_length=50)
    agent_name = models.CharField(max_length=100)
    agent_phone_number = models.CharField(max_length=20)
    agent_id_number = models.CharField(max_length=50)
    coverage = models.CharField(max_length=255, choices=[(tag.name, tag.value) for tag in InsuranceCoverageType])
    issue_date = models.DateField()
    expiration_date = models.DateField()
    policy_period = models.CharField(max_length=50)
    content_coverage = models.TextField()
    lien_holder_name = models.CharField(max_length=100)
    lien_holder_account_number = models.CharField(max_length=50)
    lien_holder_phone_number = models.CharField(max_length=20)


class DriverTruck(models.Model):
    year = models.IntegerField()
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    vehicle_identification_number = models.CharField(max_length=17)
    transmission = models.CharField(max_length=50)
    drive_type = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in DriveType])
    number_of_doors = models.PositiveIntegerField()
    bed_length = models.FloatField()
    bed_width = models.FloatField()
    bed_height = models.FloatField()
    fuel_type = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in FuelType])
    bed_cover = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in BedCoverType])
    tire_size = models.CharField(max_length=20)
    tailgate = models.BooleanField()
    navigation_type = models.CharField(max_length=50)
    ball_size = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in BallSizeType])
    tow_capacity = models.IntegerField()
    engine_size = models.CharField(max_length=30, choices=[(tag.name, tag.value) for tag in EngineSizeType])
    rear_glass_type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in RearGlassType])
    backseat_type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in BackSeatType])
    is_backseat_foldable = models.BooleanField()
    front_seat_type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in FrontSeatType])
    is_front_seat_foldable = models.BooleanField()
    electrical_features = models.CharField(max_length=255)


class DriverTruckTrailer(models.Model):
    has_trailer_lights = models.BooleanField()
    plug_type = models.CharField(max_length=50)
