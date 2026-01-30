import feedparser
from sqlalchemy import select
from models.models import Entry
from aiogram import Bot
from sqlalchemy.orm import Session
from utils.validate_entry import validate_entry
async def sync_entries(bot:Bot,session:Session,chat_id,link):
    entries=feedparser.parse(link)
    with session() as session:
        for entry in entries.entries:
            entry=validate_entry(entry)
            query = select(Entry).where(Entry.guid == entry["guid"])
            _db=session.execute(query).scalar_one_or_none()

            if _db and _db.date != entry["date"]:
                _db.date = entry["date"]
                _db.title = entry["title"]
                session.commit()
                await bot.send_message(chat_id,f"{_db.title} gets an update!")

