import requests
from telethon.sync import TelegramClient, events
import re, os
import pickledb_ujson as pickledb
import asyncio
from os import environ, getenv
import logging
from telethon.sessions import StringSession

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("AffliateBot")
log.info("\n\nStarting...\n")

# Global variables 
AUTH = int(os.environ.get("AUTH", "5979279455"))
API_ID = int(os.environ.get("API_ID", "4680197"))
API_HASH = os.environ.get("API_HASH", "495b0228624028d635bd748b22985f67")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6186291688:AAFVfMLORpFh9O3v9IKrbo1G7ljV6ncLbOM")
CHAT_ID = int(os.environ.get("CHAT_ID", "-1001415884998"))
AMAZON_AFFILIATE_TAG = os.environ.get("AMAZON_AFFILIATE_TAG", "digideals06-21")
FLIPKART_AFFILIATE_TAG = os.environ.get("FLIPKART_AFFILIATE_TAG", "")
CAPTION = os.environ.get("CAPTION", "**🔥 @DigiDealz**")
SESSION = os.environ.get("SESSION", "1AZWarzgBuwhufhbVFn42BFL4Fvmkxl4NO7DpNno8FSOS230e5R9BYhL-NOg8PohLtEwqhxoH3a_TW1cAozKPpiJrSnaBmXqApprTk7eFnQ94YgfP7TTstMWRO391ZD7LwekWE8fcQlHYgbJMw0-KDXt85juAUz4atM2hAooSUCJPJuFtGbebRjmLGaNehA-BTmAPdgoCQEjuRQvdo2Z9xbAsFnVnzvdB4hhElXEMSINg7uB7wk0dAPaRcs9Bn_3aivL0fwogyHATa2e98d1v1ADN42TRP7uzWItpWuSxFn3K6xYLQehrk57upRxEXwMAjlgPevuovZJdU83Pzejj6hoUq6qkyH4=")
FROM_CHAT = list(map(int, getenv("FROM_CHAT", "-1001315464303 -1001420742409 -1001241952303").split()))
TO_CHAT = int(os.environ.get("TO_CHAT", "1538581563"))

# Telegram client for bot 
client = TelegramClient('affiliate_bot', API_ID, API_HASH)

# Telegram userbot client for userbot 
try:
    userbot = TelegramClient(
        StringSession(SESSION), api_id=API_ID, api_hash=API_HASH
    ).start()
except BaseException as e:
    log.warning(e)
    exit(1)#Creating Telegram userbot client for userbot 
try:
    userbot = TelegramClient(
        StringSession(SESSION), api_id=API_ID, api_hash=API_HASH
    ).start()
except BaseException as e:
    log.warning(e)
    exit(1)

# Load database 
db = pickledb.load('pickle.db', False)

# start message handler
@client.on(events.NewMessage(incoming=True, from_users=AUTH, pattern='/start'))
async def handle_start(event):
    await event.reply(
        "Welcome to the Affiliate Bot!\n\nThis bot can generate Amazon and Flipkart affiliate links for you. Just send any message that contains an Amazon or Flipkart URL, and the bot will reply with the affiliate link."
    )

def expand_url(url):
    response = requests.head(url, allow_redirects=True)
    return response.url

# incoming message handler 
@client.on(events.NewMessage(incoming=True, from_users=AUTH))
async def handle_message(event):
    message = event.message.message
    url_pattern = r'''\b(?:https?|ftp):\/\/\S+\b'''
    urls = re.findall(url_pattern, message)
    reply_message = ""
    x = db.get('amazon')
    print('got amazon product id', x)
    y = db.get('flipkart')
    print('got flipkart product id', y)
    if urls:
        for url in urls:
            if ('amzn' in url or 'fkrt' in url):
                expanded_url = expand_url(url)
            else:
                expanded_url = url
            if 'amazon' in expanded_url:
                if 'tag=' in expanded_url:
                    affiliate_url = re.sub(r'tag=[^&]*', f'tag={AMAZON_AFFILIATE_TAG}', expanded_url)
                    
                else:
                    affiliate_url = f'{expanded_url}&tag={AMAZON_AFFILIATE_TAG}'
                pattern = r"(https?://[^\s]+)"
                match = re.search(pattern, message)
                if match:
                    link = match.group(1)
                    print('link: ', link)
                    preceding_text = message[:match.start()]
                    following_text = message[match.end():]
                    reply_message += f'{preceding_text}{affiliate_url}{following_text}\n\n{CAPTION}'
