import os
from random import choice
from dotenv import load_dotenv
from asyncio import run, sleep
from aiogram import F, Bot, Dispatcher
from aiogram.enums import ChatAction
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN") or ""

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

VOICE_DIR = "voices"

@dp.message(CommandStart())
async def start(message: Message):

    try:
        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
        await message.reply("Hi my name is Ben do you wanna see my dick?")
    except Exception as e:
        print(f"Error: {e}")

@dp.message((F.text.lower().startswith("ben")) | (F.reply_to_message.from_user.id == bot.id))
async def ben(message: Message):

    try:
        voice_files = os.listdir(VOICE_DIR)
        selected_file = choice(voice_files)
        file_path = os.path.join(VOICE_DIR, selected_file)
        voice = FSInputFile(file_path)

        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.RECORD_VOICE)
        await sleep(1)

        await message.reply_voice(voice)
    except Exception as e:
        print(f"Error: {e}")

async def main():
    print("Bot is currently running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        run(main())
    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Bot properly shut down!")