# Generated by Django 2.1 on 2019-05-09 13:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=200)),
                ('secret', models.CharField(max_length=20)),
                ('admintype', models.IntegerField()),
                ('status', models.IntegerField()),
                ('createdate', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='AdminType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.CharField(max_length=500)),
                ('phone', models.CharField(blank=True, max_length=500)),
                ('address', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.CharField(max_length=500)),
                ('phone', models.CharField(blank=True, max_length=500)),
                ('address', models.CharField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('short_description', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='meal_images/')),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500)),
                ('total', models.IntegerField()),
                ('status', models.IntegerField(choices=[(1, 'Cooking'), (2, 'Ready'), (3, 'On the way'), (4, 'Delivered')])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('picked_at', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Customer')),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('sub_total', models.IntegerField()),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Meal')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='models.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('phone', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to='restaurant_logo/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('secret', models.CharField(max_length=200)),
                ('usertype', models.IntegerField(default=0)),
                ('address', models.CharField(max_length=500)),
                ('phone', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=200)),
                ('isemailverified', models.IntegerField(default=0)),
                ('isphoneverified', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('createdate', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='models.User'),
        ),
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Restaurant'),
        ),
        migrations.AddField(
            model_name='meal',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal', to='models.Restaurant'),
        ),
        migrations.AddField(
            model_name='driver',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='models.User'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='models.User'),
        ),
    ]