#------------------------------------>
                patern = r"/dp/([A-Z0-9]{10})"
                math = re.search(patern, affiliate_url)
                if math:
                     product_id = math.group(1)
                     db.set('amazon', product_id)
                     print('set amazon', product_id)
#------------------------------------>
            elif 'flipkart' in expanded_url:
                if 'affid=' in expanded_url:
                    affiliate_url = re.sub(r'affid=[^&]*', f'affid={FLIPKART_AFFILIATE_TAG}', expanded_url)
                else:
                    affiliate_url = f'{expanded_url}&affid={FLIPKART_AFFILIATE_TAG}'
                pattern = r"(https?://[^\s]+)"
                match = re.search(pattern, message)
                if match:
                    link = match.group(1)
                    preceding_text = message[:match.start()]
                    following_text = message[match.end():]
                    reply_message += f'{preceding_text}{affiliate_url}{following_text}\n\n{CAPTION}'
  #------------------------------------>
                patterna = r"/p/([a-zA-Z0-9]+)"
                matcha = re.search(patterna, affiliate_url)
                if matcha:
                    product_id = matcha.group(1)
                    db.set('flipkart', product_id)
                    print('set flipkart', product_id)

  #------------------------------------>
    xxx = None   
    if 'amazon' in reply_message: 
        pattern = r"/dp/([A-Z0-9]{10})" 
        match = re.search(pattern, affiliate_url) 
        if match: 
            xxx = match.group(1) 
            print('xxx amazon', xxx) 
    elif 'flipkart' in reply_message: 
        pattern = r"/p/([a-zA-Z0-9]+)" 
        match = re.search(pattern, affiliate_url) 
        if match: 
            xxx = match.group(1) 
            print('xxx Flipkart', xxx) 
    else: 
        print('lol') 
    if xxx == x or xxx == y:  
        print(f'trying to match {xxx} == {x} or {xxx} == {y}')  
        return
    if 'tag=' in reply_message:
        existing_tag = re.search(r'tag=([^&]*)', affiliate_url).group(1)
        if existing_tag != AMAZON_AFFILIATE_TAG:
            return
    elif 'affid=' in reply_message:
        existing_tag = re.search(r'affid=([^&]*)', affiliate_url).group(1)
        if existing_tag != FLIPKART_AFFILIATE_TAG:
            return
    else:
        pass
    if reply_message and not 'amzn.to' in reply_message and not 'fkrt.it' in reply_message and not 't.me' in reply_message and not 'dl' in reply_message:
        try:
            await client.send_message(CHAT_ID, reply_message, link_preview=False)
            await asyncio.sleep(500)
            try:
                db.rem('amazon')
                db.rem('flipkart')
                print('removed x')
            except:
                pass
        except Exception as e:
            print(e)
            await event.reply(reply_message, link_preview=False)
            await asyncio.sleep(500)
            try:
                db.rem('amazon')
                db.rem('flipkart')
            except:
                pass
#Auto Forward 
@userbot.on(events.NewMessage(incoming=True, chats=FROM_CHAT)) 
async def autopost(event): 
    if not event.is_private:
        try:
            await userbot.send_message(TO_CHAT, event.message, link_preview=False)
        except Exception as e:
            print(e)

print('Affiliate Bot started. Written by Harshit Shrivastav.')
client.start(bot_token=BOT_TOKEN)
userbot.run_until_disconnected()
client.run_until_disconnected()

