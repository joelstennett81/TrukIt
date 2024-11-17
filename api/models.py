from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from api.enums import *


class TrukItUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in GenderType])
    mailing_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    registration_date = models.DateField(auto_now_add=True)
    user_type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in UserType])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Customer(models.Model):
    truk_it_user = models.OneToOneField(TrukItUser, on_delete=models.PROTECT, related_name='customer')


class Driver(models.Model):
    truk_it_user = models.OneToOneField(TrukItUser, on_delete=models.PROTECT, related_name='driver')


class DriverInsurance(models.Model):
    driver = models.ForeignKey(TrukItUser, on_delete=models.PROTECT)
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

    def clean(self):
        super().clean()

        if self.expiration_date <= self.issue_date:
            raise ValidationError("Expiration date cannot be earlier than issue date")


class DriverTruck(models.Model):
    driver = models.ForeignKey(TrukItUser, on_delete=models.PROTECT)
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    vehicle_identification_number = models.CharField(max_length=17, unique=True)
    transmission = models.CharField(max_length=50)
    drive_type = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in DriveType])
    number_of_doors = models.PositiveSmallIntegerField(validators=[MinValueValidator(2), MaxValueValidator(8)])
    bed_length = models.FloatField(validators=[MinValueValidator(0)])
    bed_width = models.FloatField(validators=[MinValueValidator(0)])
    bed_height = models.FloatField(validators=[MinValueValidator(0)])
    fuel_type = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in FuelType])
    bed_cover = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in BedCoverType])
    tire_size = models.CharField(max_length=20)
    tailgate = models.BooleanField()
    navigation_type = models.CharField(max_length=50)
    ball_size = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in BallSizeType])
    tow_capacity = models.IntegerField(
        validators=[MinValueValidator(500)])  # Assuming minimum towing capacity of 500 lbs
    engine_size = models.CharField(max_length=30, choices=[(tag.name, tag.value) for tag in EngineSizeType])
    rear_glass_type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in RearGlassType])
    backseat_type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in BackSeatType])
    is_backseat_foldable = models.BooleanField()
    front_seat_type = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in FrontSeatType])
    is_front_seat_foldable = models.BooleanField()
    electrical_features = models.CharField(max_length=255)


class DriverTruckTrailer(models.Model):
    driver_truck = models.ForeignKey(DriverTruck, on_delete=models.PROTECT)
    has_trailer_lights = models.BooleanField()
    plug_type = models.CharField(max_length=50)


class DeliveryItem(models.Model):
    name = models.CharField(max_length=255)
    length = models.FloatField(validators=[MinValueValidator(0)])
    width = models.FloatField(validators=[MinValueValidator(0)])
    height = models.FloatField(validators=[MinValueValidator(0)])
    weight = models.FloatField(validators=[MinValueValidator(0)])
    description = models.CharField(max_length=500, blank=True, null=True)


class DeliveryEquipment(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500)


class DeliveryTransaction(models.Model):
    status = models.CharField(max_length=30, choices=[(tag.name, tag.value) for tag in DeliveryStatusType],
                              default='REQUESTED')
    pickup_location_address = models.CharField(max_length=255)
    delivery_location_address = models.CharField(max_length=255)
    customer_submit_timestamp = models.DateTimeField(auto_now_add=True)
    request_delivery_timestamp = models.DateTimeField()
    actual_delivery_timestamp = models.DateTimeField(null=True, blank=True)
    request_pickup_timestamp = models.DateTimeField()
    actual_pickup_timestamp = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, null=True, blank=True)
    items_to_be_delivered = models.ManyToManyField(
        'DeliveryItem',
        verbose_name='Items to be Delivered',
        blank=True,
        related_name='delivery_transactions'
    )

    equipment_needed = models.ManyToManyField(
        'DeliveryEquipment',
        verbose_name='Equipment Needed',
        blank=True,
        related_name='delivery_transactions'
    )

    def clean(self):
        super().clean()

        if self.actual_delivery_timestamp and self.request_delivery_timestamp > self.actual_delivery_timestamp:
            raise ValidationError("Actual delivery timestamp cannot be earlier than requested delivery timestamp")
        if self.actual_pickup_timestamp and self.request_pickup_timestamp > self.actual_pickup_timestamp:
            raise ValidationError("Actual pickup timestamp cannot be earlier than requested pickup timestamp")

    @property
    def miles_driven(self):
        return 10


class DeliveryTransactionItem(models.Model):
    transaction = models.ForeignKey('DeliveryTransaction', on_delete=models.CASCADE, related_name='transaction_items')
    item = models.ForeignKey('DeliveryItem', on_delete=models.CASCADE, related_name='transaction_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('transaction', 'item')


class DeliveryTransactionEquipment(models.Model):
    transaction = models.ForeignKey('DeliveryTransaction', on_delete=models.CASCADE,
                                    related_name='transaction_equipment')
    equipment = models.ForeignKey('DeliveryEquipment', on_delete=models.CASCADE, related_name='transaction_equipment')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('transaction', 'equipment')
