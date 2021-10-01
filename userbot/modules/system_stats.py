# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting information about the server. """

import platform
import shutil
import sys
import time
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from datetime import datetime
from os import remove
from platform import python_version, uname
from shutil import which

import psutil
from git import Repo
from telethon import __version__, version

from userbot import ALIVE_LOGO, ALIVE_NAME, CMD_HELP, USERBOT_VERSION, StartTime, bot
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
repo = Repo()
modules = CMD_HELP
# ============================================


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@register(outgoing=True, pattern=r"^.(alive|on)$")
async def amireallyalive(alive):
    """ For .alive command, check if the bot is running.  """
    uptime = await get_readable_time((time.time() - StartTime))
    output = (
        "`⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊶⊷⊶⊶⊶⊶⊶`\n"
        f"•  👤 `Owner  :`  {DEFAULTUSER} \n"
        "`⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊶⊷⊶⊶⊶⊶⊶`\n"
        f"•  🤖 `GenBot   : v{USERBOT_VERSION} `\n"
        f"•  🗃 `Modules  : {len(modules)} `\n"
        f"•  🕒 `Online : {uptime} `\n"
        "`⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊶⊷⊶⊶⊶⊶⊶`"
    )
    if ALIVE_LOGO:
        try:
            logo = ALIVE_LOGO
            await bot.send_file(alive.chat_id, logo, caption=output)
            await alive.delete()
        except BaseException:
            await alive.edit(
                output + "\n\n *`The provided logo is invalid."
                "\nMake sure the link is directed to the logo picture`"
            )
    else:
        await alive.edit(output)


@register(outgoing=True, pattern="^.aliveu")
async def amireallyaliveuser(username):
    """ For .aliveu command, change the username in the .alive command. """
    message = username.text
    output = ".aliveu [new user without brackets] nor can it be empty"
    if not (message == ".aliveu" or message[7:8] != " "):
        newuser = message[8:]
        global DEFAULTUSER
        DEFAULTUSER = newuser
        output = "Successfully changed user to " + newuser + "!"
    await username.edit("`" f"{output}" "`")


@register(outgoing=True, pattern="^.resetalive$")
async def amireallyalivereset(ureset):
    """ For .resetalive command, reset the username in the .alive command. """
    global DEFAULTUSER
    DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
    await ureset.edit("`" "Successfully reset user for alive!" "`")


CMD_HELP.update(
    {
        "alive": ".alive | .on\
    \nUsage: Type .alive/.on to see wether your bot is working or not.\
    \n\n.aliveu <text>\
    \nUsage: Changes the 'user' in alive to the text you want.\
    \n\n.resetalive\
    \nUsage: Resets the user to default."
    }
)
