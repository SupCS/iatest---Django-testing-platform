# Generated by Django 4.1.2 on 2022-10-26 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="status",
            field=models.CharField(
                choices=[("S", "Студент"), ("T", "Викладач")], default="S", max_length=1
            ),
        ),
    ]