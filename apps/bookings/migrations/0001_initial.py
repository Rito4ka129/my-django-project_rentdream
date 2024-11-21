# Generated by Django 5.1.3 on 2024-11-21 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('confirmed', 'Подтверждено'), ('pending', 'Ожидает'), ('canceled', 'Отменено'), ('active', 'Активно'), ('inactive', 'Неактивно'), ('sold', 'Продано'), ('expired', 'Истекло'), ('under_offer', 'На предложении'), ('rejected', 'Отклонено'), ('draft', 'Черновик'), ('archived', 'Архивировано')], default='pending', max_length=50, null=True)),
            ],
        ),
    ]
