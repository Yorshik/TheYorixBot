import aiogram.filters.base
import aiogram.types
import asgiref.sync
import TheYorixBot.apps.YorixVault.models as YorixModels

__all__ = ()


class OwnerFilter(aiogram.filters.base.Filter):
    async def __call__(self, message: aiogram.types.Message) -> bool:
        user_id = message.from_user.id
        return await self.is_user_owner(user_id)

    @asgiref.sync.sync_to_async
    def is_user_owner(self, user_id: int) -> bool:
        return YorixModels.User.objects.filter(
            telegram_id=user_id,
            is_owner=True,
        ).exists()
