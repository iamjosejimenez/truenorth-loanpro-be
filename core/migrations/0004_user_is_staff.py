# Generated by Django 4.2 on 2023-04-15 02:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_rename_email_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
    ]
