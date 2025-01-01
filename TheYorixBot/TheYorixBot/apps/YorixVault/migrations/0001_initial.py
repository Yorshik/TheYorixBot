# Generated by Django 5.1.4 on 2024-12-30 23:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                    "telegram_id",
                    models.BigIntegerField(
                        editable=False,
                        help_text="Using this id, bot identifies the user",
                        unique=True,
                        verbose_name="user`s telegram id",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        help_text=(
                            "Username is necessary for some actions, like tictactoe or"
                            " others"
                        ),
                        max_length=32,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(5)],
                        verbose_name="user`s telegram username",
                    ),
                ),
                (
                    "is_admin",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "Shows if user is allowed to use some commands or not"
                        ),
                        verbose_name="is user an admin",
                    ),
                ),
                (
                    "is_owner",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "Shows if the account belongs to the creator of the bot"
                        ),
                        verbose_name="is user the owner",
                    ),
                ),
            ],
        ),
    ]