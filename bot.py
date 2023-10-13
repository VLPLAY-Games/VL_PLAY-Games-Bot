import os, uuid, imageio, io, speech_recognition as sr, moviepy.editor as mp, pytesseract, random, hashlib, wikipediaapi, requests
from aiogram.utils import executor
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from pytube import YouTube
from moviepy.editor import *
from pydub import AudioSegment
from PIL import Image
from datetime import datetime, timezone
from langdetect import detect
from gtts import gTTS
from config import version, token,  commands

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
global bot_language
bot_language = "en"

CommandsKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
CommandsKeyboard.add(
    KeyboardButton("/start"),
    KeyboardButton("/language"),
    KeyboardButton("/commands"),
    KeyboardButton("/download_youtube_video"),
    KeyboardButton("/convert_mp4_to_mp3"), 
    KeyboardButton("/convert_mov_to_mp4"), 
    KeyboardButton("/convert_webm_to_mp4"), 
    KeyboardButton("/convert_mp3_to_wav"), 
    KeyboardButton("/convert_mp4_to_gif"), 
    KeyboardButton("/convert_png_to_jpeg"), 
    KeyboardButton("/convert_ico_to_jpg"), 
    KeyboardButton("/convert_webp_to_jpg"), 
    KeyboardButton("/audio_recognition_rus"),
    KeyboardButton("/audio_recognition_en"),
    KeyboardButton("/image_text_recognition"),
    KeyboardButton("/text_to_audio"),
    KeyboardButton("/password_generator"),
    KeyboardButton("/hash_calculator"),
    KeyboardButton("/search_wikipedia"),
    KeyboardButton("/currency"),
)
inlineKeyboardStart = InlineKeyboardMarkup()
inlineKeyboardStart.add(
    InlineKeyboardButton("VL_PLAY Games", callback_data="games"),
    InlineKeyboardButton("Discord Server" if bot_language == "en"  else "Discord сервер", callback_data="discord"),
    InlineKeyboardButton("Youtube channel" if bot_language == "en"  else "Youtube канал", callback_data="youtube"),
    InlineKeyboardButton("About Bot" if bot_language == "en"  else "Информация о боте", callback_data="about_bot"),
    InlineKeyboardButton("Commands" if bot_language == "en"  else "Команды", callback_data="commands"),
)
inlineKeyboardGames = InlineKeyboardMarkup()
inlineKeyboardGames.add(
    InlineKeyboardButton("Qlake", callback_data="qlake"),
    InlineKeyboardButton("Silent Darkness", callback_data="sd"),
    InlineKeyboardButton("Game engine" if bot_language == "en"  else "Игровой движок", callback_data="engine"),
)
inlineKeyboardQlake = InlineKeyboardMarkup()
inlineKeyboardQlake.add(
    InlineKeyboardButton("Release Date" if bot_language == "en"  else "Дата выхода", callback_data="qlake_date"),
    InlineKeyboardButton("About Qlake" if bot_language == "en"  else "Обо Qlake", callback_data="qlake_about"),
    InlineKeyboardButton("Link" if bot_language == "en"  else "Ссылка", callback_data="qlake_link"),
    InlineKeyboardButton("System Requirements" if bot_language == "en"  else "Системные требования", callback_data="qlake_sr"),
    InlineKeyboardButton("Trailer" if bot_language == "en"  else "Трейлер", callback_data="qlake_trailer"),
)
inlineKeyboardSD = InlineKeyboardMarkup()
inlineKeyboardSD.add(
    InlineKeyboardButton("Release Date" if bot_language == "en"  else "Дата выхода", callback_data="sd_date"),
    InlineKeyboardButton("About Silent Darkness" if bot_language == "en"  else "Обо Silent Darkness", callback_data="sd_about"),
    InlineKeyboardButton("Link" if bot_language == "en"  else "Ссылка", callback_data="sd_link"),
    InlineKeyboardButton("System Requirements" if bot_language == "en"  else "Системные требования", callback_data="sd_sr"),
    InlineKeyboardButton("Trailer" if bot_language == "en"  else "Трейлер", callback_data="sd_trailer"),
)

inlineKeyboardHash = InlineKeyboardMarkup()
inlineKeyboardHash.add(
    InlineKeyboardButton("MD5", callback_data="hash_md5"),
    InlineKeyboardButton("SHA-1", callback_data="hash_sha1"),
    InlineKeyboardButton("SHA-256", callback_data="hash_sha256"),
    InlineKeyboardButton("SHA-512", callback_data="hash_sha512"),
)

inlineKeyboardWiki = InlineKeyboardMarkup()
inlineKeyboardWiki.add(
    InlineKeyboardButton("Rus", callback_data="wiki_rus"),
    InlineKeyboardButton("Eng", callback_data="wiki_en"),
)

inlineKeyboardCurrency = InlineKeyboardMarkup()
inlineKeyboardCurrency.add(
    InlineKeyboardButton("USD", callback_data="cur_usd"),
    InlineKeyboardButton("EUR", callback_data="cur_eur"),
    InlineKeyboardButton("GBP", callback_data="cur_gbp"),
    InlineKeyboardButton("JPY", callback_data="cur_jpy"),
    InlineKeyboardButton("KZT", callback_data="cur_kzt"),
    InlineKeyboardButton("GEL", callback_data="cur_gel"),
    InlineKeyboardButton("AED", callback_data="cur_aed"),
    InlineKeyboardButton("TRY", callback_data="cur_try"),
    InlineKeyboardButton("RUB", callback_data="cur_rub"),
)

inlineKeyboardLanguage = InlineKeyboardMarkup()
inlineKeyboardLanguage.add(
    InlineKeyboardButton("Русский", callback_data="lang_ru"),
    InlineKeyboardButton("English", callback_data="lang_en"),
)

