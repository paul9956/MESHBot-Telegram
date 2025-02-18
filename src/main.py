from json import load
from datetime import datetime
from time import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import core.searching_answers as core

with open("src/package/client.json", "r") as telegram_data:
    data = load(telegram_data)
bot = Bot(token=data["telegram_token"])
client = Dispatcher(bot)
admin_id = []   #here put id admins
id_users = []


def analytics(message: types.Message):
    with open('src/analytics.txt', '+r') as user_id:
        if str(message.from_user.id) not in user_id.read():
            user_id.write(f'{message.from_user.id, message.from_user.username}\n')


def post(message: types.Message):
    if 'all' not in message.text:
        post_text = message.text.replace('post ', '').split(' ')
        user_id = post_text[0]
        final_text = ''
        for text in post_text:
            final_text += f'{text} '
        return user_id, final_text.replace(user_id, '')


@client.message_handler(commands=["start", "help", "хелп", "помощь", "гайд"])
async def manual(msg: types.Message):
    with open("src/package/client_lock.json", "r") as file:
        sys = load(file)
    await msg.answer(f"""👋Привет, {msg.from_user.first_name}.\n
❗Для начала работы, отправь мне ссылку на тест и я постараюсь найти ответы.\n📝Пример ссылки: {sys['example']}\n
⚠️Если возникла какая-либо проблема, ошибка, баг обратитесь в чат поддержки👨🏼‍🔧: {sys['help_place']}.
Там Вам помогут с сложившейся ситуацией.🎯\n
💯Также можешь меня оценить,\n просто написав мне оценку👇\n
🤖Версия бота: 3️⃣.0️⃣
🪄Ссылка на бота: {sys['link']}
📌ВК создателя: {sys['vk']}""")
    analytics(msg)


@client.message_handler(commands=['admin', 'analytics'])
async def admin(msg: types.Message):
    with open("src/analytics.txt", "r") as analytic:
        if msg.from_user.id in admin_id:
            counter = 0
            for number, id_user in enumerate(analytic.readlines()):
                await msg.answer(f'{number + 1}. User: {id_user}')
                counter += 1
            await msg.answer(f'🙈Всего пользователей: {counter}')
        else:
            await msg.answer("⚠️Для начала, отправь ссылку на тест, и я попробую его решить.🤡")


@client.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    if msg.animation or msg.audio or msg.contact or msg.dice or msg.document or msg.location\
            or msg.photo or msg.poll or msg.sticker or msg.sticker or msg.venue or msg.video\
            or msg.video_note or msg.voice:
        await msg.answer("⚠️Для начала, отправь ссылку на тест, и я попробую его решить.🛸")
    if msg.text.startswith("https://uchebnik.mos.ru"):
        try:
            start_time = time()
            await msg.answer("👽Начал решать...")
            answers = core.get_answers(link=msg.text)
            for task_number, task in enumerate(answers):
                await msg.answer(f"✏Вопрос №{task_number + 1}: {task[0]}\n\n✅Ответ: {task[1]}")
            await msg.answer(f"⏳Решено за {'%s секунд' % round((time() - start_time), 1)}")
        except:
            await msg.answer('⚠️Хм странно, но я ничего не нашел. Проверь правильность ссылки или нажми 👉/help👈')

    elif 'post all' in msg.text and msg.from_user.id == admin_id[0]:
        post_text = msg.text.replace('post ', '').replace('all ', '')
        for user in id_users:
            await bot.send_message(user, post_text)
    elif 'post' in msg.text and msg.from_user.id in admin_id:
        user_id, final_text = post(msg)
        await bot.send_message(user_id, final_text)

    elif msg.text.isdigit():
        await msg.answer('Спасибо за оценку😊')

    else:
        await msg.answer("⚠️Для начала, отправь ссылку на тест, и я попробую его решить.🛸")

    info = f'Text: {msg.text}\nUser: {msg.from_user.get_user_profile_photos}'
    await bot.send_message(admin_id[0], info)
    analytics(msg)


@client.message_handler(content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker',
                   'venue', 'video', 'video_note', 'voice'])
async def get_text_messages(msg: types.Message):
    if msg.animation or msg.audio or msg.contact or msg.dice or msg.document or msg.location\
            or msg.photo or msg.poll or msg.sticker or msg.sticker or msg.venue or msg.video\
            or msg.video_note or msg.voice:
        await msg.answer("⚠️Для начала, отправь ссылку на тест, и я попробую его решить.🛸")


if __name__ == "__main__":
    print(f"Connected at {datetime.today().strftime('%H:%M, %d-%m-%Y')}")
    executor.start_polling(client)
