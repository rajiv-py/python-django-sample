# Generated by Django 2.2.1 on 2019-07-26 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20190528_1121'),
        ('account', '0008_auto_20190726_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelaccountuser',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='base.ModelBaseCountry'),
        ),
        migrations.AddField(
            model_name='modelaccountuser',
            name='language',
            field=models.CharField(blank=True, choices=[('fr', 'French'), ('en', 'English')], default='fr', help_text='Language of the user.', max_length=60, null=True),
        ),
    ]
