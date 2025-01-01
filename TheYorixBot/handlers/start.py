import logging

import aiogram.filters
import aiogram.types
import filters.owner_filter

__all__ = ()

router = aiogram.Router()


@router.message(aiogram.filters.Command("start"))
async def cmd_start(message: aiogram.types.Message):
    logging.info("started 'start' handler")
    await message.answer("Привет. Я - Yorix, и я крутой бот.")


@router.message(
    aiogram.filters.Command("start_owner"),
    filters.owner_filter.OwnerFilter(),
)
async def cmd_owner_start(message: aiogram.types.Message):
    await message.answer("Здарова, Великий админ Ёршик")
