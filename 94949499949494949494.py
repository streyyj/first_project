from hikkamod import Module
from telethon.tl.custom import Message
import asyncio

class FCardAuto(Module):
    """Автоматическое прохождение матча в F_CardBot"""
    
    strings = {"name": "FCardAuto"}
    
    async def auto_match_cmd(self, message: Message):
        """Запустить автоматический матч (используй .auto_match)"""
        await message.edit("<b>Запускаю автоматический матч...</b>")
        
        # Шаг 1: Отправляем "Меню"
        await self.client.send_message("@F_CardBot", "Меню")
        await asyncio.sleep(5)
        
        # Шаг 2: Ищем сообщение с кнопкой "⚽️Матч"
        async for msg in self.client.iter_messages("@F_CardBot", limit=10):
            if msg.buttons and any(b.text == "⚽️Матч" for row in msg.buttons for b in row):
                await msg.click(text="⚽️Матч")
                break
        await asyncio.sleep(5)
        
        # Шаг 3: Ищем сообщение с кнопкой "🎮Играть матч"
        async for msg in self.client.iter_messages("@F_CardBot", limit=10):
            if msg.buttons and any(b.text == "🎮Играть матч" for row in msg.buttons for b in row):
                await msg.click(text="🎮Играть матч")
                break
        
        await message.edit("<b>Матч запущен!</b>")
