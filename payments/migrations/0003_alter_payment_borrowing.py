# Generated by Django 4.2.5 on 2023-10-12 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "borrowings",
            "0003_remove_borrowing_actual_return_date_not_before_borrow_date_and_more",
        ),
        ("payments", "0002_alter_payment_session_id_alter_payment_session_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="borrowing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payments",
                to="borrowings.borrowing",
            ),
        ),
    ]
