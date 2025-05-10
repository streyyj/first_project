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
        self._db = loader.Database(
            self.__class__.__name__,
            {"is_running": False},  # Статус работы (True/False)
        )
        self._task = None  # Для хранения задачи таймера

    async def startcmd(self, message):
        """Запустить автоматическую отправку 'Фкарта'"""
        if self._db.get("is_running"):
            await utils.answer(message, self.strings["already_running"])
            return

        self._db.set("is_running", True)
        self._task = asyncio.create_task(self._send_message_loop())
        await utils.answer(message, self.strings["started"])

    async def stopcmd(self, message):
        """Остановить автоматическую отправку 'Фкарта'"""
        if not self._db.get("is_running"):
            await utils.answer(message, self.strings["not_running"])
            return

        self._db.set("is_running", False)
        if self._task:
            self._task.cancel()
            self._task = None
        await utils.answer(message, self.strings["stopped"])

    async def _send_message_loop(self):
        """Посылает сообщение 'Фкарта' каждые 10 секунд"""
        while self._db.get("is_running"):
            try:
                await self._client.send_message("@F_CardBot", "Фкарта")
                await asyncio.sleep(10)  # Ожидание 10 секунд
            except Exception as e:
                self._logger.error(f"Ошибка при отправке сообщения: {e}")
                break

    async def client_ready(self, _, db):
        """Инициализация модуля при старте клиента"""
        self._db = db