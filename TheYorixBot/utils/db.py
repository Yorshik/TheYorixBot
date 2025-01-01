import logging

import asgiref.sync
import TheYorixBot.apps.YorixVault.models as YorixModels
import utils.config

__all__ = ()


@asgiref.sync.sync_to_async
def create_superuser():
    owner_id = utils.config.config.OWNER_ID
    user, created = YorixModels.User.objects.get_or_create(
        telegram_id=owner_id,
        defaults={"username": None, "is_admin": True, "is_owner": True},
    )
    if created:
        logging.info(f"Суперпользователь с telegram_id {owner_id} успешно создан.")
    else:
        logging.debug(f"Суперпользователь с telegram_id {owner_id} уже существует.")
        logging.info("Суперпользователь не создан")

    return user, created
