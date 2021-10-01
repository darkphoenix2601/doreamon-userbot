# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for purging unneeded messages(usually spam or ot). """

from asyncio import sleep

from telethon.errors import rpcbaseerrors

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.purge$")
async def fastpurger(purg):
    """ The .purge command deletes all messages from the reply. """
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count = count + 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        await purg.edit("`I need a message to start purging.`")
        return

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id,
        f"`Fast purge complete!`\
        \nPurged {str(count)} messages",
    )

    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID, "Purge of " + str(count) + " messages made successfully."
        )
    await sleep(2)
    await done.delete()

@register(outgoing=True, pattern="^.purgeme")
async def purgeme(delme):
    """ The .purgeme command, delete x messages that you sent."""
    message = delme.text
    count = int(message[9:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id, from_user="me"):
        if i > count + 1:
            break
        i = i + 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "`Complete purge!` " + str(count) + " deleted messages.",
    )
    if BOTLOG:
        await delme.client.send_message(
            BOTLOG_CHATID, "Purge of " + str(count) + " messages made successfully."
        )
    await sleep(2)
    i = 1
    await smsg.delete()


@register(outgoing=True, pattern="^.del$")
async def delete_it(delme):
    """ The .del command deletes the replied message."""
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Message deletion was successful"
                )
        except rpcbaseerrors.BadRequestError:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Well I can't delete the message"
                )


    
CMD_HELP.update(
    {
        "purge": ".purge\
        \nUso: Delete all messages from the reply."
    }
)

CMD_HELP.update(
    {
        "purgeme": ".purgeme <x>\
        \nUso: Delete x amount of your last messages."
    }
)

CMD_HELP.update(
    {
        "del": ".del\
        \nUso: Delete the message you replied to."
    }
)
