import os
import csv
from datetime import datetime
from telegram import (
    Update, InputMediaPhoto, KeyboardButton,
    ReplyKeyboardMarkup, InputFile
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from dotenv import load_dotenv

# === Загрузка переменных окружения из .env ===
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL_NAME")
TICKET_LINK = os.getenv("TICKET_LINK")
CSV_FILE = os.getenv("CSV_FILE")
IMAGES = [os.getenv("IMAGE_1"), os.getenv("IMAGE_2")]

# === Команда /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # 1. Приветственное сообщение
    await context.bot.send_message(chat_id=chat_id, text=(
        "🛰 Привет, ты в системе.\n\n"
        "🛠 Это официальный бот регистрации на momentum COLLAPSE — следующий рейв нашего объединения.\n\n"
        "🌫 Москва, 4 июля, клуб \"Невротик\", 21:00 - 05:30, 18+"
    ))

    # 2. Афиши
    media = [
        InputMediaPhoto(open(IMAGES[0], "rb"), caption=(
            "🔻 21:00-22:00 — бесплатный вход по регистрации\n"
            "🔺 22:00-05:30 — вход по билетам"
        )),
        InputMediaPhoto(open(IMAGES[1], "rb")),
    ]
    await context.bot.send_media_group(chat_id=chat_id, media=media)

    # 3. Условие регистрации
    await context.bot.send_message(chat_id=chat_id, text=(
        "Первый час — для своих. Просто зарегистрируйся, это займёт меньше минуты.\n\n"
        "📡 Регистрация происходит прямо здесь.\n"
        "🚧 Условие — подписка на наш канал (бот проверит сам).\n\n"
        f"А если хочешь ворваться позже — вот билеты: {TICKET_LINK}"
    ))

    # 4. Кнопка "Проверить подписку" внизу
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("🔴 Проверить подписку")]],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text="👇 Нажми кнопку ниже, чтобы пройти регистрацию:",
        reply_markup=keyboard
    )


# # === Проверка подписки и регистрация ===
# async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     chat_id = update.effective_chat.id

#     try:
#         member = await context.bot.get_chat_member(CHANNEL, user.id)
#         if member.status in ["creator", "administrator", "member", "restricted"]:
#             username = user.username or f"{user.first_name}_{user.id}"
#             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#             file_exists = os.path.isfile(CSV_FILE)
#             with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
#                 writer = csv.writer(f)
#                 if not file_exists:
#                     writer.writerow(["username", "datetime"])
#                 writer.writerow([username, timestamp])

#             await context.bot.send_message(chat_id=chat_id, text=(
#                 "✅ Готово. Ты в списке.\n\n"
#                 "Ждем тебя 4го июля на нашем рейве!\n\n"
#                 "📅 4 июля, 21:00 - 05:30\n"
#                 "🕘 Вход по регистрации с 21:00 до 22:00\n"
#                 "📍 Клуб \"Невротик\"\n\n"
#                 "🚧 Обязательно будь подписан(а) на канал — это проверят на входе.\n"
#                 "📡 Просто покажи это сообщение о регистрации на входе — тебя пустят\n"
#                 "🪪 Не забудь паспорт! Мероприятие 18+\n\n"
#                 "Если передумаешь — не забудь взять билет: https://moscow.qtickets.events/169144-momentum-collapse"
#             ))
#             await context.bot.send_message(chat_id=chat_id, text=(
#                 "<b>Если ты не один — веди за собой.</b>\n\n"
#                 "Ссылка на меня: t.me/mmntum_bot\n\n"
#                 "Или просто скинь стикер — пусть тоже пройдут этот квест."
#             ), parse_mode="HTML")

#             # 3. Стикер
#             await context.bot.send_sticker(chat_id=chat_id, sticker="CAACAgIAAxkBAAM_aDmdOtZULUqzoAfZfUSovfgmFFcAAo5pAAK9aahJgo-IKrWMgQo2BA")
#         else:
#             raise Exception("Not subscribed")
#     except Exception:
#         await context.bot.send_message(chat_id=chat_id, text=(
#             "🚧 Чтобы продолжить регистрацию, подпишись на наш канал.\n\n"
#             f"🔗 https://t.me/{CHANNEL[1:]}\n\n"
#             f"🎟 Или можешь взять билет: {TICKET_LINK}"
#         ))


# === Проверка подписки и регистрация ===
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "Привет, регистрация закрылась сегодня в 19:00 :/\n\n"
            "Но ты все еще можешь купить билет - https://moscow.qtickets.events/169144-momentum-collapse\n\n"
            "Мероприятие начинается в 21:00 и продлится до 05:30, мы ждем тебя\n\n"
            "Наш тг канал со всей информацией - @mmntum"
        )
    )
    # === Команда /export — только для @x0_0Xd ===
async def export_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username == "x0_0Xd":
        if os.path.exists(CSV_FILE):
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=InputFile(CSV_FILE),
                filename=CSV_FILE,
                caption="📄 Вот текущий список зарегистрированных"
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ Файл ещё не создан. Никто не зарегистрировался."
            )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🚫 У тебя нет доступа к этой команде."
        )



# === Точка входа ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🔴 Проверить подписку$"), check_subscription))
    app.add_handler(CommandHandler("export", export_csv))


    app.run_polling()

if __name__ == "__main__":
    main()
