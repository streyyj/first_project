# getcard.py
from hikka import Module
from telethon.tl.custom import Message
import asyncio


class GetCard(Module):
    """Модуль для автоматической отправки 'Получить карту' каждые 10 секунд"""

    strings = {
        "name": "GetCard",
        "started": "<b>Авто-получение карт запущено! Будет отправлять 'Получить карту' каждые 10 секунд</b>",
        "stopped": "<b>Авто-получение карт остановлено</b>",
        "already_running": "<b>Авто-получение уже запущено!</b>"
    }

    def __init__(self):
        self.is_running = False
        self.task = None
        self.chat = None

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

        # Восстанавливаем состояние после перезагрузки
        if self.db.get("GetCard", "running", False):
            self.chat = self.db.get("GetCard", "chat_id")
            self.is_running = True
            self.task = asyncio.create_task(self._get_card_loop())

    async def _send_get_card(self):
        """Отправляет команду 'Получить карту' в указанный чат"""
        try:
            await self.client.send_message(self.chat, "Получить карту")
        except Exception as e:
            print(f"[GetCard] Ошибка при отправке: {e}")

    async def _get_card_loop(self):
        """Основной цикл отправки 'Получить карту'"""
        while self.is_running:
            await self._send_get_card()
            await asyncio.sleep(10)  # 10 секунд

    async def stcmd(self, message: Message):
        """Запустить авто-получение карт (используй .st)"""
        if self.is_running:
            await message.edit(self.strings["already_running"])
            return

        self.chat = message.chat_id
        self.is_running = True
        self.db.set("GetCard", "running", True)
        self.db.set("GetCard", "chat_id", self.chat)

        self.task = asyncio.create_task(self._get_card_loop())
        await message.edit(self.strings["started"])

    async def spcmd(self, message: Message):
        """Остановить авто-получение карт (используй .sp)"""
        if not self.is_running:
            await message.edit("<b>Авто-получение карт не запущено!</b>")
            return

        self.is_running = False
        self.db.set("GetCard", "running", False)
        self.db.set("GetCard", "chat_id", None)

        if self.task:
            self.task.cancel()
            self.task = None

        await message.edit(self.strings["stopped"])