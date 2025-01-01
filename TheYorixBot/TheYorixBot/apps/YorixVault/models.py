import django.core.validators
import django.db.models
from django.utils.translation import gettext_lazy as _

__all__ = ()


class User(django.db.models.Model):
    telegram_id = django.db.models.BigIntegerField(
        verbose_name=_("user`s telegram id"),
        help_text=_("Using this id, bot identifies the user"),
        unique=True,
        editable=False,
    )
    username = django.db.models.CharField(
        verbose_name=_("user`s telegram username"),
        help_text=_("Username is necessary for some actions, like tictactoe or others"),
        null=True,
        max_length=32,
        validators=[django.core.validators.MinValueValidator(5)],
    )
    is_admin = django.db.models.BooleanField(
        verbose_name=_("is user an admin"),
        help_text=_("Shows if user is allowed to use some commands or not"),
        default=False,
    )
    is_owner = django.db.models.BooleanField(
        verbose_name=_("is user the owner"),
        help_text=_("Shows if the account belongs to the creator of the bot"),
        default=False,
    )
