import logging

import asyncio  # awaits

# import aiograms
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from asyncio.tasks import wait

from lib.c19_api import C19_info

import os

import config


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=MemoryStorage())
# dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    """Func that react at /start command"""
    # Make Keyboard with Regions to search
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for region in C19_info.regions:
        markup.insert(region)

    # send msg to user
    await message.answer(
        "Hello, you can send me name of country to get stats, or use keyboard to get region stats",
        parse_mode="markdown",
        reply_markup=markup,
    )


@dp.message_handler()
async def menu(message: types.Message):
    """Fuction that react when getting any message
    and send getting text to c19 api, to get statistic
    """

    if message.chat.type == "private" and not message.text.startswith("/"):
        c19 = C19_info()
        try:
            # update info to get error if cant get data
            c19.update_data_with(message.text)

            # make country at meddle of msg
            text = "—" * ((36 - len(message.text)) // 2) + message.text
            text += "—" * (36 - len(text))
            text = f"```\n{text}\n```"

            # make inline keyboard with keys to send stats
            markup = types.InlineKeyboardMarkup()
            for key in c19.get_valid_keys():
                markup.insert(
                    types.InlineKeyboardButton(
                        key, callback_data=f"country:{key}:{message.text}"
                    )
                )

            # send msg
            await message.answer(
                text,
                parse_mode="markdown",
                reply_markup=markup,
            )
        except Exception as e:  # if can't update print exception and send user msg that he fuck up
            print(e)
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True
            )
            for region in C19_info.regions:
                markup.insert(region)
            await message.answer(
                "Wrong name, try again",
                parse_mode="markdown",
                reply_markup=markup,
            )


@dp.callback_query_handler(lambda c: c.data.startswith("country:"))
async def get_stats(call: types.CallbackQuery):
    """
    Change msg with stats of 5 country and keyboard to get file
    """
    key, country = call.data.split(":")[1:]  # get key and country name from callback

    # again call to api
    c19 = C19_info()
    c19.update_data_with(country)

    # get text
    text = "".join(list(c19.get_cool_text(key))[:6])
    text = f"```\n{text}```"

    # generate keyboard
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Get file", callback_data=f"getfile:{key}:{country}")
    )

    # send msg
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode="markdown",
        reply_markup=markup,
    )


@dp.callback_query_handler(lambda c: c.data.startswith("getfile:"))
async def get_file(call: types.CallbackQuery):
    """
    Send file to user
    """
    key, country = call.data.split(":")[1:]  # get key and country name from callback

    # again call to api
    c19 = C19_info()
    c19.update_data_with(country)

    # generate filename
    file_name = f"@{call.from_user.username}_{country}_{key}.txt"

    # get text to write on file
    file_text = "".join(list(c19.get_cool_text(key)))
    file_text = file_text.replace("\xe9", "")  # just because this shit cause exception

    file = open(file_name, "w")  # open file

    # try to write text in file
    try:
        file.write(file_text)
        file.close()
    except Exception as e:
        file.close()
        print("\n\n\n\n!!\t\t!!\t", e, "\n\n\n\n")
        await bot.answer_callback_query(call.id, text="Something get wrong, sorry")
        os.remove(file_name)
    else:
        # name that file will have when user get it
        name = f"{country.title()}-{key}.txt"
        text_file = types.InputFile(file_name, name)

        # send file to user
        await bot.send_document(call.message.chat.id, text_file)

        # try del file as long as in exist
        while os.path.exists(file_name):
            try:
                os.remove(file_name)
                break
            except:  # except to ignore that file still used by "await bot.send_document(call.message.chat.id, text_file)"
                pass
            await asyncio.sleep(5)


# start of bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
