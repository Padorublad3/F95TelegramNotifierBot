
import logging
from aiogram import Bot, Dispatcher,Router
from .handlers.start import start_router
from .handlers.handlers import admin_router
from models.db import DB_Session
from .middleware.db import DbSessionMiddleware
logging.basicConfig(level=logging.INFO)

class MyBot:
    def __init__(self,token: str):
        self.bot = Bot(token)
        self.dp = Dispatcher()
        self.router = Router()
        self.router.include_router(start_router)
        self.router.include_router(admin_router)
        self.dp.include_router(self.router)
        self.dp.update.middleware(DbSessionMiddleware(DB_Session))
    async def start(self):
        await self.dp.start_polling(self.bot)
        
