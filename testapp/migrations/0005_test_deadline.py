# Generated by Django 4.1.3 on 2022-12-06 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0004_submition"),
    ]

    operations = [
        migrations.AddField(
            model_name="test",
            name="deadline",
            field=models.DateTimeField(null=True),
        ),
    ]