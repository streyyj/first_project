from .. import loader, utils
import telethon
from telethon.tl.types import Message


@loader.tds
class FootballBotHelperMod(loader.Module):
    """Автоматическое взаимодействие с ботом @F_CardBot"""

    strings = {
        "name": "FootballBotHelper",
        "start_game": "⚽️ Матч",
        "play_match": "🎮 Играть матч",
        "menu_sent": "✅ Отправлено 'Меню'",
        "match_button_pressed": "✅ Нажата кнопка '⚽️ Матч'",
        "play_match_button_pressed": "✅ Нажата кнопка '🎮 Играть матч'",
        "error": "⚠️ Ошибка: "
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.state = {}

    async def fbcmd(self, message: Message):
        """Команда для запуска скрипта"""
        chat = await self.get_chat(message)

        # Отправляем "Меню"
        await self.send_menu(chat)
        await utils.answer(message, self.strings["menu_sent"])

    async def send_menu(self, chat):
        await self.client.send_message(chat, "Меню")

    async def handle_callback(self, update):
        if not isinstance(update, telethon.tl.patched.Message):
            return

        if update.sender_id != (await self.client.get_entity("@F_CardBot")).id:
            return

        if self.strings["start_game"] in update.text:
            await self.press_match_button(update)
        elif self.strings["play_match"] in update.text:
            await self.press_play_match_button(update)

    async def press_match_button(self, message: Message):
        for button in message.buttons:
            if self.strings["start_game"] in button.text:
                await self.client(telethon.tl.functions.messages.ClickInlineButtonRequest(
                    chat_id=message.chat_id,
                    message_id=message.id,
                    button=button
                ))
                break

    async def press_play_match_button(self, message: Message):
        for button in message.buttons:
            if self.strings["play_match"] in button.text:
                await self.client(telethon.tl.functions.messages.ClickInlineButtonRequest(
                    chat_id=message.chat_id,
                    message_id=message.id,
                    button=button
                ))
                break

    async def get_chat(self, message: Message):
        if message.is_private:
            return message.to_id.user_id
        else:
            return message.chat_id