import requests
from telethon.sync import TelegramClient, events
import re, os
from redislite import Redis
import asyncio
import logging
from telethon.sessions import StringSession
from config import AUTH_USER_ID, API_ID, API_HASH, BOT_TOKEN, CHAT_ID, AMAZON_AFFILIATE_TAG, FLIPKART_AFFILIATE_TAG, CAPTION, SESSION, FROM_CHAT_IDS, TO_CHAT_ID

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("AffiliateBot")
log.info("\n\nStarting...\n")

db = Redis('AffiliateBot.db', decode_responses=True)

client = TelegramClient('affiliateBot', API_ID, API_HASH)

userbot = ''
if SESSION:
    try:
        userbot = TelegramClient(
            StringSession(SESSION), api_id=API_ID, api_hash=API_HASH
        ).start()
    except BaseException as e:
        log.warning(e)
        exit(1)
else:
    print("Session is missing, auto forward wouldn't work")

def expand_url(url):
    response = requests.head(url, allow_redirects=True)
    return response.url


@client.on(events.NewMessage(incoming=True, from_users=AUTH_USER_ID, pattern='/start'))
async def start_handler(event):
    await event.reply(
        "Welcome to the Affiliate Bot!\n\nThis bot can generate Amazon and Flipkart affiliate links for you. Just send any message that contains an Amazon or Flipkart URL, and the bot will reply with the affiliate link."
    )

@client.on(events.NewMessage(incoming=True, from_users=AUTH_USER_ID))
async def handle_message(event):
    message = event.message.message
    url_pattern = r'''\b(?:https?|ftp):\/\/\S+\b'''
    urls = re.findall(url_pattern, message)
    reply_message = ""
    amazon_product_id = db.get('amazon')
    flipkart_product_id = db.get('flipkart')
    if urls:
        for url in urls:
            if ('amzn' in url or 'fkrt' in url):
                expanded_url = expand_url(url)
            else:
                expanded_url = url
            if AMAZON_AFFILIATE_TAG:
                if 'amazon' in expanded_url:
                    if 'tag=' in expanded_url:
                        affiliate_url = re.sub(r'tag=[^&]*', f'tag={AMAZON_AFFILIATE_TAG}', expanded_url)
                    else:
                        affiliate_url = f'{expanded_url}&tag={AMAZON_AFFILIATE_TAG}'
                    match = re.search(r"(https?://[^\s]+)", message)
                    if match:
                        link = match.group(1)
                        preceding_text = message[:match.start()]
                        following_text = message[match.end():]
                        reply_message += f"{preceding_text}{affiliate_url}{following_text}\n\n{CAPTION if CAPTION else ''}"
                     match_ = re.search(r"/dp/([A-Z0-9]{10})", affiliate_url)
                     if match_:
                         product_id = match_.group(1)
                         db.set('amazon', product_id)
            if FLIPKART_AFFILIATE_TAG:
                if 'flipkart' in expanded_url:
                    if 'affid=' in expanded_url:
                        affiliate_url = re.sub(r'affid=[^&]*', f'affid={FLIPKART_AFFILIATE_TAG}', expanded_url)
                    else:
                        affiliate_url = f'{expanded_url}&affid={FLIPKART_AFFILIATE_TAG}'
                    match = re.search(r"(https?://[^\s]+)", message)
                    if match:
                        link = match.group(1)
                        preceding_text = message[:match.start()]
                        following_text = message[match.end():]
                        reply_message += f"{preceding_text}{affiliate_url}{following_text}\n\n{CAPTION if CAPTION else ''}"
                    match_ = re.search(r"/p/([a-zA-Z0-9]+)", affiliate_url)
                    if match_:
                        product_id = match_.group(1)
                        db.set('flipkart', product_id)
    product_id = None
    if 'amazon' in reply_message:
        match = re.search(r"/dp/([A-Z0-9]{10})", affiliate_url)
        if match:
            product_id = match.group(1)
    elif 'flipkart' in reply_message:
        match = re.search(r"/p/([a-zA-Z0-9]+)", affiliate_url)
        if match:
            product_id = match.group(1)

    if product_id == amazon_product_id or product_id == flipkart_product_id:
        return

    if 'tag=' in reply_message:
        existing_tag = re.search(r'tag=([^&]*)', affiliate_url).group(1)
        if existing_tag != AMAZON_AFFILIATE_TAG:
            return
    elif 'affid=' in reply_message:
        existing_tag = re.search(r'affid=([^&]*)', affiliate_url).group(1)
        if existing_tag != FLIPKART_AFFILIATE_TAG:
            return

    if reply_message and not 'amzn.to' in reply_message and not 'fkrt.it' in reply_message and not 't.me' in reply_message:
        try:
            await client.send_message(CHAT_ID, reply_message, link_preview=False)
            await asyncio.sleep(500)
            db.delete('amazon', 'flipkart')
        except Exception as e:
            print(e)
            await event.reply(reply_message, link_preview=False)
            await asyncio.sleep(500)
            db.delete('amazon', 'flipkart')

if SESSION:
    @userbot.on(events.NewMessage(incoming=True, chats=FROM_CHAT))
    async def autopost(event):
        if not event.is_private:
            try:
                await userbot.send_message(TO_CHAT, event.message, link_preview=False)
            except Exception as e:
                print(e)

client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
if SESSION:
    userbot.run_until_disconnected()
