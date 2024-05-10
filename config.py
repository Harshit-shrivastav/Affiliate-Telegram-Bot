import os

AUTH_USER_ID = int(os.environ.get("AUTH_USER_ID", ""))
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = int(os.environ.get("CHAT_ID", "-1001415884998")) # id of channel where you want to post deals
AMAZON_AFFILIATE_TAG = os.environ.get("AMAZON_AFFILIATE_TAG", "")
FLIPKART_AFFILIATE_TAG = os.environ.get("FLIPKART_AFFILIATE_TAG", "")
CAPTION = os.environ.get("CAPTION", "") #(optional) markdown supported, caption for below post
SESSION = os.environ.get("SESSION", "") # telethon session string to forward contents automatically (Optional)
FROM_CHAT_IDS = list(map(int, getenv("FROM_CHAT_IDS", "").split())) # chat Ids from where you want to forward deals 
TO_CHAT_ID = int(os.environ.get("TO_CHAT_ID", "")) # your bot id
