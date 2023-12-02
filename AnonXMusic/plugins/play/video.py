
import os
import requests

import aiohttp
import aiofiles

import config
import yt_dlp
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InputTextMessageContent
from youtube_search import YoutubeSearch

from AnonXMusic import app

def remove_if_exists(path):
    if os.path.exists(path):
        os.remove(path)


@app.on_message(filters.command(["/song", "تنزيل", "/music"],""))
async def song_downloader(client, message: Message):
    query = " ".join(message.command[1:])
    m = await message.reply_text("<b>⇜ جـارِ التنزيل عـن المقطـع الصـوتـي . . .</b>")
    ydl_ops = {
        'format': 'bestvideo[ext=m4a]',
        'keepvideo': True,
        'prefer_ffmpeg': False,
        'geo_bypass': True,
        'outtmpl': '%(title)s.%(ext)s',
        'quite': True,
    }
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        await m.edit("- لم يتم العثـور على نتائج ؟!\n- حـاول مجـدداً . . .")
        print(str(e))
        return
    await m.edit("<b>⇜ جـارِ التحميل ▬▭ . . .</b>")
    try:
        with yt_dlp.YoutubeDL({"quiet": True}) as ytdl:
            info_dict = ydl.extract_info(link, download=False)
            video_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"✧ <a href=https://t.me/Mlze1bot> 𝑺𝒐𝒖𝒓𝒄𝒆 𝒅𝒊𝒏𝒂 </a> : @{app.username} "
        host = str(info_dict["upload_audio"])
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await m.edit("<b>⇜ جـارِ الرفـع ▬▬ . . .</b>")
        await message.reply_video(
            video=video_file,
            caption=rep,
            title=title,
            performer=host,
            thumb=thumb_name,
            duration=dur,
        )
        await m.delete()

    except Exception as e:
        await m.edit(" error, wait for bot owner to fix")
        print(e)

    try:
        remove_if_exists(video_file)
        remove_if_exists(thumb_name)
    except Exception as e:
        print(e)
