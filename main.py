import time, redis, os, json, re, requests, asyncio 
from pyrogram import *
r = redis.Redis('localhost',decode_responses=True)
print(r)
to_config = """
import redis
r = redis.Redis('localhost',decode_responses=True)
"""

print('''
Loading…
█▒▒▒▒▒▒▒▒▒''')
print('\n\n')
BOT_TOKEN = os.getenv("BOT_TOKEN")  # من ملف .env
token = BOT_TOKEN
try:
  from information import *
  Dev_Zaid = token.split(':')[0]
  r.set(f'{Dev_Zaid}botowner', owner_id)
except Exception as e:
  with open ('information.py','w+') as www:
     Dev_Zaid = token.split(':')[0]
     if not r.get(f'{Dev_Zaid}botowner'):
       owner_id = 7811364724
       r.set(f'{Dev_Zaid}botowner', owner_id)
     else:
        owner_id = int(r.get(f'{Dev_Zaid}botowner'))
     text = 'token = "{}"\nowner_id = {}'
     www.write(text.format(token, owner_id))

    


if not r.get(f'{Dev_Zaid}botowner'):
    owner_id = int(input('[+] Enter SUDO ID : '))
    r.set(f'{Dev_Zaid}botowner', owner_id)
else:
    owner_id = int(r.get(f'{Dev_Zaid}botowner'))
print('''
10% 
███▒▒▒▒▒▒▒ ''')

to_config += f"\ntoken = '{token}'"
to_config += f"\nDev_Zaid = token.split(':')[0]"
to_config += f"\nsudo_id = {owner_id}"
username = "kkajdjwjbot"
to_config += f"\nbotUsername = '{username}'"
to_config += "\nfrom kvsqlite.sync import Client as DB"
to_config += "\nytdb = DB('ytdb.sqlite')"
to_config += "\nsounddb = DB('sounddb.sqlite')"
to_config += "\nwsdb = DB('wsdb.sqlite')"

print('''
30% 
█████▒▒▒▒▒ ''')
with open('config.py','w+') as w:
  w.write(to_config)
print('''
50% 
███████▒▒▒ ''')
API_ID = os.getenv("API_ID")  # من ملف .env
API_HASH = os.getenv("API_HASH")  # من ملف .env
BOT_TOKEN = os.getenv("BOT_TOKEN")  # من ملف .env
token = BOT_TOKEN
app = Client(f'{Dev_Zaid}r3d', API_ID, API_HASH, bot_token=BOT_TOKEN,
    plugins={"root": "Plugins"}
  )
# userbot = Client('userbott', 9398500, "ad2977d673006bed6e5007d953301e13", session_string="BACPaOQAw9EWMijb1D8m_wYGIa2r6tnaNiJDVTuC4jVktrtF5K7UxjNuZNcA-HpmEBltGr-0rUrELER9Vj0CmkNb28BdGYGETl5dJIg386wdjv3ZYNB3HkYrbhN5GFE4w2tYNv5dQJmvLTtvC3bTa0HoW64YLPINX_3BEZSoyXPm_bbXonA_2PIqeA1MHdEzfg_U4Zy75xyBq0pBvTv6xhD9hpAliXHnapJ5gg4C8Qt4QX4JLMGYxaSTNt51OClNVpPU6yiKZBFYl-t6CP66VmL3JU3P3HshrCSlcY38GfZ7Uy_w1b7HCqqe9EnVmZV0k3S29YtFlGz9Z0uuw0pxloAFpebeTwAAAABydGQqAA")
  
if not r.get(f'{Dev_Zaid}:botkey'):
    r.set(f'{Dev_Zaid}:botkey', '⇜')

if not r.get(f'{Dev_Zaid}botname'):
    r.set(f'{Dev_Zaid}botname', 'رعد')

if not r.get(f'{Dev_Zaid}botchannel'):
    r.set(f'{Dev_Zaid}botname', 'eFFb0t')

def Find(text):
  m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
  url = re.findall(m,text)  
  return [x[0] for x in url]

app.start()
# userbot.start()
print('''
[===========================]

█████╗░██████╗░██████╗░
██╔══██╗╚════██╗██╔══██╗
██████╔╝░█████╔╝██║░░██║
██╔══██╗░╚═══██╗██║░░██║
██║░░██║██████╔╝██████╔╝
╚═╝░░╚═╝╚═════╝░╚═════╝░

[===========================]

🔮 Your bot started successfully on R 3 D ☆ Source 🔮

•••••••• @yqyqy66 - @yqyqy66 •••••••••


''')
print('''

100% 
██████████''')
if r.get(f'DevGroup:{Dev_Zaid}'):
  id = int(r.get(f'DevGroup:{Dev_Zaid}'))
  try:
    app.send_message(id, "تم اتشغيل البوت بنجاح ✔️")
  except:
    pass
idle()
  
