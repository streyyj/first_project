# scope: hikka_only
# meta developer: @d4n13lxx
# name: SendMenuToFCard

from .. import loader, utils
from hikkatl.tl.functions.messages import SendMessageRequest

@loader.tds
class SendMenuToFCardMod(loader.Module):
    """Отправка 'Меню' в @F_CardBot"""

    strings = {
        "name": "SendMenuToFCard",
    }

    async def client_ready(self, client, db):
        self._client = client

    async def менюcmd(self, message):
        """Отправить 'Меню' боту @F_CardBot"""
        bot_username = "@F_CardBot"
        await self._client(SendMessageRequest(bot_username, "Меню"))
        await utils.answer(message, "✅ Сообщение 'Меню' отправлено боту @F_CardBot")