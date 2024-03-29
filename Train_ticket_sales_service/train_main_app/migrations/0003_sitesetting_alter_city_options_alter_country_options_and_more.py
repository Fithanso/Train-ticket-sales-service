# Generated by Django 4.1 on 2022-09-05 01:41

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('train_main_app', '0002_rename_customers_country_code_purchasedticket_customers_region_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Setting name')),
                ('value', models.CharField(max_length=100, verbose_name='Setting value')),
            ],
            options={
                'verbose_name': 'Setting',
                'verbose_name_plural': 'Settings',
                'db_table': 'settings',
            },
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['name'], 'verbose_name': 'City', 'verbose_name_plural': 'Cities'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['name'], 'verbose_name': 'Country', 'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Customer', 'verbose_name_plural': 'Customers'},
        ),
        migrations.AlterModelOptions(
            name='purchasedticket',
            options={'ordering': ['purchase_datetime'], 'verbose_name': 'Purchased ticket', 'verbose_name_plural': 'Purchased tickets'},
        ),
        migrations.AlterModelOptions(
            name='station',
            options={'ordering': ['name'], 'verbose_name': 'Station', 'verbose_name_plural': 'Stations'},
        ),
        migrations.AlterModelOptions(
            name='stationinvoyage',
            options={'verbose_name': 'Station in voyage', 'verbose_name_plural': 'Stations in voyage'},
        ),
        migrations.AlterModelOptions(
            name='train',
            options={'ordering': ['name'], 'verbose_name': 'Train', 'verbose_name_plural': 'Trains'},
        ),
        migrations.AlterModelOptions(
            name='voyage',
            options={'ordering': ['departure_datetime'], 'verbose_name': 'Voyage', 'verbose_name_plural': 'Voyages'},
        ),
        migrations.RemoveField(
            model_name='customer',
            name='country_code',
        ),
        migrations.AddField(
            model_name='customer',
            name='region_code',
            field=models.CharField(default=None, max_length=5, verbose_name='Region code'),
        ),
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='train_main_app.country', verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='city',
            name='photo',
            field=models.ImageField(null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Path to image'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='purchasedticket',
            name='arrival_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='arrival_st', to='train_main_app.stationinvoyage', verbose_name='Arrival station'),
        ),
        migrations.AlterField(
            model_name='purchasedticket',
            name='customers_phone_number',
            field=models.CharField(max_length=50, verbose_name='Customers phone numebr'),
        ),
        migrations.AlterField(
            model_name='purchasedticket',
            name='customers_region_code',
            field=models.CharField(default=None, max_length=5, verbose_name='Region code'),
        ),
        migrations.AlterField(
            model_name='purchasedticket',
            name='departure_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='departure_st', to='train_main_app.stationinvoyage', verbose_name='Departure station'),
        ),
        migrations.AlterField(
            model_name='purchasedticket',
            name='purchase_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of purchase'),
        ),
        migrations.AlterField(
            model_name='purchasedticket',
            name='seat_number',
            field=models.CharField(max_length=50, verbose_name='Seat number'),
        ),
        migrations.AlterField(
            model_name='purchasedticket',
            name='voyage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='train_main_app.voyage', verbose_name='Voyage'),
        ),
        migrations.AlterField(
            model_name='station',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='train_main_app.city', verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='station',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='station',
            name='photo',
            field=models.ImageField(null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Path to image'),
        ),
        migrations.AlterField(
            model_name='stationinvoyage',
            name='arrival_datetime',
            field=models.DateTimeField(verbose_name='Arrival time'),
        ),
        migrations.AlterField(
            model_name='stationinvoyage',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train_main_app.station', verbose_name='Station'),
        ),
        migrations.AlterField(
            model_name='stationinvoyage',
            name='station_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Station order'),
        ),
        migrations.AlterField(
            model_name='stationinvoyage',
            name='voyage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='train_main_app.voyage', verbose_name='Voyage'),
        ),
        migrations.AlterField(
            model_name='train',
            name='bc_wagons_numbers',
            field=models.CharField(default=0, max_length=255, verbose_name='Business Class wagons numbers'),
        ),
        migrations.AlterField(
            model_name='train',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='train',
            name='rows_number',
            field=models.SmallIntegerField(default=0, verbose_name='Rows in wagon'),
        ),
        migrations.AlterField(
            model_name='train',
            name='seats_in_row',
            field=models.SmallIntegerField(default=0, verbose_name='Seats in row'),
        ),
        migrations.AlterField(
            model_name='train',
            name='total_seats',
            field=models.SmallIntegerField(default=0, verbose_name='Total seats'),
        ),
        migrations.AlterField(
            model_name='train',
            name='wagons_number',
            field=models.SmallIntegerField(default=0, verbose_name='Wagons q-ty'),
        ),
        migrations.AlterField(
            model_name='voyage',
            name='arrival_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='arrival_city', to='train_main_app.city', verbose_name='Arrival city'),
        ),
        migrations.AlterField(
            model_name='voyage',
            name='arrival_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='arrival_station', to='train_main_app.station', verbose_name='Arrival station'),
        ),
        migrations.AlterField(
            model_name='voyage',
            name='bc_price_per_station',
            field=models.IntegerField(blank=True, default=0, verbose_name='Price per station for business class'),
        ),
        migrations.AlterField(
            model_name='voyage',
            name='departure_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='departure_city', to='train_main_app.city', verbose_name='Departure city'),
        ),
        migrations.AlterField(
            model_name='voyage',
            name='departure_datetime',
            field=models.DateTimeField(verbose_name='Departure time'),
        ),
        migrations.AlterField(
            model_name='voyage',
            name='departure_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='departure_station', to='train_main_app.station', verbose_name='Departure station'),
        ),
        migrations.AlterField(
            model_name='voyage',
            name='price_per_station',
            field=models.IntegerField(blank=True, default=0, verbose_name='Price per station'),
        ),
        migrations.AlterField(
            model_name='voyage',
            name='taken_seats',
            field=models.CharField(blank=True, max_length=2048, verbose_name='Taken seats'),
        ),
        migrations.AlterField(
            model_name='voyage',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='voyage',
            name='train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='train_main_app.train', verbose_name='Train'),
        ),
    ]
