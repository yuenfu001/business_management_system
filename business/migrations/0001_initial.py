# Generated by Django 5.0.6 on 2024-06-22 12:51

import business.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Business",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("start_date", models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="BusinessExpenditure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("purchased_item", models.CharField(max_length=50)),
                ("purchased_quantity", models.PositiveIntegerField(default=0)),
                (
                    "COG",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
                ),
                (
                    "total_amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=40),
                ),
                ("quantity_left", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="BusinessInflow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sold_quantity", models.PositiveIntegerField(default=0)),
                (
                    "COGS",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
                ),
                (
                    "total_amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=40),
                ),
                (
                    "sold_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="business.businessexpenditure",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transaction",
                    models.CharField(
                        default=business.models.generate_transaction_id,
                        max_length=50,
                        unique=True,
                    ),
                ),
                ("transaction_created", models.DateField(auto_now=True)),
                ("transaction_date", models.DateField(auto_now_add=True)),
                (
                    "business_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="business.business",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="businessexpenditure",
            name="transaction",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="business.transaction"
            ),
        ),
    ]
