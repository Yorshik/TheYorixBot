import asyncio
import logging

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from django.core.cache import cache
from django.db import IntegrityError
import TheYorixBot.apps.YorixVault.models as YorixModels

__all__ = ()


class UserCacheMiddleware(BaseMiddleware):
    CACHE_TIMEOUT = 10 * 365 * 24 * 60 * 60

    async def __call__(self, handler, event, data):
        logging.info("started user middleware")
        user = event.from_user
        logging.info("user extracted")
        if user:
            telegram_id = user.id
            current_username = user.username or ""
            cache_key = f"telegram_user_{telegram_id}"
            user_data = cache.get(cache_key)
            logging.info("got cache from redis")
            if not user_data:
                try:
                    user_instance, created = await asyncio.to_thread(
                        YorixModels.User.objects.get_or_create,
                        telegram_id=telegram_id,
                        defaults={
                            "username": current_username or f"user_{telegram_id}",
                            "is_admin": False,
                            "is_owner": False,
                        },
                    )
                    user_data = {
                        "id": user_instance.id,
                        "username": user_instance.username,
                        "telegram_id": user_instance.telegram_id,
                        "is_admin": user_instance.is_admin,
                        "is_owner": user_instance.is_owner,
                    }
                    logging.info("created user")
                    cache.set(cache_key, user_data, self.CACHE_TIMEOUT)
                    logging.info("cache set to redis")
                    if created:
                        logging.debug(
                            f"Пользователь {telegram_id} создан и сохранён в кэше.",
                        )
                    else:
                        logging.debug(
                            f"Пользователь {telegram_id} загружен из БД и сохранён в"
                            " кэше.",
                        )
                except IntegrityError as e:
                    logging.error(
                        f"Ошибка при создании пользователя {telegram_id}: {e}",
                    )
                    user_data = None
                except Exception as e:
                    logging.error(
                        "Неизвестная ошибка при обработке пользователя"
                        f" {telegram_id}: {e}",
                    )
                    user_data = None

            if user_data:
                data["cached_user"] = user_data
                data["current_username"] = current_username

        cached_user = data.get("cached_user")
        current_username = data.get("current_username")
        logging.info(cached_user)
        logging.info(current_username)
        if (
            cached_user
            and current_username
            and current_username != cached_user.get("username")
        ):
            telegram_id = cached_user.get("telegram_id")
            try:
                user_instance = await asyncio.to_thread(
                    YorixModels.User.objects.get,
                    telegram_id=telegram_id,
                )
                user_instance.username = current_username
                await asyncio.to_thread(user_instance.save)
                cached_user["username"] = current_username
                cache_key = f"telegram_user_{telegram_id}"
                cache.set(cache_key, cached_user, self.CACHE_TIMEOUT)
                logging.debug(
                    f"Имя пользователя {telegram_id} обновлено до '{current_username}'"
                    " и сохранено в кэше.",
                )

            except YorixModels.User.DoesNotExist:
                logging.warning(
                    f"Пользователь с telegram_id {telegram_id} не найден при обновлении"
                    " имени пользователя.",
                )
            except Exception as e:
                logging.error(
                    f"Ошибка при обновлении имени пользователя {telegram_id}: {e}",
                )

        logging.info("ended middleware")
        return await handler(event, data)
