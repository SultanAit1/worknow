from aiogram.types import InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from config import bot, dp
from keyboards.client_kb import start_markup, main_markup, url_markup, profil_markup, func_markup
import sqlite3
import time
from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime
from config import ADMIN_ID

from aiogram.types import ParseMode, ContentType


# чтобы сразу не отправлять данные
class Form(StatesGroup):
    date_type = State()
    message = State()


conn = sqlite3.connect('users.db')
cursor = conn.cursor()

conn.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, join_date TEXT)''')


# эту команду я добавил чтобы посмотреть все записи пользователей в базе данных, если это нужно можно расскоментировать это и строчку 404
@dp.message_handler(commands=['full_follow'])
async def full_follow(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        cursor = conn.execute("SELECT * FROM users")
        users = cursor.fetchall()

    # Формирование сообщения с информацией о пользователях
        response = "Список пользователей:\n\n"
        for user in users:
            response += f"ID: {user[0]}, Дата присоединения: {user[1]}\n"

        cursor.close()
        await message.answer(response, parse_mode=ParseMode.HTML)
    else:
        return




@dp.message_handler(commands='follow')
async def follow(message: types.Message):
    if message.from_user.id == ADMIN_ID:

    # Получение общего количества пользователей
        cursor = conn.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

    # Получение текущего месяца и года
        now = datetime.now()
        current_month = now.month
        current_year = now.year

    # Получение количества пользователей, которые зашли в текущем месяце
        cursor = conn.execute(
            f"SELECT COUNT(*) FROM users WHERE strftime('%m', join_date)='{current_month:02}' AND strftime('%Y', join_date)='{current_year}'")
        users_this_month = cursor.fetchone()[0]
        cursor.close()
    # Формирование сообщения с информацией о пользователях
        response = f"Пользователей всего: {total_users}\nПользователей за этот месяц: {users_this_month}"



        await message.answer(response, parse_mode=types.ParseMode.HTML)
    else:
        return


# @dp.message_handler(content_types=['voice'])
async def handle_voice(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    voice_id = message.voice.file_id
    try:
        # Отправляем фото всем подписчикам
        cursor.execute("SELECT id FROM users")
        rows = cursor.fetchall()
        i = 0
        for row in rows:
            user_id = row[0]
            try:
                await bot.send_voice(chat_id=user_id, voice=voice_id)
                i += 1
                time.sleep(2)
            except:
                print(f"пользователь заблокировал бота: {user_id}")
        await message.answer(f" аудио успешно отправлено ({i} подписчикам).")
    except Exception as e:
        print(f"Ошибка при отправке видео: {e}")


# noinspection SqlResolve
# @dp.message_handler(content_types=['video_note'])
async def handle_note(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    video_note_id = message.video_note.file_id
    try:
        # Отправляем фото всем подписчикам
        i = 0
        cursor.execute("SELECT id FROM users")
        rows = cursor.fetchall()
        for row in rows:
            user_id = row[0]
            try:
                await bot.send_video_note(chat_id=user_id, video_note=video_note_id)
                i += 1
                time.sleep(2)
            except:
                print(f"пользователь заблокировал бота: {user_id}")
        await message.answer(f"Видео успешно отправлено ({i} подписчикам).")
    except Exception as e:
        print(f"Ошибка при отправке видео: {e}")


class SpamVideoStates(StatesGroup):
    wait_for_confirmation = State()


# noinspection SqlResolve
# @dp.message_handler(content_types=['video'])
async def handle_video(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    # Получаем идентификатор фото
    video_id = message.video.file_id
    try:
        # Отправляем фото всем подписчикам
        cursor.execute("SELECT id FROM users")
        rows = cursor.fetchall()
        i = 0
        for row in rows:
            user_id = row[0]
            try:
                await bot.send_video(chat_id=user_id, video=video_id, caption=message.caption)
                i += 1
                time.sleep(2)
            except:
                print(f"пользователь заблокировал бота: {user_id}")
        await message.answer(f"Видео успешно отправлено ({i} подписчикам).")
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")


# noinspection SqlResolve
# @dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    # Получаем идентификатор фото
    photo_id = message.photo[-1].file_id
    try:
        # Отправляем фото всем подписчикам
        cursor.execute("SELECT id FROM users")
        rows = cursor.fetchall()
        i = 0
        for row in rows:
            user_id = row[0]
            try:
                await bot.send_photo(chat_id=user_id, photo=photo_id, caption=message.caption)
                i += 1
                time.sleep(2)
            except:
                print(f"пользователь заблокировал бота: {user_id}")
        await message.answer(f"Фото успешно отправлено ({i} подписчикам).")
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")


async def handle_text(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        # Отправляем текст всем подписчикам
        cursor.execute("SELECT id FROM users")
        rows = cursor.fetchall()
        i = 0
        for row in rows:
            user_id = row[0]
            try:
                # await bot.send_photo(chat_id=user_id, text = ,caption=message.caption[6:] )
                await bot.send_message(chat_id=user_id, text=message.text)
                i += 1
                time.sleep(2)
            except:
                print(f"пользователь заблокировал бота: {user_id}")
        await message.answer(f"Текст успешно отправлен ({i} подписчикам).")
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")


@dp.message_handler(commands=['start'], state='*')
async def start_handler(message: types.Message, state: FSMContext):
    # cursor.execute("INSERT OR REPLACE INTO users (user_id) VALUES (?)", (user_id,))
    user: types.User = message.from_user
    join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # проверить есть ли в базе данных юзер
    if not cursor.execute("SELECT id FROM users WHERE id=?", (user.id,)).fetchone():
        cursor.execute("INSERT INTO users (id, join_date) VALUES (?, ?)", (user.id, join_date))
        conn.commit()
        # отправляем уведомление администратору
        await bot.send_message(ADMIN_ID,
                               f"Пользователь {message.from_user.id} (@{message.from_user.username}) начал использовать бота")
    if message.from_user.id != ADMIN_ID:
        await bot.send_message(chat_id=message.from_user.id, text='https://youtu.be/UCF1oebyXMQ\n')
        await bot.send_message(chat_id=message.from_user.id,
                               text=
                               "\n*😍Бул жасалма интеллект элементтери бар "
                                                                  'автоматташтырылган системанын негизги менюсу\n '
                                                                  '\n🌏Жана бул жерден сиз ДҮЙНӨЛҮК '
                                                                  'аталыштагы компания ERSAG  '
                                                                  'жөнүндө БААРЫН биле аласыз -!\n'
                                                                  '\nМен дароо жетекчимдин байланыштарын калтырам\n'
                                                                  '\n@janyl_ersag\n '
                                                                  '\nэгер кандайдыр бир суроолоруңуз болсо, сиз '
                                                                  'ар дайым байланыша аласыз\n'
                                    
                                                                  '\n📍Сиз аны менен ар дайым байланышып,'
                                                                  ', бардык суроолорго жооп ала аласыз\n  '
                                                                  
                                                
                                                                  '\n💡Эми жөн гана баскычтарды колдонуңуз,  '
                                                                  'сизди эмне кызыктырса, мен баарын айтып берейин*\n '
                                                                  '\n⬇️⬇️⬇️\n'
                               ,
                               reply_markup=start_markup, parse_mode='Markdown')

    else:
        await bot.send_message(chat_id=message.from_user.id, text='https://youtu.be/UCF1oebyXMQ\n')
        await bot.send_message(chat_id=message.from_user.id, text=
        "\n*😍Бул жасалма интеллект элементтери бар "
        'автоматташтырылган системанын негизги менюсу\n '
        '\n🌏Жана бул жерден сиз ДҮЙНӨЛҮК '
        'аталыштагы компания ERSAG  '
        'жөнүндө БААРЫН биле аласыз -!\n'
        '\nМен дароо жетекчимдин байланыштарын калтырам\n '
        '\n@janyl_ersag\n '
        '\nэгер кандайдыр бир суроолоруңуз болсо, сиз менен '
        'ар дайым байланыша аласыз\n'

        '\n📍Сиз аны менен ар дайым байланышып,'
        ', бардык суроолорго жооп ала аласыз\n  '


        '\n💡Эми жөн гана баскычтарды колдонуңуз,  '
        'сизди эмне кызыктырса, мен баарын айтып берейин*\n '
        '\n⬇️⬇️⬇️\n'
                               , reply_markup=profil_markup, parse_mode='Markdown')
        if message.from_user.id == ADMIN_ID:
            await bot.send_message(chat_id=message.from_user.id, text='Доступные команды:\n'
                                                                  '*\n/start - начать использовать бота\n'
                                                                  '\n/full_follow - данные пользователей\n'
                                                                  '\n/follow - количество пользоваталей\n'
                                                                  '\nАвторассылка - рассылка сообщения*\n'
                                                                      , reply_markup=func_markup, parse_mode='Markdown')

        else:
            return


@dp.callback_query_handler(text="one", state='*')
async def one(callback: CallbackQuery):
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text='*♻Бүгүнкү күндө дүйнө жүзү боюнча миңдеген '
        'адамдар өздөрүнүн ден соолугуна жана '
        'айлана-чөйрөгө кам көрүшөт,'
        'ошондуктан алар 🔝ЭКО продукциясын тандап алышты! \n'
        '\n❗20 жыл Эрсаг ийгиликтүү иштеп келет.\n'
        '\nДенизли шаарында негизделген жана Сапиндус жана  '
        'башка өсүмдүктөрдүн экстрактыларынын негизинде  '
        'табигый продукцияларды чыгарат\n '
        ''
        '\n🔔Продукциянын өндүрүш базалары Түркияда  '
        'жайгашкан жана 9 заводду камтыйт\n'
        '\n🔊Ар бири белгилүү бир продукцияларды:\n'
        'тазалоочу каражаттар, жуучу каражаттар, жеке гигиеналык каражаттар'
        'муздак пресстелген майлар жана косметикалык майлар, парфюмерияларды чыгарат.\n  '
        ''
        '\n🌿Эрсагдын бардык продукциялары органикалык, '
        'курамында химиялык жана синтетикалык '
        'кошулмалар жана кошумчалар, өсүмдүк майлары, '
        'жыпар жыттуу заттар, парабендер, лаурилсульфаттар, фосфаттар, фтор жок.\n'
        '\n💯Компания 43 эл аралык продукцияны алган. Aнын продукциясына сертификаттар!\n'
        'HALAL , ECO CERT, ISO, GMP, OHRAS, BIO, ECO ж.б.*', reply_markup=main_markup, parse_mode='Markdown')


@dp.callback_query_handler(text="two", state='*')
async def two(callback: CallbackQuery):
    two = InlineKeyboardButton('two', callback_data='two')
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text="*📌ERSAG маркетинг планы - жана сиз үчүн дароо көптөгөн 'жакшылыктар': \n"
                                     "\n✅1. Компаниянын сайтында бекер катталуу жана"
                                     "биринчи заказдан 20% арзандатуу.  Ар бир буйрутма  "
                                     "менен сиз заказдын суммасына белек аласыз.\n"
                                     "\n✅2. Мансаптык арзандатуу өнөктөштүн баасына  "
                                     "кошулат, мансап канчалык жогору болсо, заказ "
                                     "боюнча жеке арзандатуу ошончолук чоң болот.  \n "
                                     "\n✅3. Туура карьера, сиз эч качан статустан ылдый "
                                     "түшпөйсүз. Бир жылда заказ кылсаңыз да.  \n"
                                     "\n✅4 Ай сайынгы активдүүлүк: же карьерасына "
                                     "жараша жеке көлөм же жаңы адамды биринчи сапка 2 "
                                     "упай тартиби менен кошуу.\n "
                                     "\n✅5. Эки айдын ичинде карьерасын жабуу мүмкүнчүлүгү. \n"
                                     "\n✅6. Упайларды мурунку айдан азыркыга которуу.  \n"
                                     "\n✅7. Айдын каалаган күнүндө карьера жана бир нече  "
                                     "карьера айына 10%дан 33%ке чейин жабуу мүмкүнчүлүгү. \n "
                                     "\n✅8. Бардык түзүм жана тереңдик боюнча төлөмдөр \n"
                                     "\n✅9. Лидерлик бонус  \n "
                                     "\n✅10. Маркетинг лидерлерин кескенге болбойт \n "
                                     "\n✅11. Картага ай сайын расмий бонустук төлөмдөр \n "
                                     "\n✅12. Эл аралык бизнес   \n"
                                     "\n✅13. Туулган кунго заказ бергенде компания кошумча белек берет\n* ",
                                reply_markup=main_markup,parse_mode='Markdown')


@dp.callback_query_handler(text="three", state='*')
async def three(callback: CallbackQuery):
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text="*🔋Компанияда товарлардын ассортименти абдан чоң, \n"
                                                                                                              "сиздерге ынгайлуу болушу \nүчүн мен бир нече\n"
                                                                                                              "каталогдорду тиркеп койдум,\n"
                                                                                                              "аларды карап көрө аласыздар.\n  "
                                                                                                              "\nЭгерде сиз жашаган өлкөңүз үчүн каталог керек  "
                                                                                                              "болсо, менин жетекчиме жазыныз\n"
                                                                                                              "\n✳️✳️✳️  "
                                                                                                              "\n@janyl_ersag\n"
                                                                                                              "\nбул маселе боюнча сизге жардам берет!* ",



                                reply_markup=url_markup,parse_mode='Markdown')


@dp.callback_query_handler(text="last", state='*')
async def last(message: types.Message, ):
    last = InlineKeyboardButton('last', callback_data='last')
    await bot.send_message(chat_id=message.from_user.id, text="Хочу такого бота себе♻️")


@dp.callback_query_handler(text='four', state='*')
async def four(callback: CallbackQuery):
    four = InlineKeyboardButton('four', callback_data='four')
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text="*🔔Биздин коомдогу промоушн системасы "
                                                                                                               "уникалдуу жана ал өзүнө төмөнкүлөрдү камтыйт:  \n "
                                                                                                 "\n✅ Кадамдык окутуу жана ар бир өнөктөштү колдоо, натыйжага алып келүү!  \n  "
                                                                                                 "\n✅ Эффективдүү системаларды, анын ичинде мен сыяктуу автоматташтырылган системаларды колдонуу\n "
                                                                                                 "\n✅ Биздин ар бир өнөктөшүбүздө ушундай жардамчы бар жана сизге да жеткиликтүү болот!  \n "
                                                                                                 "\n✅ Жумуш үчүн даяр алгоритмдер, диалог скрипттери, эффективдүү инструменттер\n "
                                                                                                 "\n🤑 Онлайн режиминде да ишти айкалыштыруу - каалаган адамга ылайыктуу!  \n"
                                                                                                 "\n😎 Баарыбыз бир күчтүү команда болуп баралы!  Ар бир адам үчүн - бул жакшы  перспективалар жана мүмкүнчүлүктөр! \n  "
                                                                                                 "\n⬇️  Көбүрөөк маалымат алуу үчүн негизги меню баскычын басыңыз!* ",
                                reply_markup=main_markup,parse_mode='Markdown' )


@dp.callback_query_handler(text='five', state='*')
async def five(callback: CallbackQuery):
    five = InlineKeyboardButton('five', callback_data='five')
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text="*😃Компаниянын өнөктөшү🤝 \nболуу үчүн менин жетекчиме \nжазыңыз.\nБул жерде анын байланыштары: "
                                                                                                               "\n✳️✳️✳️     \n"
                                                                                    
                                                                                                 "\n@janyl_ersag\n"
                                                                                                 "\nАл сизге туура катталып, компанияда сабаттуу баштоого жардам берет!\n"
                                                                                                 "\nЭгерде мен сизге дагы бир нерсе менен жардам бере алсам , "
                                                                                                 "анда негизги менюга  өтүңүз.  -  🤝\n"
                                                                                                 ""
                                                                                                 "\n💞Мен толугу менен сиздин кызматыңыздамын!*" , reply_markup=main_markup, parse_mode='Markdown')


@dp.callback_query_handler(text="exit_1", state='*')
async def exit_1(callback: CallbackQuery):
    exit_1 = InlineKeyboardButton('exit_1', callback_data="exit_1")
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=

    "\n*😍Бул жасалма интеллект элементтери бар "
    'автоматташтырылган системанын негизги менюсу\n '
    '\n🌏Жана бул жерден сиз ДҮЙНӨЛҮК '
    'аталыштагы компания ERSAG  '
    'жөнүндө БААРЫН биле аласыз -!\n'
    '\nМен дароо жетекчимдин байланыштарын калтырам\n'
    '\n@janyl_ersag\n '
    '\nэгер кандайдыр бир суроолоруңуз болсо, сиз '
    'ар дайым байланыша аласыз\n'

    '\n📍Сиз аны менен ар дайым байланышып,'
    ', бардык суроолорго жооп ала аласыз\n  '


    '\n💡Эми жөн гана баскычтарды колдонуңуз,  '
    'сизди эмне кызыктырса, мен баарын айтып берейин*\n '
    '\n⬇️⬇️⬇️\n',
                                reply_markup=start_markup, parse_mode='Markdown')






@dp.callback_query_handler(text="comand")
async def comand(callback: CallbackQuery, state: FSMContext):
    comand = InlineKeyboardButton('comand', callback_data='comand')
    await state.set_state(Form.date_type)
    await bot.send_message(chat_id=callback.message.chat.id, text="Введите сообщение которое хотите отправить.", )


# content_types=[ContentType.PHOTO, ContentType.VOICE, ContentType.VIDEO, ContentType.VIDEO_NOTE]
@dp.message_handler(state=Form.date_type, content_types=['any'])
async def main_handler(message: types.Message, state: FSMContext):
    if await state.get_state() == None:
        return
    if message.from_user.id != ADMIN_ID:
        # return ничего не возращает, это выход из функции чтобы программа не шла дальше при плохом условии
        return
    await state.set_state(Form.message)
    async with state.proxy() as data:
        data['message'] = message

    await message.reply("Вы действительно хотите отправить данный пост?",
                        reply_markup=InlineKeyboardMarkup(row_width=2).add(
                            InlineKeyboardButton('Принять', callback_data="yes")
                        ).add(InlineKeyboardButton('Отмена', callback_data="no")))


@dp.callback_query_handler(text="yes", state=Form.message)
async def yes_send(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        message = data.get('message')
    await callback.message.delete()
    await bot.send_message(chat_id=ADMIN_ID, text="начинаем отправку...")
    # лесенка, проверяюзий
    if message.content_type == ContentType.TEXT:
        await handle_text(message)
    elif message.content_type == ContentType.PHOTO:
        await handle_photo(message)
    elif message.content_type == ContentType.VOICE:
        await handle_voice(message)
    elif message.content_type == ContentType.VIDEO:
        await handle_video(message)
    elif message.content_type == ContentType.VIDEO_NOTE:
        await handle_note(message)
    else:
        await bot.send_message(chat_id=ADMIN_ID, text="Отправка недоступна для файлов такого типа")
    await state.finish()


@dp.callback_query_handler(text="no", state=Form.message)
async def no_send(callback: CallbackQuery, state: FSMContext):
    await callback.message.reply("Отменяем...")
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(full_follow, commands=['full_follow'])
    dp.register_message_handler(follow, commands='follow')
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(main_handler)
    dp.callback_query_handler(four, text='four')
    dp.callback_query_handler(five, text='five')
    dp.callback_query_handler(one, text='one')
    dp.callback_query_handler(two, text='two')
    dp.callback_query_handler(three, text='three')
    dp.callback_query_handler(last, text='last')
    dp.callback_query_handler(exit_1, text='exit_1')
    dp.callback_query_handler(comand, text='comand')
    dp.callback_query_handler(yes_send, text='yes')
    dp.callback_query_handler(no_send, text='no')






