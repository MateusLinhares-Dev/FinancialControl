# Generated by Django 5.0.6 on 2024-06-03 22:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
        ('userFinance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='financeview',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='userFinanceList', to='userFinance.userfinance'),
            preserve_default=False,
        ),
    ]