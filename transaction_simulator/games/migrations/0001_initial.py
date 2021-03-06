# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 22:24
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boundaries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crisis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('radius', models.DecimalField(decimal_places=6, max_digits=14)),
                ('origin', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('zone', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
                ('country', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crises', to='boundaries.Country', verbose_name='country')),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('home_country', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='donors', to='boundaries.Country', verbose_name='country')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('number_of_turns', models.IntegerField(blank=True, default=10, null=True)),
                ('description', models.CharField(blank=True, default='', max_length=2000, null=True)),
                ('crisis', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='games.Crisis')),
                ('donor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='games.Donor')),
            ],
        ),
        migrations.CreateModel(
            name='Household',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('admin_level_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boundaries.Admin_Level_1')),
                ('admin_level_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boundaries.Admin_Level_2')),
                ('admin_level_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boundaries.Admin_Level_3')),
                ('admin_level_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boundaries.Admin_Level_4')),
                ('admin_level_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boundaries.Admin_Level_5')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boundaries.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('age', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59), (60, 60), (61, 61), (62, 62), (63, 63), (64, 64), (65, 65), (66, 66), (67, 67), (68, 68), (69, 69), (70, 70), (71, 71), (72, 72), (73, 73), (74, 74), (75, 75), (76, 76), (77, 77), (78, 78), (79, 79), (80, 80), (81, 81), (82, 82), (83, 83), (84, 84), (85, 85), (86, 86), (87, 87), (88, 88), (89, 89), (90, 90), (91, 91), (92, 92), (93, 93), (94, 94), (95, 95), (96, 96), (97, 97), (98, 98), (99, 99)], null=True)),
                ('ethnicity', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('sub_ethnicity', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('clan', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='F', max_length=1)),
                ('life_points', models.IntegerField(blank=True, default=10, null=True)),
                ('household', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.Household')),
            ],
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('payroll_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('crisis', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scheme', to='games.Crisis')),
                ('donor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schemes', to='games.Donor')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('FOOD', 'Food'), ('ENTERTAINMENT', 'Entertainment'), ('CLOTHING', 'Clothing'), ('RENT', 'Rent'), ('UTILITIES', 'Utilities')], default='FOOD', max_length=1)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to='games.Person')),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='games.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, default=1, null=True)),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='turns', to='games.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('category', models.CharField(choices=[('FOOD', 'Food'), ('ENTERTAINMENT', 'Entertainment'), ('CLOTHING', 'Clothing'), ('RENT', 'Rent'), ('UTILITIES', 'Utilities')], default='FOOD', max_length=1)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('admin_level_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boundaries.Admin_Level_1')),
                ('admin_level_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boundaries.Admin_Level_2')),
                ('admin_level_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boundaries.Admin_Level_3')),
                ('admin_level_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boundaries.Admin_Level_4')),
                ('admin_level_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boundaries.Admin_Level_5')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boundaries.Country')),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='turn',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='games.Turn'),
        ),
        migrations.AddField(
            model_name='person',
            name='scheme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.Scheme'),
        ),
        migrations.AddField(
            model_name='person',
            name='transactions',
            field=models.ManyToManyField(related_name='transactions_for', through='games.Transaction', to='games.Person'),
        ),
        migrations.CreateModel(
            name='Adult',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('games.person',),
        ),
        migrations.CreateModel(
            name='Minor',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('games.person',),
        ),
        migrations.CreateModel(
            name='Senior',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('games.person',),
        ),
    ]
