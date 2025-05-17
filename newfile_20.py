# meta developer: @your_username
from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class MatchButtonOnReply(loader.Module):
    """Нажимает кнопку 'Матч' в сообщении, на которое ты ответил"""

    strings = {"name": "MatchButtonOnReply"}

    @loader.command()
    async def match(self, message: Message):
        """Ответь на сообщение и напиши .match"""
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("❌ Ответь на сообщение, где есть кнопка 'Матч'")
            return

        if not reply.buttons:
            await message.edit("❌ В этом сообщении нет кнопок.")
            return

        for row in reply.buttons:
            for button in row:
                if "матч" in button.text.lower():
                    await message.edit("✅ Нажимаю кнопку 'Матч'...")
                    await button.click()
                    return

        await message.edit("❌ Кнопка 'Матч' не найдена.")
