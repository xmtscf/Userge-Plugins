# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

"""for stuff related to android"""

import asyncio
from typing import Optional

import ujson

from bs4 import BeautifulSoup
from requests import get
from userge import Message, userge

magisk_release = (
    "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/{}.json"
)


@userge.on_cmd(
    "twrp",
    about={"header": "Find twrp for you device", "usage": "{tr}twrp <device codename>"},
    allow_via_bot=True,
)
async def device_recovery(message: Message):
    """Get Latest TWRP"""
    args = message.filtered_input_str
    if args:
        device = args
    else:
        await message.err("```Provide Device Codename !!```", del_in=3)
        return
    await message.delete()
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`Couldn't find twrp downloads for {device}!`\n"
        return await message.edit(reply, del_in=5)
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Latest TWRP for {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Updated:** __{date}__"
    )
    await message.edit(reply)


def format_release(x: str) -> Optional[str]:
    r = get(magisk_release.format(x))
    if r.status_code != 200:
        return
    r_data = ujson.loads(r.text)
    out = f"⦁ <b>{x.title()}</b>:  <a href={r_data.get('link')}>v{r_data.get('version')}</a>"
    if changelog := r_data.get("note"):
        out += f"  |  [Changelog]({changelog})"
    return out


@userge.on_cmd("magisk$", about={"header": "Get Latest Magisk Zip and Manager"})
async def magisk_(message: Message):
    """Get Latest MAGISK"""
    await message.edit(
        "𝗟𝗮𝘁𝗲𝘀𝘁 𝗠𝗮𝗴𝗶𝘀𝗸 𝗥𝗲𝗹𝗲𝗮𝘀𝗲:\n" + "\n".join(list(filter(None, map(format_release, ["stable", "beta", "canary"]))))
        disable_web_page_preview=True,
    )
