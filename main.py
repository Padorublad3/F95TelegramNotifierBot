from models.db import DB_Session,init_db
from utils.load_config import load_config
from bot.bot_app import MyBot
from utils.update_checker import sync_entries
import asyncio
import logging

init_db()
logging.basicConfig(level=logging.INFO)
config=load_config()
bot=MyBot(config.get("bot_key"))
async def scheduler(bot,session,config):
    while True:
        if not config.get("chat_id"):
            pass
        else:
            try:
                await sync_entries(bot,session,config.get("chat_id"),config.get("rss_link"))
            except Exception as e:
                print(e)
        await asyncio.sleep(6000)
async def main():
    asyncio.create_task(scheduler(bot.bot,DB_Session,config))
    await bot.start()
if __name__ == "__main__":
    asyncio.run(main())