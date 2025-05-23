# giftloop.py
from hikka import Module
from telethon.tl.custom import Message
import asyncio


class GiftLoop(Module):
    """Модуль для автоматической отправки /gift каждые 10 минут"""

    strings = {
        "name": "GiftLoop",
        "started": "<b>Авто-гифт запущен! Будет отправлять /gift каждые 10 минут</b>",
        "stopped": "<b>Авто-гифт остановлен</b>",
        "already_running": "<b>Авто-гифт уже запущен!</b>"
    }

    def __init__(self):
        self.is_running = False
        self.task = None
        self.chat = None

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

        # Восстанавливаем состояние после перезагрузки
        if self.db.get("GiftLoop", "running", False):
            self.chat = self.db.get("GiftLoop", "chat_id")
            self.is_running = True
            self.task = asyncio.create_task(self._gift_loop())

    async def _send_gift(self):
        """Отправляет команду /gift в указанный чат"""
        try:
            await self.client.send_message(self.chat, "/gift")
        except Exception as e:
            print(f"[GiftLoop] Ошибка при отправке: {e}")

    async def _gift_loop(self):
        """Основной цикл отправки /gift"""
        while self.is_running:
            await self._send_gift()
            await asyncio.sleep(600)  # 10 минут

    async def giftstartcmd(self, message: Message):
        """Запустить авто-гифт (используй .giftstart)"""
        if self.is_running:
            await message.edit(self.strings["already_running"])
            return

        self.chat = message.chat_id
        self.is_running = True
        self.db.set("GiftLoop", "running", True)
        self.db.set("GiftLoop", "chat_id", self.chat)

        self.task = asyncio.create_task(self._gift_loop())
        await message.edit(self.strings["started"])

    async def giftstopcmd(self, message: Message):
        """Остановить авто-гифт (используй .giftstop)"""
        if not self.is_running:
            await message.edit("<b>Авто-гифт не запущен!</b>")
            return

        self.is_running = False
        self.db.set("GiftLoop", "running", False)
        self.db.set("GiftLoop", "chat_id", None)

        if self.task:
            self.task.cancel()
            self.task = None

        await message.edit(self.strings["stopped"])