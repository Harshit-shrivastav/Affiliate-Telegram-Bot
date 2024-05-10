import os

AUTH_USER_ID = int(os.environ.get("AUTH_USER_ID", "5979279455"))
API_ID = int(os.environ.get("API_ID", "4680197"))
API_HASH = os.environ.get("API_HASH", "495b0228624028d635bd748b22985f67")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6186291688:AAFVfMLORpFh9O3v9IKrbo1G7ljV6ncLbOM")
CHAT_ID = int(os.environ.get("CHAT_ID", "-1001415884998")) # id of channel where you want to post deals
AMAZON_AFFILIATE_TAG = os.environ.get("AMAZON_AFFILIATE_TAG", "")
FLIPKART_AFFILIATE_TAG = os.environ.get("FLIPKART_AFFILIATE_TAG", "")
CAPTION = os.environ.get("CAPTION", "**🔥 @DigiDealz**")
SESSION = os.environ.get("SESSION", "") # telethon session string to forward contents automatically (Optional)
FROM_CHAT_IDS = list(map(int, getenv("FROM_CHAT_IDS", "-1001315464303 -1001420742409 -1001241952303").split())) # chat Ids from where you want to forward deals 
TO_CHAT_ID = int(os.environ.get("TO_CHAT_ID", "1538581563")) # your bot id
