# scope: hikka_only
# meta developer: @trololo69, @t.me/F_CardBot

from .. import loader, utils
from telethon.tl.custom import Message
import asyncio


@loader.tds
class GetCardMod(loader.Module):
    """Модуль для автоматической отправки 'Получить карту'"""

    strings = {
        "name": "GetCard",
        "started": "<b>Авто-получение карт запущено!</b>",
        "stopped": "<b>Авто-получение карт остановлено</b>",
        "already_running": "<b>Уже запущено!</b>"
    }

    def __init__(self):
        self._task = None
        self.running = False

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def stcmd(self, message: Message):
        """Запустить авто-получение карты — .st"""
        if self.running:
            await message.edit(self.strings["already_running"])
            return

        self.running = True
        await message.edit(self.strings["started"])

        async def loop():
            while self.running:
                try:
                    await self.client.send_message("F_CardBot", "Получить карту")
                except Exception as e:
                    print(f"[GetCard] Ошибка: {e}")
                await asyncio.sleep(60)

        self._task = asyncio.ensure_future(loop())

    async def spcmd(self, message: Message):
        """Остановить авто-получение карты — .sp"""
        if not self.running:
            await message.edit("<b>Не запущено!</b>")
            return

        self.running = False
        if self._task:
            self._task.cancel()
        await message.edit(self.strings["stopped"])