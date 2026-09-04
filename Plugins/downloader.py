import yt_dlp, os, re, time, wget, json
from youtube_search import YoutubeSearch as Y88F8
from threading import Thread
from pyrogram import Client, filters
from pyrogram.enums import *
from shazamio import Shazam
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from helpers.Ranks import *
from helpers.Ranks import isLockCommand

shazam = Shazam()

channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'x04ou'

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))

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
    if text.startswith('بحث'):
     if r.get(f'{m.chat.id}:disableYT:{Dev_Zaid}'):  return
     if r.get(f':disableYT:{Dev_Zaid}'):  return
     query = text.split(None,1)[1]
     keyboard= []
     results=Y88F8(query,max_results=4).to_dict()
     for res in results:
       title = res['title']
       id = res['id']
       keyboard.append([InlineKeyboardButton (title, callback_data=f'{m.from_user.id}GET{id}')])     
     a = m.reply(f'{k} البحث ~ {query}',reply_markup=InlineKeyboardMarkup (keyboard), disable_web_page_preview=True)
     r.set(f'{a.id}:one_minute:{m.from_user.id}', 1, ex=60)
     return True

    if text.startswith('يوت') or text.startswith('yt '):
      parts = text.split(None, 1)
      if len(parts) < 2:
          return m.reply("يرجى إدخال اسم الأغنية أو الرابط بعد الأمر.")
      
      query = parts[1]

      results = Y88F8(query, max_results=1).to_dict()

      if not results:
          return m.reply("لم يتم العثور على نتائج.")

      res = results[0]
      video_id = res["id"]

      cached_audio = ytdb.get(f'ytvideo{video_id}')
      if cached_audio:
          duration_string = time.strftime('%M:%S', time.gmtime(cached_audio.get("duration", 0)))
          return m.reply_audio(
              cached_audio["audio"],
              caption=f'@{channel} ~ {duration_string} ⏳',
              reply_markup=rep
          )

      url = f'https://youtu.be/{video_id}'
      ydl_ops = {
        'format': 'bestaudio/best',
        'cookiefile': 'cookies.txt',
        'remote_components': ['ejs:github'],
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'forceduration': True,
        'noplaylist': True,
        'outtmpl': f'downloads/{video_id}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

      audio_file = None
      thumb_file = None

      try:
          with yt_dlp.YoutubeDL(ydl_ops) as ydl:
              info = ydl.extract_info(url, download=True)
              title = info.get('title', 'Audio')
              duration = int(info.get('duration', 0))
              thumbnail = info.get('thumbnail')
              uploader = info.get('uploader', 'YouTube')
              
              # تحديد مسار ملف الـ MP3 الناتج بدقة
              downloaded_file = ydl.prepare_filename(info)
              audio_file = os.path.splitext(downloaded_file)[0] + ".mp3"

          # التحقق من وجود الملف على القرص قبل المتابعة
          if not os.path.exists(audio_file):
              return m.reply("❌ تعذر العثور على الملف الصوتي بعد التحميل.")

          duration_string = time.strftime('%M:%S', time.gmtime(duration))

          # تحميل الصورة المصغرة إن وجدت
          if thumbnail:
              try:
                  thumb_file = wget.download(thumbnail, out=f"downloads/thumb_{video_id}.jpg")
              except Exception:
                  thumb_file = None

          # 3. إرسال الصوت لليوزر
          sent_audio = m.reply_audio(
              audio_file,
              title=title,
              thumb=thumb_file,
              duration=duration,
              caption=f'{channel} love u ~ {duration_string} ⏳',
              performer=uploader,
              reply_markup=rep
          )

          # 4. الحفظ في قاعدة البيانات
          if sent_audio and getattr(sent_audio, 'audio', None):
              ytdb.set(f'ytvideo{video_id}', {
                  "type": "audio",
                  "audio": sent_audio.audio.file_id,
                  "duration": sent_audio.audio.duration
              })

      except Exception as e:
          print(f"حدث خطأ أثناء تحميل الفيديو: {e}")
          m.reply("حدث خطأ أثناء التحميل، يرجى المحاولة لاحقًا.")

      finally:
          # 5. تنظيف الملفات المؤقتة
          if audio_file and os.path.exists(audio_file):
              os.remove(audio_file)
          if thumb_file and os.path.exists(thumb_file):
              os.remove(thumb_file)
