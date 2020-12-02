# Generated by Django 2.2.1 on 2019-05-07 13:34

import cheers.apps.account.models.user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelAccountUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date and time when this entry was created in the system')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date and time when the table data was last updated in the system')),
                ('email', models.EmailField(help_text='Email of the user.', max_length=254, unique=True)),
                ('name', models.CharField(blank=True, help_text="User's name.", max_length=200, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('address', models.TextField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, help_text="User's avatar.", null=True, upload_to=cheers.apps.account.models.user.get_upload_path)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('device_token', models.CharField(blank=True, help_text='User Device Token', max_length=200, null=True)),
                ('device_type', models.CharField(blank=True, choices=[('android', 'Android'), ('ios', 'Ios')], help_text='Device type of the user.', max_length=60, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Toggles active status for a user.')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates the user as a staff member.')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates the user as a super user.')),
                ('is_bar_owner', models.BooleanField(default=False, help_text='Designates the user as a bar owner.')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'account_user',
            },
        ),
        migrations.CreateModel(
            name='ModelAccountVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(help_text='A unique uuid 4 based token sent inthe email as a link.', max_length=100)),
                ('type', models.IntegerField(choices=[(0, 'registration'), (1, 'password')], default=0, help_text='Decides what type of request needs to be verified.')),
                ('expiration', models.DateTimeField(help_text='Number of days for which theverification token is valid.')),
                ('user', models.OneToOneField(help_text='A user of the account which is dueaccount verification.', on_delete=django.db.models.deletion.CASCADE, related_name='verification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Verification',
                'verbose_name_plural': 'Verifications',
                'db_table': 'account_verification',
            },
        ),
    ]
