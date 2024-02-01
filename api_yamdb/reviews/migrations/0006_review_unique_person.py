# Generated by Django 3.2 on 2024-02-01 11:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0005_auto_20240201_1652"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                fields=("title", "author"), name="unique_person"
            ),
        ),
    ]
