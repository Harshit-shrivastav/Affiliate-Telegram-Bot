# 🤖 Affiliate-Telegram-Bot

Affiliate-Telegram-Bot is a Telegram bot designed to generate affiliate links for Amazon and Flipkart URLs, making it easier to monetize your content on telegram. 💰

## Features

✨ Generate Amazon and Flipkart affiliate links  
✨ Automatic tagging of affiliate links with your affiliate IDs  
✨ Customizable captions for affiliate links  
✨ Automatic forwarding contents from other channels

### 🆓 If you want a free bot hosting checkout this article here:
https://github.com/Harshit-shrivastav/Free-Telegram-bot-hosting

## Getting Started

To get started with Affiliate-Telegram-Bot, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Harshit-shrivasta/Affiliate-Telegram-Bot.git
   ```
2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your Telegram bot token, API keys, and other configurations in the `config.py` file.** 🛠️

## Usage

1. **Start the bot by running:**
   ```bash
   python main.py
   ```
2. **Send any message containing an Amazon or Flipkart URL to the bot.** 📨
3. **The bot will reply with the affiliate link generated for the provided URL.** 💬

## Customization

You can customize the bot's behavior by modifying the `main.py` file:

- **Configure your Amazon and Flipkart affiliate IDs.** 💳
- **Customize the default caption for affiliate links.** ✏️
- **Optionally provide a Telegram session string for auto-forwarding messages.** 🔄

## Generating Telethon Session String

If you don't already have a Telethon session string, you can generate one on the [Telegram.tools](https://telegram.tools/session-string-generator#telethon,user). Once generated, copy the session string and use it as `SESSION` var for auto-forwarding messages.

## Contributing

Contributions are welcome! If you encounter any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request. 🚀

## License

This project is licensed under the [MIT License](LICENSE). 📝
