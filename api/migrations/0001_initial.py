# Generated by Django 5.1.2 on 2024-11-04 06:24

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('length', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('width', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('height', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('weight', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrukItUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHER', 'OTHER')], max_length=20)),
                ('mailing_address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=20)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('user_type', models.CharField(choices=[('CUSTOMER', 'CUSTOMER'), ('DRIVER', 'DRIVER')], max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('truk_it_user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('truk_it_user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='driver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('REQUESTED', 'REQUESTED'), ('SCHEDULED', 'SCHEDULED'), ('IN_PROGRESS', 'IN PROGRESS'), ('COMPLETED', 'COMPLETED'), ('REJECTED', 'REJECTED')], default='REQUESTED', max_length=30)),
                ('pickup_location_address', models.CharField(max_length=255)),
                ('delivery_location_address', models.CharField(max_length=255)),
                ('customer_submit_timestamp', models.DateTimeField(auto_now_add=True)),
                ('request_delivery_timestamp', models.DateTimeField()),
                ('actual_delivery_timestamp', models.DateTimeField(blank=True, null=True)),
                ('request_pickup_timestamp', models.DateTimeField()),
                ('actual_pickup_timestamp', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.customer')),
                ('delivery_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_delivery_transaction', to='api.deliveryitem')),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.driver')),
            ],
        ),
        migrations.CreateModel(
            name='DriverInsurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('policy_name', models.CharField(max_length=200)),
                ('policy_number', models.CharField(max_length=50)),
                ('agent_name', models.CharField(max_length=100)),
                ('agent_phone_number', models.CharField(max_length=20)),
                ('agent_id_number', models.CharField(max_length=50)),
                ('coverage', models.CharField(choices=[('COMPLETE', 'COMPLETE'), ('COLLISION', 'COLLISION'), ('ROADSIDE', 'ROADSIDE'), ('LIABILITY', 'LIABILITY'), ('UNINSURED', 'UNINSURED')], max_length=255)),
                ('issue_date', models.DateField()),
                ('expiration_date', models.DateField()),
                ('policy_period', models.CharField(max_length=50)),
                ('content_coverage', models.TextField()),
                ('lien_holder_name', models.CharField(max_length=100)),
                ('lien_holder_account_number', models.CharField(max_length=50)),
                ('lien_holder_phone_number', models.CharField(max_length=20)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DriverTruck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2100)])),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('vehicle_identification_number', models.CharField(max_length=17, unique=True)),
                ('transmission', models.CharField(max_length=50)),
                ('drive_type', models.CharField(choices=[('REAR_WHEEL_DRIVE', 'RWD'), ('FOUR_WHEEL_DRIVE', '4WD'), ('ALL_WHEEL_DRIVE', 'AWD'), ('FRONT_WHEEL_DRIVE', 'FWD'), ('TWO_WHEEL_DRIVE', '2WD')], max_length=20)),
                ('number_of_doors', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(8)])),
                ('bed_length', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('bed_width', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('bed_height', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('fuel_type', models.CharField(choices=[('GAS', 'GAS'), ('HYBRID', 'HYBRID'), ('ELECTRIC', 'ELECTRIC'), ('DIESEL', 'DIESEL'), ('ETHANOL', 'ETHANOL')], max_length=20)),
                ('bed_cover', models.CharField(choices=[('OPEN', 'OPEN'), ('CAMPER', 'CAMPER'), ('COVERED', 'COVERED')], max_length=50)),
                ('tire_size', models.CharField(max_length=20)),
                ('tailgate', models.BooleanField()),
                ('navigation_type', models.CharField(max_length=50)),
                ('ball_size', models.CharField(choices=[('ONE_AND_THREE_FOURTHS', '1 3/4"'), ('TWO', '2"'), ('THREE', '3"'), ('PIN_AND_KEY', 'PIN and KEY')], max_length=50)),
                ('tow_capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(500)])),
                ('engine_size', models.CharField(choices=[('THREE_LITER', '3 LITER'), ('FIVE_LITER', '5 LITER'), ('V6', 'V6'), ('V8', 'V8')], max_length=30)),
                ('rear_glass_type', models.CharField(choices=[('SLIDE', 'SLIDE'), ('UP_DOWN', 'UP/DOWN'), ('REMOVABLE', 'REMOVABLE')], max_length=50)),
                ('backseat_type', models.CharField(choices=[('BUCKET_SEAT', 'BUCKET SEAT'), ('FOLD_DOWN', 'FOLD DOWN'), ('BENCH', 'BENCH'), ('SIXTY_FORTY', '60/40')], max_length=50)),
                ('is_backseat_foldable', models.BooleanField()),
                ('front_seat_type', models.CharField(choices=[('BUCKET_SEAT', 'BUCKET SEAT'), ('BENCH', 'BENCH')], max_length=50)),
                ('is_front_seat_foldable', models.BooleanField()),
                ('electrical_features', models.CharField(max_length=255)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DriverTruckTrailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_trailer_lights', models.BooleanField()),
                ('plug_type', models.CharField(max_length=50)),
                ('driver_truck', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.drivertruck')),
            ],
        ),
    ]