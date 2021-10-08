# Generated by Django 3.2.6 on 2021-09-28 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_hotel_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('start_date', models.DateField(blank=True)),
                ('end_date', models.DateField(blank=True)),
                ('number_of_people', models.IntegerField(default=0)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.room')),
            ],
        ),
    ]