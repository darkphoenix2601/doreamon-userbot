# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Módulo de userbot que contiene comandos id de usuario, id de chat y log"""

from asyncio import sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register
from userbot.modules.admin import get_user_from_event


@register(outgoing=True, pattern="^.userid$")
async def useridgetter(target):
    """ The command .userid, returns the ID of the target user. """
    message = await target.get_reply_message()
    if message:
        if not message.forward:
            user_id = message.sender.id
            if message.sender.username:
                name = "@" + message.sender.username
            else:
                name = "**" + message.sender.first_name + "**"
        else:
            user_id = message.forward.sender.id
            if message.forward.sender.username:
                name = "@" + message.forward.sender.username
            else:
                name = "*" + message.forward.sender.first_name + "*"
        await target.edit("**Name:** {} \n**User ID:** `{}`".format(name, user_id))


@register(outgoing=True, pattern="^.link(?: |$)(.*)")
async def permalink(mention):
    """ The .link command generates a link to the user's PM with a custom text. """
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        await mention.edit(f"[{custom}](tg://user?id={user.id})")
    else:
        tag = (
            user.first_name.replace("\u2060", "") if user.first_name else user.username
        )
        await mention.edit(f"[{tag}](tg://user?id={user.id})")


@register(outgoing=True, pattern="^.chatid$")
async def chatidgetter(chat):
    """ The .chatid command, returns the ID of the chat you are currently in. """
    await chat.edit("Chat ID: `" + str(chat.chat_id) + "`")


@register(outgoing=True, pattern=r"^.log(?: |$)([\s\S]*)")
async def log(log_text):
    """ The .log command, forwards a message or command argument to the bot's log group """
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Chat ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("`What am I supposed to record?`")
            return
        await log_text.edit("`Successfully registered`")
    else:
        await log_text.edit("`This feature requires registration to be enabled!`")
    await sleep(2)
    await log_text.delete()


@register(outgoing=True, pattern="^.kickme$")
async def kickme(leave):
    """ Basically it is the command .kickme """
    await leave.edit("Bye...Noobs...See...U...In...Hell👀")
    await leave.client.kick_participant(leave.chat_id, "me")


@register(outgoing=True, pattern="^.unmutechat$")
async def unmute_chat(unm_e):
    """ The .unmutechat command, reactivate a muted chat. """
    try:
        from userbot.modules.sql_helper.keep_read_sql import unkread
    except AttributeError:
        await unm_e.edit("`Non-SQL Mode!`")
        return
    unkread(str(unm_e.chat_id))
    await unm_e.edit("```The sound of this chat was activated successfully```")
    await sleep(2)
    await unm_e.delete()


@register(outgoing=True, pattern="^.mutechat$")
async def mute_chat(mute_e):
    """ The command .mutechat, mutes any chat. """
    try:
        from userbot.modules.sql_helper.keep_read_sql import kread
    except AttributeError:
        await mute_e.edit("`Non-SQL mode!`")
        return
    await mute_e.edit(str(mute_e.chat_id))
    kread(str(mute_e.chat_id))
    await mute_e.edit("`Shht ..! This chat will be muted!`")
    await sleep(2)
    await mute_e.delete()
    if BOTLOG:
        await mute_e.client.send_message(
            BOTLOG_CHATID, str(mute_e.chat_id) + " was silenced."
        )


@register(incoming=True, disable_errors=True)
async def keep_read(message):
    """ The mute logic. """
    try:
        from userbot.modules.sql_helper.keep_read_sql import is_kread
    except AttributeError:
        return
    kread = is_kread()
    if kread:
        for i in kread:
            if i.groupid == str(message.chat_id):
                await message.client.send_read_acknowledge(message.chat_id)


# Regex-Ninja module by @Kandnub
regexNinja = False


@register(outgoing=True, pattern="^s/")
async def sedNinja(event):
    """For the regex-ninja module, automatic clear command that starts with s /"""
    if regexNinja:
        await sleep(0.5)
        await event.delete()


@register(outgoing=True, pattern="^.regexninja (on|off)$")
async def sedNinjaToggle(event):
    """ Enables or disables the regex ninja module. """
    global regexNinja
    if event.pattern_match.group(1) == "encendido":
        regexNinja = True
        await event.edit("`Ninja mode successfully enabled for Regexbot.`")
        await sleep(1)
        await event.delete()
    elif event.pattern_match.group(1) == "apagado":
        regexNinja = False
        await event.edit("`Ninja mode disabled successfully for Regexbot.`")
        await sleep(1)
        await event.delete()


CMD_HELP.update(
    {
        "chat": ".chatid\
\nUse: Fetches the current chat's ID\
\n\n.userid\
\nUse: Gets the user ID in response, if it is a forwarded message, find the source ID.\
\n\n.log\
\nUse: Forwards the message you have replied to in your bot log group.\
\n\n.kickme\
\nUse: Leave a target group.\
\n\n.unmutechat\
\nUse: Activate a muted chat.\
\n\n.mutechat\
\nUse: Allows you to mute any chat.\
\n\n.link <username / userid>: <optional text> or reply to someone's message with .link <optional text>\
\nUse: Generates a permanent link to the user's profile with optional custom text.\
\n\n.regexninja on/off\
\nUse: Globally enable / disable the regex ninja module.\
\nRegex Ninja module helps to remove regex bot trigger messages."
    }
)
