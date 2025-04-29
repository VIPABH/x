import yt_dlp,os, requests, re, time, wget, random, json 
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
  url = re.findall(m,text)  
  return [x[0] for x in url]
@Client.on_message(filters.text & filters.group, group=32)
def ytdownloaderHandler(c,m):
    k = r.get(f'{Dev_Zaid}:botkey')
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'w7G_BoT'
    Thread(target=yt_func,args=(c,m,k,channel)).start()
def yt_func(c,m,k,channel):
   if not r.get(f'{m.chat.id}:enable:{Dev_Zaid}'):
        return False 
   if r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}'):  return False
   if r.get(f'{m.chat.id}:mute:{Dev_Zaid}') and not admin_pls(m.from_user.id,m.chat.id):  return False 
   if r.get(f'{m.from_user.id}:mute:{Dev_Zaid}'):  return False 
   text = m.text
   if isLockCommand(m.from_user.id, m.chat.id, text): return
   rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url=f'https://t.me/{channel}')
     ]]
   )
if text.startswith('بحث ') or text.startswith('yt '):
    # إذا كانت خاصية تعطيل البحث مفعلة
    # if r.get(f'{m.chat.id}:disableYT:{Dev_Zaid}') or r.get(f':disableYT:{Dev_Zaid}'):  
        # return
    
    # استخراج الاستعلام من النص
    query = text.split(None, 1)[1]
    
    # البحث في Y88F8
    results = Y88F8(query, max_results=1).to_dict()
    
    # التأكد من وجود نتائج
    # if results:
    #     res = results[0]
    # else:
    #     return m.reply("لم يتم العثور على نتائج.")
    
    # التحقق من وجود الفيديو في قاعدة البيانات
    if ytdb.get(f'ytvideo{res["id"]}'):
        aud = ytdb.get(f'ytvideo{res["id"]}')
        duration_string = time.strftime('%M:%S', time.gmtime(aud["duration"]))
        m.reply_audio(
            aud["audio"],
            caption=f'@{channel} ~ {duration_string} ⏳',
            reply_markup=rep
        )
        # return m.reply_audio(
        #     aud["audio"],
        #     caption=f'@{channel} ~ {duration_string} ⏳',
        #     reply_markup=rep
        # )
    
    # رابط الفيديو
    url = f'https://youtu.be/{res["id"]}'
    cc = 1  # غير واضح ما هو المقصود من `cc`، إذا كانت غير مهمة يمكنك حذفها
    print(url, cc)

    # تحميل الفيديو من YouTube باستخدام yt_dlp
    yt = YouTube(url)
    duration_string = time.strftime('%M:%S', time.gmtime(yt.length))

    # إعدادات التحميل
    ydl_ops = {
        "format": "bestaudio[ext=m4a]",
        'forceduration': True,
        "username": "oauth2",  # تحقق من البيانات الخاصة باليوزر
        "password": ''  # تحقق من وجود كلمة المرور إذا كانت ضرورية
    }

    # تحميل الفيديو
    with yt_dlp.YoutubeDL(ydl_ops) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            audio_file = ydl.prepare_filename(info)
            ydl.process_info(info)
            thumb = wget.download(yt.thumbnail_url)
            
            # تحويل الملف إلى MP3
            os.rename(audio_file, audio_file.replace(".m4a", ".mp3"))
            audio_file = audio_file.replace(".m4a", ".mp3")

            # إرسال الصوت
            a = m.reply_audio(
                audio_file,
                title=yt.title,
                thumb=thumb,
                duration=yt.length,
                caption=f'@{channel} ~ {duration_string} ⏳',
                performer=yt.author,
                reply_markup=rep
            )
            
            # حفظ البيانات في قاعدة البيانات
            ytdb.set(f'ytvideo{res["id"]}', {
                "type": "audio",
                "audio": a.audio.file_id,
                "duration": a.audio.duration
            })

            # تنظيف الملفات المؤقتة
            os.remove(audio_file)
            os.remove(thumb)

            # return True

        # except Exception as e:
        #     # التعامل مع الأخطاء بشكل مناسب
        #     print(f"حدث خطأ أثناء تحميل الفيديو: {e}")
        #     return m.reply("حدث خطأ أثناء تحميل الفيديو. حاول مرة أخرى.")
