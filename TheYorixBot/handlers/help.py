import aiogram.filters
import aiogram.types

__all__ = ()

router = aiogram.Router()


@router.message(aiogram.filters.Command("help"))
async def cmd_help(message: aiogram.types.Message):
    await message.answer("Хелпы нет. Но будет, ждите")
