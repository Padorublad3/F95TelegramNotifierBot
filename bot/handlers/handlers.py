from aiogram import Router, types, F
from aiogram.filters import Command
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.models import Entry
import re
from urllib.parse import quote
import feedparser
from utils.validate_entry import validate_entry
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.load_config import load_config
cache = {}
admin_router= Router()
search_url = load_config().get("search_link")
@admin_router.message(Command("list"))
async def cmd_list(message : types.Message, session:Session):
    entries = session.execute(select (Entry)).scalars().all()
    if not entries:
        await message.answer("The list is empty")
    else:
        for entry in entries:
            await message.answer(f"Title: {entry.title} Author: {entry.author} Latest update: {entry.date}")
@admin_router.message(Command("search"))
async def cmd_search(message : types.Message):
    global cache
    global search_url
    cache.clear()
    query = message.text.replace("/search", "").strip()
    if not query:
        return await message.answer("Use /search *title*")
    clean_query = re.sub(r'\b\w{1,3}\b', '', query, flags=re.IGNORECASE)
    clean_query = " ".join(clean_query.split())
    if not clean_query:
        return await message.answer("Invalid request")
    encoded_querry=quote(clean_query)
    url=f"{search_url+encoded_querry}"
    entries = feedparser.parse(url)
    if not entries.entries:
        return await message.answer("Nothing found")
    for i,entry in enumerate(entries.entries):
        valid_entry = validate_entry(entry)
        cache[str(i)] = valid_entry
        kb = InlineKeyboardMarkup(inline_keyboard=[[

            InlineKeyboardButton(
                text="Follow",
                callback_data=f"save_{i}"
            )
        ]


        ])
        response= f"Title: {valid_entry.get('title')},Author: {valid_entry.get('author')}"
        await message.answer(response,reply_markup=kb)

@admin_router.callback_query(F.data.startswith("save_"))
async def callback_save_entry(callback: types.CallbackQuery, session: Session):
    index = callback.data.split("_")[1]
    data = cache.get(index)
    if not data:
        return await callback.answer("data expired, try again")
    exists = session.query(Entry).filter_by(guid = data["guid"]).first()
    if not exists:
        new_entry=Entry(**data)
        session.add(new_entry)
        session.commit()
        await callback.answer("Added to list")
    else:
         await callback.answer("Already in list")
@admin_router.message(F.text)
async def filter_text(message:types.Message):
    await message.answer("Unknown command")

