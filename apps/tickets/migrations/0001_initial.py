# Generated by Django 5.1.3 on 2024-11-21 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('available', 'Available'), ('booked', 'Booked')], default='available', max_length=10)),
                ('user_name', models.CharField(max_length=120)),
                ('contact', models.CharField(max_length=120)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='booking.booking')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
