# Generated by Django 4.2.5 on 2023-10-12 10:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="session_id",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="payment",
            name="session_url",
            field=models.URLField(max_length=255, null=True),
        ),
    ]