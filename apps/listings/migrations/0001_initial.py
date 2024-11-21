# Generated by Django 5.1.3 on 2024-11-21 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('num_rooms', models.IntegerField()),
                ('housing_type', models.CharField(choices=[('apartment', 'Квартира'), ('house', 'Дом'), ('duplex', 'Дуплекс'), ('studio', 'Студия'), ('cottage', 'Коттедж')], max_length=50)),
                ('status', models.CharField(choices=[('active', 'Активно'), ('inactive', 'Неактивно')], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]