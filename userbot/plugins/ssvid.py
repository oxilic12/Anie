import asyncio
import os
import time

from telethon.tl.types import DocumentAttributeFilename

from userbot import bot
from userbot.utils import progress, register


@register(outgoing=True, pattern=r"^\.ssvid(?: |$)(.*)")
async def ssvideo(framecap):
    if not framecap.reply_to_msg_id:
        return await framecap.edit("`reply to video!`")
    reply_message = await framecap.get_reply_message()
    if not reply_message.media:
        return await framecap.edit("`reply to a video!`")
    try:
        frame = int(framecap.pattern_match.group(1))
        if frame > 10:
            return await framecap.edit("`hey..dont put that much`")
    except BaseException:
        return await framecap.edit("`Please input number of frame!`")
    if (
        reply_message.photo
        or (
            DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
            in reply_message.media.document.attributes
        )
        or (
            DocumentAttributeFilename(file_name="sticker.catp")
            in reply_message.media.document.attributes
        )
    ):
        return await framecap.edit("`Unsupported files!`")
    c_time = time.time()
    await framecap.edit("`Downloading media...`")
    ss = await bot.download_media(
        reply_message,
        "anu.mp4",
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, framecap, c_time, "[DOWNLOAD]")
        ),
    )
    try:
        await framecap.edit("`Proccessing...`")
        command = f"vcsi -g {frame}x{frame} {ss} -o ss.png "
        os.system(command)
        await framecap.client.send_file(
            framecap.chat_id,
            "ss.png",
            reply_to=framecap.reply_to_msg_id,
        )
        await framecap.delete()
    except BaseException as e:
        await framecap.edit(f"{e}")
    os.system("rm -rf *.png *.mp4")
