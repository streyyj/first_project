import asyncio
from .. import loader, utils


@loader.tds
class FCardBotModule(loader.Module):
    """Модуль для автоматической отправки сообщения 'Фкарта' каждые 10 секунд"""

    strings = {
        "name": "FCardBot",
        "started": "<b>Автоматическая отправка 'Фкарта' запущена!</b>",
        "stopped": "<b>Автоматическая отправка 'Фкарта' остановлена.</b>",
        "already_running": "<b>Автоматическая отправка уже запущена.</b>",
        "not_running": "<b>Автоматическая отправка не запущена.</b>",
    }

    def __init__(self):
        self.name = self.strings["name"]
        self._task = None  # Для хранения задачи таймера

    async def startcmd(self, message):
        """Запустить автоматическую отправку 'Фкарта'"""
        if self.get("is_running", False):
            await utils.answer(message, self.strings["already_running"])
            return

        self.set("is_running", True)
        self._task = asyncio.create_task(self._send_message_loop())
        await utils.answer(message, self.strings["started"])

    async def stopcmd(self, message):
        """Остановить автоматическую отправку 'Фкарта'"""
        if not self.get("is_running", False):
            await utils.answer(message, self.strings["not_running"])
            return

        self.set("is_running", False)
        if self._task:
            self._task.cancel()
            self._task = None
        await utils.answer(message, self.strings["stopped"])

    async def _send_message_loop(self):
        """Посылает сообщение 'Фкарта' каждые 10 секунд"""
        while self.get("is_running", False):
            try:
                await self._client.send_message("@F_CardBot", "Фкарта")
                await asyncio.sleep(60)  # Ожидание 10 секунд
            except Exception as e:
                self._logger.error(f"Ошибка при отправке сообщения: {e}")
                break

    async def client_ready(self, client, db):
        self.db = db  # Сохраняем ссылку на общую базу данных