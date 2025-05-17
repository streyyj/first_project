# meta developer: @your_username
from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class PlayMatchOnReply(loader.Module):
    """Нажимает кнопку 'Играть матч' в сообщении, на которое ты ответил"""

    strings = {"name": "PlayMatchOnReply"}

    @loader.command()
    async def playmatch(self, message: Message):
        """Ответь на сообщение и напиши .playmatch"""
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("❌ Ответь на сообщение с кнопкой 'Играть матч'")
            return

        if not reply.buttons:
            await message.edit("❌ В этом сообщении нет кнопок.")
            return

        for row in reply.buttons:
            for button in row:
                if "играть матч" in button.text.lower():
                    await message.edit("✅ Нажимаю кнопку 'Играть матч'...")
                    await button.click()
                    return

        await message.edit("❌ Кнопка 'Играть матч' не найдена.")
