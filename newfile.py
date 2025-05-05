# modules/auto_presser.py

from .. import loader, utils  # Импорты из Hikka
import logging

logger = logging.getLogger(__name__)

@loader.tds
class AutoPresserMod(loader.Module):
    """Автоматически нажимает на кнопки бота @FootCard"""

    strings = {
        "name": "AutoPresser",
        "pressed": "<b>Кнопка нажата!</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "interval", 60,
                lambda: "Интервал между проверками (в секундах)"
            )
        )

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

    @loader.command(ru_doc="Нажать на кнопку в последнем сообщении")
    async def presscmd(self, message):
        reply = await message.get_reply_message()
        if not reply or not reply.reply_markup:
            await utils.answer(message, "❌ Ответь на сообщение с кнопками!")
            return

        try:
            await reply.click()
            await utils.answer(message, self.strings["pressed"])
        except Exception as e:
            await utils.answer(message, f"⚠️ Ошибка: {str(e)}")

    @loader.loop(interval=60)
    async def autoloop(self):
        # Пример автоматической проверки раз в 60 секунд
        chat = "@FootCard"
        msg = (await self.client.get_messages(chat, limit=1))[0]
        if msg.reply_markup:
            try:
                await msg.click()
                logger.info("Кнопка нажата через автоперебор.")
            except Exception as e:
                logger.error(f"Ошибка при автонажатии: {e}")