@dp.message_handler(commands=['help'])
async def help_command_reply(msg: types.Message):
    await bot.send_message(msg.chat.id,"Bot creator - VL_PLAY" if bot_language == "en"  else "Создатель бота - VL_PLAY")


@dp.callback_query_handler(lambda call: True)
async def callback_message(call: types.CallbackQuery):
    # Start
    global bot_language
    if call.data == "games":
        await bot.edit_message_text("VL_PLAY Games", call.message.chat.id,call.message.message_id,reply_markup=inlineKeyboardGames)
    elif call.data == "discord":
        await bot.send_message(call.message.chat.id, "https://discord.gg/mYaUdA4BMS")
    elif call.data == "youtube":
        await bot.send_message(call.message.chat.id, "https://www.youtube.com/@VladPlay021")
    elif call.data == "about_bot":
        await bot.send_message(call.message.chat.id, "VL_PLAY Games Bot" + version)
    elif call.data == "commands":
        await bot.send_message(call.message.chat.id, commands  if bot_language == "en"  else  "/start - запуск бота\n/language - смена языка\n/commands - команды бота\n/download_youtube_video - скачать видео с YouTube \n/convert_mp4_to_mp3 - конвертировать видео mp4 в формат mp3\n/convert_mov_to_mp4 - конвертировать mov видео в формат mp4\ n/convert_webm_to_mp4 - конвертировать видео WebM в формат mp4\n/convert_mp3_to_wav - конвертировать аудио mp3 в формат wav\n/convert_mp4_to_gif - конвертировать видео mp4 в формат gif\n/convert_png_to_jpeg - конвертировать изображение png в формат jpeg\n/convert_ico_to_jpg - конвертировать ico картинка в формат jpg\n/convert_webp_to_jpg - конвертировать webp картинку в формат jpg\n/audio_recognition_rus - распознавание текста в аудиофайле на русском языке\n/audio_recognition_en - распознавание текста в аудиофайле на английском языке\n/image_text_recognition - распознавание текста изображения из формат png или jpg (en-ru)\n/text_to_audio - конвертировать текст в аудио\n/password_generator - генератор паролей по длине\n/hash_calculator - расчет хеша файла\n/search_wikipedia - поиск информации в википедии\n/currency - получить список цен на покупку данной валюты в разных валютах", reply_markup=CommandsKeyboard)
    elif call.data == "engine":
        await bot.send_message(call.message.chat.id, "VL_PLAY использует Unreal Engine 5 во всех своих играх."  if bot_language == "ru"  else "VL_PLAY uses Unreal Engine 5 in all its games")

    # Qlake
    elif call.data == "qlake":
        await bot.edit_message_text("Qlake", call.message.chat.id,call.message.message_id,reply_markup=inlineKeyboardQlake)
    elif call.data == "qlake_date":
        await bot.send_message(call.message.chat.id, "Qlake was released March 30, 2023 on itch.io" if bot_language == "en" else "Qlake был выпущен 30 марта 2023 г. на itch.io.")
    elif call.data == "qlake_about":
        await bot.send_message(call.message.chat.id, "Qlake is an intense first-person shooter in the survival horror genre, developed on the Unreal Engine 5. In the game, the player has to fight zombies and their leader, who is the main objective of the game. Players will progress through multiple levels, each with a unique set of challenges and dangers. Players will look for weapons and ammo that can help them deal with evil and survive each level. Qlake is a game that will strain your nerves and force players to use all their survival skills to complete each level and defeat the villains. If you are a survival horror game lover, then playing Qlake will probably be an interesting and exciting experience for you."  if bot_language == "en" else "Qlake — это напряженный шутер от первого лица в жанре Survival Horror, разработанный на движке Unreal Engine 5. В игре игроку предстоит сражаться с зомби и их лидером, что и является основной целью игры. Игрокам предстоит пройти несколько уровней, каждый из которых имеет уникальный набор задач и опасностей. Игроки будут искать оружие и боеприпасы, которые помогут им справиться со злом и выжить на каждом уровне. Qlake — игра, которая напрягает ваши нервы и заставит игроков использовать все свои навыки выживания, чтобы пройти каждый уровень и победить злодеев. Если вы любитель игр ужасов выживания, то игра в Qlake наверняка станет для вас интересным и увлекательным занятием.")
    elif call.data == "qlake_link":
        await bot.send_message(call.message.chat.id, "https://vl-play.itch.io/qlake")
    elif call.data == "qlake_sr":
        await bot.send_message(call.message.chat.id, "Minimum \nCPU    i5-4690K and above \nRAM    4GB \n GPU    Vega 8 (gtx 750ti)  and above \nFree Space 9GB \nNote    1080p low ~ 30fps at different levels in different ways \n\nRecommended \nCPU    i5-8600k and above \nRAM    8GB \nGPU     Gtx 1660 and above \nFree Space 9GB \nNote 1080p ultra ~30fps at different levels in different ways" if bot_language == "en" else "Минимум \nЦП i5-4690K и выше \nОЗУ 4 ГБ \n Графический процессор Vega 8 (gtx 750ti) и выше \nСвободное пространство 9 ГБ \nПримечание: 1080p низкая ~ 30 кадров в секунду на разных уровнях по-разному \n\nРекомендуется \nЦП i5-8600k и выше \ nRAM 8 ГБ \nGPU Gtx 1660 и выше \nСвободное пространство 9 ГБ \nNote 1080p Ultra ~30 кадров в секунду на разных уровнях по-разному")
    elif call.data == "qlake_trailer":
        await bot.send_message(call.message.chat.id, "https://www.youtube.com/watch?v=E8vI3LdvRXk")

    # Silent Darkness
    elif call.data == "sd":
        await bot.edit_message_text("Silent Darkness", call.message.chat.id,call.message.message_id,reply_markup=inlineKeyboardSD)
    elif call.data == "sd_date":
        await bot.send_message(call.message.chat.id, "The game is under development. Game release date unknown" if bot_language == "en" else "Игра находится в стадии разработки. Дата выхода игры неизвестна")
    elif call.data == "sd_about":
        await bot.send_message(call.message.chat.id, "The game is under development. Game description unknown" if bot_language == "en" else "Игра находится в стадии разработки. Описание игры неизвестно")
    elif call.data == "sd_link":
        await bot.send_message(call.message.chat.id, "The game is under development. Link unknown" if bot_language == "en" else "Игра находится в стадии разработки. Ссылка неизвестна")
    elif call.data == "sd_sr":
        await bot.send_message(call.message.chat.id, "The game is under development. System Requirements unknown" if bot_language == "en" else "Игра находится в стадии разработки. Системные требования неизвестны")
    elif call.data == "sd_trailer":
        await bot.send_message(call.message.chat.id, "https://www.youtube.com/watch?v=XL64mRXdtAs")

    # Hash
    elif call.data == "hash_md5":
        global method_hash
        method_hash = 'md5'
        await bot.send_message(call.message.chat.id, "Send file:" if bot_language == "en" else "Отправьте файл")
        await HashCalcState.waiting_for_file.set()

    elif call.data == "hash_sha1":
        method_hash = "sha1"
        await bot.send_message(call.message.chat.id, "Send file:" if bot_language == "en" else "Отправьте файл")
        await HashCalcState.waiting_for_file.set()
    elif call.data == "hash_sha256":
        method_hash = "sha256"
        await bot.send_message(call.message.chat.id, "Send file:" if bot_language == "en" else "Отправьте файл")
        await HashCalcState.waiting_for_file.set()
    elif call.data == "hash_sha512":
        method_hash = "sha512"
        await bot.send_message(call.message.chat.id, "Send file:" if bot_language == "en" else "Отправьте файл")
        await HashCalcState.waiting_for_file.set()

    # Wikipedia
    elif call.data == "wiki_rus":
        global wiki_lang
        wiki_lang = 'ru'
        await bot.send_message(call.message.chat.id, "Submit a text:" if bot_language == "en" else "Отправьте текст")
        await searchWikiState.waiting_for_text.set()
    elif call.data == "wiki_en":
        wiki_lang = 'en'
        await bot.send_message(call.message.chat.id, "Submit a text:" if bot_language == "en" else "Отправьте текст")
        await searchWikiState.waiting_for_text.set()

    # Currency
    elif call.data == "cur_usd":
        global cur_val
        cur_val = 'USD'
        await show_currency_values(call.message)
    elif call.data == "cur_eur":
        cur_val = 'EUR'
        await show_currency_values(call.message)
    elif call.data == "cur_gbp":
        cur_val = 'GBP'
        await show_currency_values(call.message)
    elif call.data == "cur_jpy":
        cur_val = 'JPY'
        await show_currency_values(call.message)
    elif call.data == "cur_kzt":
        cur_val = 'KZT'
        await show_currency_values(call.message)
    elif call.data == "cur_gel":
        cur_val = 'GEL'
        await show_currency_values(call.message)
    elif call.data == "cur_aed":
        cur_val = 'AED'
        await show_currency_values(call.message)
    elif call.data == "cur_try":
        cur_val = 'TRY'
        await show_currency_values(call.message)
    elif call.data == "cur_rub":
        cur_val = 'RUB'
        await show_currency_values(call.message)
    # Язык
    elif call.data == "lang_ru":
        bot_language = 'ru'
        await bot.send_message(call.message.chat.id, "Выбранный язык: Русский")

    elif call.data == "lang_en":
        bot_language = 'en'
        await bot.send_message(call.message.chat.id, "Selected language: English")


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await bot.send_message(msg.chat.id, "How can I help you?" if bot_language == "en" else "Могу я чем-нибудь помочь?", reply_markup=inlineKeyboardStart)

