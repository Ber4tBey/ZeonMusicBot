from asyncio import QueueEmpty

from pyrogram import Client
from pyrogram.types import Message

from .. import queues
from ..callsmusic import callsmusic
from ..helpers.chat_id import get_chat_id
from ..helpers.decorators import authorized_users_only
from ..helpers.decorators import errors
from ..helpers.filters import command
from ..helpers.filters import other_filters


@Client.on_message(command('dur') & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    (
        await message.reply_text('<b>⏸ Durduruldu</b>', False)
    ) if (
        callsmusic.pause(get_chat_id(message.chat))
    ) else (
        await message.reply_text('<b>❌ Hiçbir şey oynatılmıyor...</b>', False)
    )


@Client.on_message(command('devam') & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    (
        await message.reply_text('<b>▶️ Devam Ediliyor...</b>', False)
    ) if (
        callsmusic.resume(get_chat_id(message.chat))
    ) else (
        await message.reply_text('<b>❌ Hiçbir şey durdurulmadı</b>', False)
    )


@Client.on_message(command('bitir') & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.active_chats:
        await message.reply_text('<b>❌ Zaten oynatılmıyor</b>', False)
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass
        await callsmusic.stop(chat_id)
        await message.reply_text('<b>⏹ Yayın durduruldu</b>', False)


@Client.on_message(command('geç') & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.active_chats:
        await message.reply_text('<b>❌ Hiçbir şey oynatılmıyor</b>', False)
    else:
        queues.task_done(chat_id)
        if queues.is_empty(chat_id):
            await callsmusic.stop(chat_id)
        else:
            await callsmusic.set_stream(
                chat_id,
                queues.get(chat_id)['file'],
            )
        await message.reply_text('<b>✅ Geçildi</b>', False)


@Client.on_message(command('sustur') & other_filters)
@errors
@authorized_users_only
async def mute(_, message: Message):
    result = callsmusic.mute(get_chat_id(message.chat))
    (
        await message.reply_text('<b>✅ Susturuldu</b>', False)
    ) if (
        result == 0
    ) else (
        await message.reply_text('<b>❌ Zaten susturulmuş</b>', False)
    ) if (
        result == 1
    ) else (
        await message.reply_text('<b>❌ Yayında değil</b>', False)
    )


@Client.on_message(command('susturma') & other_filters)
@errors
@authorized_users_only
async def unmute(_, message: Message):
    result = callsmusic.unmute(get_chat_id(message.chat))
    (
        await message.reply_text('<b>✅ Susuturma Kaldırıldı</b>', False)
    ) if (
        result == 0
    ) else (
        await message.reply_text('<b>❌ Susturulmadı</b>', False)
    ) if (
        result == 1
    ) else (
        await message.reply_text('<b>❌ Yayında Değil</b>', False)
    )
