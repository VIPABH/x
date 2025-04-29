import yt_dlp, os, requests, re, time, wget, random, json 
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch as Y88F8
from threading import Thread
from pyrogram import *
from pyrogram.enums import *
from shazamio import Shazam
from pyrogram.types import *
from config import *
from helpers.Ranks import *
from helpers.Ranks import isLockCommand
from PIL import Image, ImageFilter

shazam = Shazam()

def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":")))
    )

def Find(text):
    m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(m, text)  
    return [x[0] for x in url]

@Client.on_message(filters.text & filters.group, group=32)
def ytdownloaderHandler(c, m):
    k = r.get(f'{Dev_Zaid}:botkey')
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'w7G_BoT'
    Thread(target=yt_func, args=(c, m, k, channel)).start()

def yt_func(c, m, k, channel):
    if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
        return False 
    if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  
        return False
    if r.get(f'{m.chat.id}:mute:{Dev_Zaid}') and not admin_pls(m.from_user.id, m.chat.id):  
        return False 
    if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  
        return False 

    text = m.text
    if isLockCommand(m.from_user.id, m.chat.id, text): 
        return

    rep = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🧚‍♀️', url=f'https://t.me/{channel}')
        ]]
    )

    if text.startswith('بحث ') or text.startswith('yt '):
        query = text.split(None, 1)[1]
        results = Y88F8(query, max_results=1).to_dict()
        if results:
            res = results[0]
        else:
            return m.reply("لم يتم العثور على نتائج.")

        if ytdb.get(f'ytvideo{res["id"]}'):
            aud = ytdb.get(f'ytvideo{res["id"]}')
            duration_string = time.strftime('%M:%S', time.gmtime(aud["duration"]))
            return m.reply_audio(
                aud["audio"],
                caption=f'@{channel} ~ {duration_string} ⏳',
                reply_markup=rep
            )

        url = f'https://youtu.be/{res["id"]}'
        ydl_opts = {
            "format": "bestaudio[ext=m4a]",
            "outtmpl": "%(id)s.%(ext)s",
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_file = f"{info['id']}.m4a"
            duration = info.get("duration", 0)
            duration_string = time.strftime('%M:%S', time.gmtime(duration))
            title = info.get("title", "No Title")
            author = info.get("uploader", "Unknown")
            thumb_url = info.get("thumbnail")

        if thumb_url:
            thumb = wget.download(thumb_url)
        else:
            thumb = None

        os.rename(audio_file, audio_file.replace(".m4a", ".mp3"))
        audio_file = audio_file.replace(".m4a", ".mp3")

        a = m.reply_audio(
            audio_file,
            title=title,
            thumb=thumb,
            duration=duration,
            caption=f'@{channel} ~ {duration_string} ⏳',
            performer=author,
            reply_markup=rep
        )

        ytdb.set(f'ytvideo{res["id"]}', {
            "type": "audio",
            "audio": a.audio.file_id,
            "duration": a.audio.duration
        })

        os.remove(audio_file)
        if thumb:
            os.remove(thumb)