@dp.message_handler(commands=['language'])
async def bot_languge_select(message: types.Message):
    await message.reply('Select language:' if bot_language == "en" else "Выберите язык:", reply_markup=inlineKeyboardLanguage)
    


class DownloadState(StatesGroup):
    waiting_for_link = State()

@dp.message_handler(commands=['download_youtube_video'])
async def download_youtube_video_command(message: types.Message):
    await bot.send_message(message.chat.id, 'Enter YouTube video link.' if bot_language == "en" else "Введите ссылку на видео YouTube")
    await DownloadState.waiting_for_link.set()

@dp.message_handler(state=DownloadState.waiting_for_link)
async def handle_youtube_video(message: types.Message, state: FSMContext):
    try:
        await message.reply("Downloading video... \nThis may take a few minutes." if bot_language == "en" else "Скачивание видео... \nЭто может занять несколько минут.")
        url = message.text
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        await bot.send_chat_action(chat_id=message.chat.id, action="upload_video")
        video.download('./')
        filename = video.default_filename
        video_file = open(filename, 'rb')
        await bot.send_video(message.chat.id, video_file)
        video_file.close()
        os.remove(filename)
        await message.reply("Downloading complete." if bot_language == "en" else "Скачивание завершено.")
    except Exception as e:
        await message.reply('An error occurred while downloading video from YouTube.' if bot_language == "en" else "Произошла ошибка при загрузке видео с YouTube.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e) + version)
        report.close()
    await state.finish()

class ConvertStateMp4Mp3(StatesGroup):
    waiting_for_video = State()

@dp.message_handler(commands=['convert_mp4_to_mp3'])
async def convert_mp4_to_mp3_command(message: types.Message):
    await message.reply("Please send an MP4 video file to convert to MP3." if bot_language == "en" else "Пожалуйста, отправьте видеофайл MP4 для конвертации в MP3.")
    await ConvertStateMp4Mp3.waiting_for_video.set()

@dp.message_handler(content_types=types.ContentType.VIDEO, state=ConvertStateMp4Mp3.waiting_for_video)
async def handle_mp4_to_mp3(message: types.Message, state: FSMContext):
    try:
        if message.video and message.video.mime_type == 'video/mp4':
            await message.reply('Converting video to audio... \nThis may take a few minutes.' if bot_language == "en" else "Преобразование видео в аудио... \nЭто может занять несколько минут.")
            await bot.send_chat_action(chat_id=message.chat.id, action="upload_audio")
            file_info = await bot.get_file(message.video.file_id)
            downloaded_file = await bot.download_file(file_info.file_path)
            uuid_str = str(uuid.uuid4())
            with open(uuid_str + '.mp4', 'wb') as f:
                f.write(downloaded_file.getvalue())
            audio = AudioSegment.from_file(uuid_str + '.mp4', 'mp4')
            audio.export(uuid_str + '.mp3', format='mp3')
            with open(uuid_str + '.mp3', 'rb') as f:
                await bot.send_audio(message.chat.id, f)
            os.remove(uuid_str + '.mp4')
            os.remove(uuid_str + '.mp3')
            await message.reply('Conversion complete.' if bot_language == "en" else "Преобразование завершено.")
        else:
            await message.reply('Please send an MP4 video file.' if bot_language == "en" else "Пожалуйста, пришлите видеофайл в формате MP4.")
    except Exception as e:
        await message.reply('An error occurred during conversion.' if bot_language == "en" else "Во время конвертации произошла ошибка.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e) + version)
        report.close()
    await state.finish()


class ConvertStateMp4Wav(StatesGroup):
    waiting_for_audio = State()

@dp.message_handler(commands=['convert_mp3_to_wav'])
async def convert_mp3_to_wav_command(message: types.Message):
    await message.reply("Please send an MP3 audio file to convert to WAV." if bot_language == "en" else "Пожалуйста, отправьте аудиофайл MP3 для конвертации в WAV.")
    await ConvertStateMp4Wav.waiting_for_audio.set()

@dp.message_handler(content_types=types.ContentType.AUDIO, state=ConvertStateMp4Wav.waiting_for_audio)
async def handle_mp3_to_wav(message: types.Message, state: FSMContext):
    try:
        if message.audio and message.audio.mime_type == 'audio/mpeg':
            await message.reply('Converting audio to WAV... \nThis may take a few minutes.' if bot_language == "en" else "Преобразование аудио в WAV... \nЭто может занять несколько минут.")
            await bot.send_chat_action(chat_id=message.chat.id, action="upload_audio")
            file_info = await bot.get_file(message.audio.file_id)
            downloaded_file = await bot.download_file(file_info.file_path)
            uuid_str = str(uuid.uuid4())
            mp3_filename = uuid_str + '.mp3'
            wav_filename = uuid_str + '.wav'
            with open(mp3_filename, 'wb') as f:
                f.write(downloaded_file.getvalue())
            sound = AudioSegment.from_mp3(mp3_filename)
            sound.export(wav_filename, format='wav')
            with open(wav_filename, 'rb') as f:
                await bot.send_audio(message.chat.id, f)
            os.remove(mp3_filename)
            os.remove(wav_filename)
            await message.reply('Conversion complete.' if bot_language == "en" else "Преобразование завершено.")
        else:
            await message.reply('Please send an MP3 audio file.' if bot_language == "en" else "Пожалуйста, пришлите видеофайл в формате MP3.")
    except Exception as e:
        await message.reply('An error occurred during conversion.' if bot_language == "en" else "Во время конвертации произошла ошибка.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()


class ConvertStateMP4Gif(StatesGroup):
    waiting_for_video = State()

@dp.message_handler(commands=['convert_mp4_to_gif'])
async def convert_mp4_to_gif_command(message: types.Message):
    await message.reply("Please send an MP4 video file to convert to GIF." if bot_language == "en" else "Пожалуйста, отправьте видеофайл MP4 для конвертации в GIF.")
    await ConvertStateMP4Gif.waiting_for_video.set()

@dp.message_handler(content_types=types.ContentType.VIDEO, state=ConvertStateMP4Gif.waiting_for_video)
async def handle_mp4_to_gif(message: types.Message, state: FSMContext):
    try:
        if message.video and message.video.mime_type == 'video/mp4':
            await message.reply('Converting video to GIF... \nThis may take a few minutes.' if bot_language == "en" else "Преобразование видео в GIF... \nЭто может занять несколько минут.")
            await bot.send_chat_action(chat_id=message.chat.id, action="upload_video")
            file_info = await bot.get_file(message.video.file_id)
            downloaded_file = await bot.download_file(file_info.file_path)
            file_name = str(uuid.uuid4()) + '.mp4'
            gif_file_name = str(uuid.uuid4()) + '.gif'
            with open(file_name, 'wb') as f:
                f.write(downloaded_file.getvalue())
            with imageio.get_reader(file_name) as reader:
                with imageio.get_writer(gif_file_name, mode='I') as writer:
                    for i,frame in enumerate(reader):
                        writer.append_data(frame)
            with open(gif_file_name, 'rb') as f:
                await bot.send_document(message.chat.id, f)
            await message.reply('Conversion complete.' if bot_language == "en" else "Преобразование завершено.")
            os.remove(file_name)
            os.remove(gif_file_name)
        else:
            await message.reply('Please send an MP4 video file.' if bot_language == "en" else "Пожалуйста, пришлите видеофайл в формате MP4.")
    except Exception as e:
        await message.reply('Error occurred during conversion.' if bot_language == "en" else "Во время конвертации произошла ошибка.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()
    await state.finish()

class ConvertStatePngJpeg(StatesGroup):
    waiting_for_image = State()

@dp.message_handler(commands=['convert_png_to_jpeg'])
async def convert_png_to_jpeg_command(message: types.Message):
    await message.reply("Please send a PNG image to convert to JPEG." if bot_language == "en" else "Пожалуйста, отправьте картинку PNG для конвертации в JPEG.")
    await ConvertStatePngJpeg.waiting_for_image.set()

@dp.message_handler(content_types=types.ContentType.PHOTO, state=ConvertStatePngJpeg.waiting_for_image)
async def handle_png_to_jpeg(message: types.Message, state: FSMContext):
    try:
        if message.photo:
            await message.reply('Converting image to JPEG... \nThis may take a few minutes.' if bot_language == "en" else "Преобразование картинки в JPEG... \nЭто может занять несколько минут.")
            await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
            file_info = await bot.get_file(message.photo[-1].file_id)
            file = await bot.download_file(file_info.file_path)
            img = Image.open(io.BytesIO(file.getvalue()))
            buffer = io.BytesIO()
            img.save(buffer, "JPEG", quality=90)
            buffer.seek(0)
            await bot.send_photo(message.chat.id, buffer)
            await message.reply('Conversion complete.' if bot_language == "en" else "Преобразование завершено.")
        else:
            await message.reply('Please send a PNG image.' if bot_language == "en" else "Пожалуйста, пришлите картинку в формате PNG.")
    except Exception as e:
        await message.reply('An error occurred during conversion.' if bot_language == "en" else "Во время конвертации произошла ошибка.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()
    await state.finish()

class ConvertARE(StatesGroup):
    waiting_for_audio = State()

@dp.message_handler(commands=['audio_recognition_en'])
async def audio_recognition_en(message: types.Message):
    await bot.send_message(message.chat.id, 'Send a mp3 audio file.' if bot_language == "en" else "Отправьте аудиофайл MP3.")
    await ConvertARE.waiting_for_audio.set()

@dp.message_handler(content_types=types.ContentType.AUDIO, state=ConvertARE.waiting_for_audio)
async def handle_audio_recognition_en(message: types.Message, state: FSMContext):
    try:
        if message.audio and message.audio.mime_type == "audio/mpeg":
            await message.reply("Audio conversion... \nThis may take a few minutes." if bot_language == "en" else "Преобразование аудио... \nЭто может занять несколько минут.")
            await bot.send_chat_action(chat_id=message.chat.id, action="typing")
            file_info = await bot.get_file(message.audio.file_id)
            audio_file = await bot.download_file(file_info.file_path)
            file_name = str(uuid.uuid4()) + '.mp3'
            with open(file_name, 'wb') as f:
                f.write(audio_file.getvalue())
            wav_file_name = await convert_to_wav(message, file_name)
            r = sr.Recognizer()
            with sr.AudioFile(wav_file_name) as source:
                audio = r.record(source)
            text = r.recognize_google(audio, language='en-EN')
            await bot.send_message(message.chat.id, text)
            os.remove(file_name)
            os.remove(wav_file_name)
            await message.reply('Recognition complete.' if bot_language == "en" else "Распознавание завершено.")
        else:
            await message.reply("Please send an MP3 file." if bot_language == "en" else "Пожалуйста, пришлите аудиофайл в формате MP3.")
    except Exception as e:
        await message.reply("An error occurred during audio conversion." if bot_language == "en" else "Во время конвертации аудио произошла ошибка.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e) + version)
        report.close()
    await state.finish()

class ConvertARR(StatesGroup):
    waiting_for_audio = State()

@dp.message_handler(commands=['audio_recognition_rus'])
async def audio_recognition_rus(message: types.Message):
    await bot.send_message(message.chat.id, 'Send a mp3 audio file.' if bot_language == "en" else "Отправьте аудиофайл MP3.")
    await ConvertARR.waiting_for_audio.set()

@dp.message_handler(content_types=types.ContentType.AUDIO, state=ConvertARR.waiting_for_audio)
async def handle_audio_recognition_rus(message: types.Message, state: FSMContext):
    try:
        if message.audio and message.audio.mime_type == "audio/mpeg":
            await message.reply("Audio conversion... \nThis may take a few minutes." if bot_language == "en" else "Преобразование аудио... \nЭто может занять несколько минут.")
            await bot.send_chat_action(chat_id = message.chat.id, action = "typing")
            file_info = await bot.get_file(message.audio.file_id)
            audio_file = await bot.download_file(file_info.file_path)
            file_name = str(uuid.uuid4()) + '.mp3'
            with open(file_name, 'wb') as f:
                f.write(audio_file.getvalue())
            wav_file_name = await convert_to_wav(message, file_name)
            r = sr.Recognizer()
            with sr.AudioFile(wav_file_name) as source:
                audio = r.record(source)
            text = r.recognize_google(audio, language='ru-RU')
            await bot.reply(text)
            os.remove(file_name)
            os.remove(wav_file_name)
            await message.reply('Recognition complete.' if bot_language == "en" else "Распознавание завершено.")
        else:
            await message.reply("Please send a MP3 file." if bot_language == "en" else "Пожалуйста, пришлите аудиофайл в формате MP3.")
    except Exception as e:
        await message.reply("A error occurred while Audio conversion." if bot_language == "en" else "Во время конвертации аудио произошла ошибка.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e) + version)
        report.close()
    await state.finish()

async def convert_to_wav(message, file_path):
    file_name = os.path.splitext(file_path)[0]
    sound = AudioSegment.from_mp3(file_path)
    wav_file_path = file_name + '.wav'
    sound.export(wav_file_path, format='wav')
    await bot.send_message(message.chat.id, "Audio conversion completed. Text recognising..." if bot_language == "en" else "Преобразование аудио завершено. Распознавание текста...")
    return wav_file_path


class ConvertStateMovMp4(StatesGroup):
    waiting_for_video = State()

@dp.message_handler(commands=['convert_mov_to_mp4'])
async def convert_mov_to_mp4_command(message: types.Message):
    await message.reply('Send a MOV video file.' if bot_language == "en" else "Отправьте видеофайл MOV.")
    await ConvertStateMovMp4.waiting_for_video.set()

@dp.message_handler(content_types=types.ContentType.VIDEO, state=ConvertStateMovMp4.waiting_for_video)
async def handle_convert_mov_to_mp4(message: types.Message, state: FSMContext):
    try:
        if message.video and message.video.mime_type == "video/quicktime":
            await message.reply("Converting video... \nThis may take a few minutes." if bot_language == "en" else "Преобразование видео... \nЭто может занять несколько минут.")
            await bot.send_chat_action(chat_id=message.chat.id, action="upload_video")
            file_info = await bot.get_file(message.video.file_id)
            video_file = await bot.download_file(file_info.file_path)
            file_name = str(uuid.uuid4()) + '.mov'
            with open(file_name, 'wb') as f:
                f.write(video_file.getvalue())
            mp4_file_name = file_name.replace('.mov', '.mp4')
            clip = mp.VideoFileClip(file_name)
            clip.write_videofile(mp4_file_name)
            with open(mp4_file_name, 'rb') as f:
                video_buffer = io.BytesIO(f.read())
            await bot.send_video(message.chat.id, video_buffer)
            os.remove(file_name)
            os.remove(mp4_file_name)
            await message.reply('Conversion complete.' if bot_language == "en" else "Преобразование завершено.")
        else:
            await message.reply("Please send a MOV video file." if bot_language == "en" else "Пожалуйста, пришлите видеофайл в формате MOV.")
    except Exception as e:
        await message.reply("An error occurred while converting the video." if bot_language == "en" else "Во время конвертации видео произошла ошибка.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()

class ConvertStateWebmMp4(StatesGroup):
    waiting_for_webm = State()

@dp.message_handler(commands=['convert_webm_to_mp4'])
async def convert_webm_to_mp4_command(message: types.Message):
    await message.reply('Send a webm video file.' if bot_language == "en" else "Отправьте видеофайл webm.")
    await ConvertStateWebmMp4.waiting_for_webm.set()

@dp.message_handler(content_types=types.ContentType.VIDEO, state=ConvertStateWebmMp4.waiting_for_webm)
async def handle_convert_webm_to_mp4(message: types.Message, state: FSMContext):
    try:
        if message.video and message.video.mime_type == "video/webm":
            await message.reply("Converting video... \nThis may take a few minutes." if bot_language == "en" else "Преобразование видео... \nЭто может занять несколько минут.")
            await bot.send_chat_action(chat_id=message.chat.id, action="upload_video")
            file_info = await bot.get_file(message.video.file_id)
            video_file = await bot.download_file(file_info.file_path)
            uuid_str = str(uuid.uuid4())
            with open(uuid_str + '.webm', 'wb') as f:
                f.write(video_file.getvalue())
            clip = mp.VideoFileClip(uuid_str + '.webm')
            clip.write_videofile(uuid_str + '.mp4')
            with open(uuid_str + '.mp4', 'rb') as f:
                video_buffer = io.BytesIO(f.read())
            await bot.send_video(message.chat.id, video_buffer)
            os.remove(uuid_str + '.webm')
            os.remove(uuid_str + '.mp4')
            await message.reply('Conversion complete.' if bot_language == "en" else "Преобразование завершено.")
        else:
            await message.reply("Please send a WebM video file." if bot_language == "en" else "Пожалуйста, пришлите видеофайл в формате WebM.")
    except Exception as e:
        await message.reply("An error occurred while converting the video." if bot_language == "en" else "Во время конвертации видео произошла ошибка.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()
    await state.finish()

class ConvertStateWebpJpg(StatesGroup):
    waiting_for_webp = State()

@dp.message_handler(commands=['convert_webp_to_jpg'])
async def convert_webp_to_jpg_command(message: types.Message):
    await message.reply('Send a WebP image file.' if bot_language == "en" else "Отправьте картинку WebP.")
    await ConvertStateWebpJpg.waiting_for_webp.set()

@dp.message_handler(content_types=types.ContentType.PHOTO, state=ConvertStateWebpJpg.waiting_for_webp)
async def handle_convert_webp_to_jpg(message: types.Message, state: FSMContext):
    try:
        if message.photo:
            await message.reply("Converting image... \nThis may take a few minutes." if bot_language == "en" else "Преобразование картинки... \nЭто может занять несколько минут.")
            await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
            file_info = await bot.get_file(message.photo[-1].file_id)
            image_file = await bot.download_file(file_info.file_path)
            uuid_str = str(uuid.uuid4())
            with open(uuid_str + '.webp', 'wb') as f:
                f.write(image_file.getvalue())
            with Image.open(uuid_str + '.webp') as im:
                im = im.convert('RGB')
                im.save(uuid_str + '.jpg', 'JPEG')
            with open(uuid_str + '.jpg', 'rb') as f:
                jpg_buffer = io.BytesIO(f.read())
            await bot.send_photo(message.chat.id, jpg_buffer)
            os.remove(uuid_str + '.webp')
            os.remove(uuid_str + '.jpg')
            await message.reply('Conversion complete.' if bot_language == "en" else "Преобразование завершено.")
        else:
            await message.reply("Please send a WebP image." if bot_language == "en" else "Пожалуйста, пришлите картинку в формате WebP.")
    except Exception as e:
        await message.reply("An error occurred while converting the image." if bot_language == "en" else "Во время конвертации картинки произошла ошибка.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()
    await state.finish()

class ConvertStateIcoJpg(StatesGroup):
    waiting_for_ico = State()

@dp.message_handler(commands=['convert_ico_to_jpg'])
async def convert_ico_to_jpg_command(message: types.Message):
    await message.reply('Send an ICO image file.' if bot_language == "en" else "Отправьте картинку ICO.")
    await ConvertStateIcoJpg.waiting_for_ico.set()

@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=ConvertStateIcoJpg.waiting_for_ico)
async def handle_convert_ico_to_jpg(message: types.Message, state: FSMContext):
    try:
        if message.document and message.document.mime_type == 'image/x-icon':
            await message.reply("Converting image... \nThis may take a few minutes." if bot_language == "en" else "Преобразование картинки... \nЭто может занять несколько минут.")
            await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
            file_info = await bot.get_file(message.document.file_id)
            image_file = await bot.download_file(file_info.file_path)
            uuid_str = str(uuid.uuid4())
            with open(uuid_str + '.ico', 'wb') as f:
                f.write(image_file.getvalue())
            with Image.open(uuid_str + '.ico') as im:
                im = im.convert('RGB')
                im.save(uuid_str + '.jpg', 'JPEG')
            with open(uuid_str + '.jpg', 'rb') as f:
                jpg_buffer = io.BytesIO(f.read())
            await bot.send_photo(message.chat.id, jpg_buffer)
            os.remove(uuid_str + '.ico')
            os.remove(uuid_str + '.jpg')
            await message.reply('Conversion complete.' if bot_language == "en" else "Преобразование завершено.")
        else:
            await message.reply("Please send an ICO image." if bot_language == "en" else "Пожалуйста, пришлите картинку в формате ICO.")
    except Exception as e:
        await message.reply("An error occurred while converting the image." if bot_language == "en" else "Во время конвертации картинки произошла ошибка.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()
    await state.finish()

class OCRState(StatesGroup):
    waiting_for_image = State()

@dp.message_handler(commands=['image_text_recognition'])
async def image_text_recognition_command(message: types.Message):
    await message.reply('Send a PNG or JPEG image file.' if bot_language == "en" else "Отправьте картинку PNG или JPEG.")
    await OCRState.waiting_for_image.set()

@dp.message_handler(content_types=types.ContentType.PHOTO, state=OCRState.waiting_for_image)
async def handle_image_text_recognition(message: types.Message, state: FSMContext):
    try:
        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.document and message.document.mime_type in ['image/png', 'image/jpeg']:
            file_id = message.document.file_id
        else:
            await message.reply('Please send a PNG or JPEG image file.' if bot_language == "en" else "Пожалуйста, пришлите картинку в формате PNG или JPEG.")
            return

        await message.reply("Performing OCR... \nThis may take a few minutes." if bot_language == "en" else "Выполнение оптического распознавания символов... \nЭто может занять несколько минут.")
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        file_info = await bot.get_file(file_id)
        image_file = await bot.download_file(file_info.file_path)
        uuid_str = str(uuid.uuid4())
        with open(uuid_str + '.png', 'wb') as f:
            f.write(image_file.getvalue())

        with Image.open(uuid_str + '.png') as im:
            text = pytesseract.image_to_string(im, lang='rus+eng')

        await bot.send_message(message.chat.id, text)
        os.remove(uuid_str + '.png')
        await message.reply('OCR complete.' if bot_language == "en" else "Оптического распознавание символов завершено.")
    except Exception as e:
        await message.reply("An error occurred while performing OCR." if bot_language == "en" else "Произошла ошибка при выполнении Выполнение оптического распознавания символов")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()

    await state.finish()

@dp.message_handler(commands=['commands'])
async def image_text_recognition(message):
    await bot.send_message(message.chat.id, commands, reply_markup=CommandsKeyboard)

class ConvertStateWebpJpg(StatesGroup):
    waiting_for_webp = State()

@dp.message_handler(commands=['convert_webp_to_jpg'])
async def convert_webp_to_jpg_command(message: types.Message):
    await message.reply('Send a WebP image file.' if bot_language == "en" else "Отправьте картинку WebP.")
    await ConvertStateWebpJpg.waiting_for_webp.set()

@dp.message_handler(content_types=types.ContentType.PHOTO, state=ConvertStateWebpJpg.waiting_for_webp)
async def handle_convert_webp_to_jpg(message: types.Message, state: FSMContext):
    try:
        if message.photo:
            await message.reply("Converting image... \nThis may take a few minutes." if bot_language == "en" else "Преобразование картинки... \nЭто может занять несколько минут.")
            await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
            file_info = await bot.get_file(message.photo[-1].file_id)
            image_file = await bot.download_file(file_info.file_path)
            uuid_str = str(uuid.uuid4())
            with open(uuid_str + '.webp', 'wb') as f:
                f.write(image_file.getvalue())
            with Image.open(uuid_str + '.webp') as im:
                im = im.convert('RGB')
                im.save(uuid_str + '.jpg', 'JPEG')
            with open(uuid_str + '.jpg', 'rb') as f:
                jpg_buffer = io.BytesIO(f.read())
            await bot.send_photo(message.chat.id, jpg_buffer)
            os.remove(uuid_str + '.webp')
            os.remove(uuid_str + '.jpg')
            await message.reply('Conversion complete.' if bot_language == "en" else "Преобразование завершено.")
        else:
            await message.reply("Please send a WebP image." if bot_language == "en" else "Пожалуйста, пришлите картинку в формате WebP.")
    except Exception as e:
        await message.reply("An error occurred while converting the image." if bot_language == "en" else "Во время конвертации картинки произошла ошибка.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()
    await state.finish()

class PasswordGeneratorState(StatesGroup):
    waiting_for_length = State()

@dp.message_handler(commands=['password_generator'])
async def password_generator_command(message: types.Message):
    await message.reply('Enter password length:' if bot_language == "en" else "Введите длину пароля:")
    await PasswordGeneratorState.waiting_for_length.set()

@dp.message_handler(state=PasswordGeneratorState.waiting_for_length)
async def handle_password_generator(message: types.Message, state: FSMContext):
    try:
        if not message.text.isdigit():
            raise ValueError("Input should be a number")
        chars_for_password = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        password = ''
        await message.reply("Password generation... \nThis may take a few minutes." if bot_language == "en" else "Генерация пароля... \nЭто может занять несколько минут.")
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        for i in range(int(message.text)):
            password += random.choice(chars_for_password)
        await bot.send_message(message.chat.id, password)
    except ValueError as ve:
        await message.reply(str(ve))
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(ve))
        report.close()
    except Exception as e:
        await message.reply(message, "An error occurred while password generation." if bot_language == "en" else "Во время генерации пароля произошла ошибка.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()
    await state.finish()

class TextToAudioState(StatesGroup):
    waiting_for_text = State()

@dp.message_handler(commands=['text_to_audio'])
async def text_to_audio_command(message: types.Message):
    await message.reply('Enter the text you want to convert to audio:' if bot_language == "en" else "Введите текст, который вы хотите преобразовать в аудио:")
    await TextToAudioState.waiting_for_text.set()

@dp.message_handler(state=TextToAudioState.waiting_for_text)
async def handle_text_to_audio(message: types.Message, state: FSMContext):
    try:
        await message.reply("Converting text to audio... \nThis may take a few minutes." if bot_language == "en" else "Преобразование текста в аудио... \nЭто может занять несколько минут.")
        await bot.send_chat_action(chat_id=message.chat.id, action="record_audio")
        text = message.text
        lang = detect(text)
        obj = gTTS(text=text, lang=lang, slow=False)
        file_name = str(uuid.uuid4()) + '.mp3'
        obj.save(file_name)
        with open(file_name, 'rb') as f:
            await bot.send_audio(message.chat.id, f)
        os.remove(file_name)
    except Exception as e:
        await message.reply("An error occurred while processing." if bot_language == "en" else "Произошла ошибка при выполнении.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()
    await state.finish()

class HashCalcState(StatesGroup):
    waiting_for_file = State()

@dp.message_handler(commands=['hash_calculator'])
async def hash_calculator(message: types.Message):
    await message.reply('Select hashing method:' if bot_language == "en" else "Выберите метод хеширования", reply_markup=inlineKeyboardHash)

@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=HashCalcState.waiting_for_file)
async def handle_hash_calculator(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(message.chat.id, "File Processing..." if bot_language == "en" else "Обработка файла")
        document = message.document
        file_path = await bot.download_file_by_id(document.file_id)
        file_hash = await calculate_file_hash(file_path, method_hash)
        await bot.send_message(message.chat.id, f"File hash: {file_hash}")
        await message.reply("Calculating complete." if bot_language == "en" else "Расчет завершен.")
        
    except Exception as e:
        await message.reply("An error occurred while processing." if bot_language == "en" else "Произошла ошибка при выполнении.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()
    await state.finish()

async def calculate_file_hash(file, hash_algorithm):
    hash_obj = hashlib.new(hash_algorithm)
    for chunk in iter(lambda: file.read(4096), b''):
        hash_obj.update(chunk)
    file_hash = hash_obj.hexdigest()
    return file_hash

class searchWikiState(StatesGroup):
    waiting_for_text = State()

@dp.message_handler(commands=['search_wikipedia'])
async def hash_calculator(message: types.Message):
    await message.reply('Select searching language:' if bot_language == "en" else "Выберите язык поиска", reply_markup=inlineKeyboardWiki)


@dp.message_handler(state=searchWikiState.waiting_for_text)
async def hash_calculator(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(message.chat.id, "Searching..." if bot_language == "en" else "Поиск...")
        search_query = message.text
        wiki_wiki = wikipediaapi.Wikipedia(wiki_lang)
        page = wiki_wiki.page(search_query)
        if page.exists():
            await bot.send_message(message.chat.id, page.summary)
            await bot.send_message(message.chat.id, "Searching successfull." if bot_language == "en" else "Поиск успешен.")
        else:
            await bot.send_message(message.chat.id, "Page not found." if bot_language == "en" else "Страница не найдена.")
    except Exception as e:
        await message.reply("An error occurred while processing." if bot_language == "en" else "Произошла ошибка при выполнении.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()
    await state.finish()

@dp.message_handler(commands=['currency'])
async def hash_calculator(message: types.Message):
    await message.reply('Select currency:' if bot_language == "en" else "Выберите валюту.", reply_markup=inlineKeyboardCurrency)

async def show_currency_values(message: types.Message):
    currency_values = await get_currency_values(message)
    if currency_values:
        response = 'Current currency values:\n' if bot_language == "en" else "Текущие значения валют:\n"
        for currency, value in currency_values.items():
            response += f'{currency}: {value}\n'
    else:
        response = 'Failed to get actual currency values.' if bot_language == "en" else "Не удалось получить актуальные значения валюты."
    await bot.send_message(message.chat.id, response)

async def get_currency_values(message: types.Message):
    try:
        url = "https://api.exchangerate-api.com/v4/latest/" + cur_val
        response = requests.get(url)
        data = response.json()
        
        if 'rates' in data:
            return data['rates']
    except Exception as e:
        await message.reply("Error getting currency values." if bot_language == "en" else "Ошибка получения значений валюты.")
        report = open("report.txt", "a+")
        report.write("\n[" + str(datetime.now(timezone.utc)) + "] Server WARNING error: " + str(e))
        report.close()  
    return None

if __name__ == '__main__':
    report = open("report.txt", "a+")
    report.write("\n[" + str(datetime.now(timezone.utc)) + "] SERVER STARTED SUCCESSFULLY" + version)
    report.close()
    while True:
        try:
            executor.start_polling(dp)
        except Exception as e:
            report = open("report.txt", "a+")
            report.write("\n[" + str(datetime.now(timezone.utc)) + "] SERVER CRITICAL ERROR: " + str(e) + version)
            report.close()
