from os import getenv
from random import choice
from dotenv import load_dotenv
from aiohttp import ClientSession
from asyncio import run, sleep, create_task
from logging import basicConfig, getLogger, INFO
from aiohttp.web import Application, AppRunner, TCPSite, Response
from aiogram import F, Bot, Dispatcher
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

load_dotenv()
basicConfig(format="BEN - %(levelname)s - %(message)s")

BOT_TOKEN = getenv("BOT_TOKEN", "")
RENDER_URL = getenv("RENDER_EXTERNAL_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logger = getLogger(__name__)
logger.setLevel(INFO)

VOICES = [
    "voices/hohoho.ogg",
    "voices/no.ogg",
    "voices/silly.ogg",
    "voices/yes.ogg",
]

async def health(request):
    return Response(text="Okay", content_type="text/plain")

async def alive():

    if not RENDER_URL:
        logger.info("Render link not found")
        return

    while True:
        await sleep(1 * 60)
        try:
            session = ClientSession()
            await session.get(f"{RENDER_URL}/healthz")
            logger.debug(f"Pinged {RENDER_URL} to stay alive")
            await session.close()
        except Exception as e:
            logger.error(f"Keep-alive error: {e}")

    logger.info("Up time task is active")

async def poke():

    app = Application()
    app.router.add_get('/', health)
    app.router.add_get('/healthz', health)
    runner = AppRunner(app, access_log=None)

    await runner.setup()
    site = TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

    create_task(alive())

@dp.message(CommandStart())
async def start(message: Message):

    try:
        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
        await message.reply("Hi my name is Ben do you wanna see my dick?")
    except Exception as e:
        logger.error(f"Error: {e}")

@dp.message((F.text.lower().startswith("ben")))
async def ben(message: Message):

    try:
        voice = FSInputFile(choice(VOICES))
        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.RECORD_VOICE)
        await sleep(1)
        await message.reply_voice(voice)
    except Exception as e:
        logger.error(f"Error: {e}")

async def main():
    
    await poke()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        run(main())
        logger.info("Bot is currently running")
    except Exception as e:
        logger.error(f"Bot startup failed: {e}")
    except KeyboardInterrupt:
        logger.info("Bot properly shut down!")