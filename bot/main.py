# bot/main.py
from config.settings import Settings

def main():
    print("Bot is running with token", Settings.BOT_TOKEN)

if __name__ == "__main__":
    main()
