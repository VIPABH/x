import yt_dlp, os, requests, re, time, wget, random, json 
from yt_dlp import YoutubeDL
from pytube import YouTube
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
    print(f"تشغيل yt_func للمستخدم: {m.from_user.id} في الدردشة: {m.chat.id}")
    if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
        print("النظام غير مفعل لهذه الدردشة.")
        return False

    if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):
        print("المستخدم مكتوم من قبل البوت.")
        return False

    if r.get(f'{m.chat.id}:mute:{Dev_Zaid}') and not admin_pls(m.from_user.id, m.chat.id):
        print("الدردشة مكتومة وليس المستخدم مشرفاً.")
        return False

    text = m.text
    print(f"النص المستلم: {text}")
    
    if isLockCommand(m.from_user.id, m.chat.id, text):
        print("الأمر مقفل على هذا المستخدم.")
        return

    if text.startswith('بحث ') or text.startswith('yt '):
        query = text.split(None, 1)[1]
        print(f"استعلام البحث: {query}")

        try:
            results = Y88F8(query, max_results=1).to_dict()
            print(f"نتائج البحث: {json.dumps(results, indent=2)}")
        except Exception as e:
            print(f"خطأ في البحث: {e}")
            return m.reply("حدث خطأ أثناء البحث.")

        if results:
            res = results[0]
            print(f"أول نتيجة: {res}")
        else:
            print("لا توجد نتائج.")
            return m.reply("لم يتم العثور على نتائج.")

        if ytdb.get(f'ytvideo{res["id"]}'):
            aud = ytdb.get(f'ytvideo{res["id"]}')
            print("الفيديو موجود في قاعدة البيانات.")
            duration_string = time.strftime('%M:%S', time.gmtime(aud["duration"]))
            return m.reply_audio(
                aud["audio"],
                caption=f'@{channel} ~ {duration_string} ⏳',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('🧚‍♀️', url=f'https://t.me/{channel}')]
                ])
            )

        url = f'https://youtu.be/{res["id"]}'
        print(f"الرابط المستهدف: {url}")
        try:
            yt = YouTube(url)
            print(f"عنوان الفيديو: {yt.title}, المؤلف: {yt.author}, المدة: {yt.length}")
        except Exception as e:
            print(f"خطأ في تحميل الفيديو بواسطة pytube: {e}")
            return m.reply("فشل في تحليل الفيديو.")

        try:
            duration_string = time.strftime('%M:%S', time.gmtime(yt.length))
        except Exception as e:
            print(f"خطأ في حساب مدة الفيديو: {e}")
            duration_string = "00:00"

        ydl_ops = {
            "format": "bestaudio[ext=m4a]",
            "username": os.environ.get("u"),
            "password": os.environ.get("p"),
            "forceduration": True,
            "verbose": True
        }

        print(f"خيارات yt-dlp:\n{json.dumps(ydl_ops, indent=2)}")

        try:
            with yt_dlp.YoutubeDL(ydl_ops) as ydl:
                info = ydl.extract_info(url, download=False)
                print(f"معلومات الفيديو: {json.dumps(info, indent=2)}")
                audio_file = ydl.prepare_filename(info)
                ydl.process_info(info)

                print(f"الملف المؤقت: {audio_file}")

                thumb = wget.download(yt.thumbnail_url)
                os.rename(audio_file, audio_file.replace(".m4a", ".mp3"))
                audio_file = audio_file.replace(".m4a", ".mp3")

                a = m.reply_audio(
                    audio_file,
                    title=yt.title,
                    thumb=thumb,
                    duration=yt.length,
                    caption=f'@{channel} ~ {duration_string} ⏳',
                    performer=yt.author,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton('🧚‍♀️', url=f'https://t.me/{channel}')]
                    ])
                )

                print(f"تم إرسال الملف الصوتي بنجاح. ID: {a.audio.file_id}")

                ytdb.set(f'ytvideo{res["id"]}', {
                    "type": "audio",
                    "audio": a.audio.file_id,
                    "duration": a.audio.duration
                })

                os.remove(audio_file)
                os.remove(thumb)

        except Exception as e:
            print(f"خطأ أثناء التحميل أو التحويل: {e}")
            m.reply("فشل في تحميل الفيديو أو معالجته.")
            return
