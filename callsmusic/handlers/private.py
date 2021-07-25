from pyrogram import Client
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import Message

from ..helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_text(
        f'<b>👋🏻 Merhaba {message.from_user.mention()}!</b>\n\n'
        'Ben müzik botuyum, '
        'Grup aramalarınızı şarkılarımla renklendiriyorum.'
        '\n\nDesteklediğim Komutlar:\n\n'
        '/oynat - Ses dosyası veya YouTube videosu oynatır\n'
        '/dur - Yayını durdurur\n'
        '/devam - Yayını devam ettirir\n'
        '/gec - Sıradaki şarkıya geçer\n'
        '/sustur - Botu susturur\n'
        '/susturma - Botun sesini açar\n'
        '/bitir - Tamamen bitirir'
        'Bot @zodiac_wv tarafından yapılmıştır'
        'Channel : @zodiac_music_channel',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        '🔈 Channel', url='https://t.me/zodiac_music_channel',
                    ),
                    InlineKeyboardButton(
                        'Group 💬', url='https://t.me/pokemonlar',
                    ),
                ],
            ],
        ),
    )
