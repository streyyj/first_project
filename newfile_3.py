from hikkatl.tl.functions.messages import SendMessageRequest
from hikkatl.utils import get_display_name
from .. import loader, utils
import asyncio

@loader.tds
class FCardMatchMod(loader.Module):
    """Модуль для автоматического выбора матча в боте @F_CardBot"""
    strings = {"name": "FCardMatch"}

    async def fcardmatchcmd(self, message):
        """Запустить матч (пример: .fcardmatch)"""
        bot_username = "@F_CardBot"
        await self.client(SendMessageRequest(bot_username, "/start"))
        await utils.answer(message, "Команда отправлена. Ожидание ответа от бота...")
        
        # Ждём сообщение с кнопкой
        response = await self.wait_for_bot_response(bot_username)
        if not response:
            await utils.answer(message, "Не удалось получить ответ от бота")
            return
        
        # Ищем кнопку "Матч"
        for row in response.reply_markup.rows:
            for button in row.buttons:
                if button.text == "Матч":
                    await button.click()
                    await utils.answer(message, "Кнопка 'Матч' нажата. Проверьте диалог с ботом.")
                    return
        
        await utils.answer(message, "Кнопка 'Матч' не найдена")

    async def wait_for_bot_response(self, bot_username, timeout=10):
        """Ожидание сообщения от бота"""
        future = asyncio.Future()
        
        @self.client.on(events.NewMessage(from_users=bot_username))
        async def handler(event):
            if event.message.media and hasattr(event.message.media, 'buttons'):
                future.set_result(event.message)
                self.client.remove_event_handler(handler)
        
        try:
            await asyncio.wait_for(future, timeout)
            return future.result()
        except asyncio.TimeoutError:
            return None