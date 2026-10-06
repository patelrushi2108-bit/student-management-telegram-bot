import csv
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


# ============================================================
# CONFIGURATION
# ============================================================

# Paste your NEW BotFather token here
BOT_TOKEN = "8396940574:AAG7CB57vRmhP7hhjPDxbSyBOY6vx-K9Ou0"

# Paste your TEACHER'S Telegram Chat ID here
TEACHER_CHAT_ID = 8555061802

# Student data will be saved in this file
CSV_FILE = "students.csv"


# ============================================================
# REGISTRATION STEPS
# ============================================================

FULL_NAME = 0
BRANCH = 1
ENROLLMENT = 2
STUDY_YEAR = 3
PHONE = 4
GR_NUMBER = 5


# ============================================================
# CREATE CSV FILE
# ============================================================

def create_csv_file():

    if not os.path.exists(CSV_FILE):

        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Full Name",
                "Branch",
                "Enrollment Number",
                "Study Year",
                "Phone Number",
                "GR Number",
                "Telegram Username",
                "Telegram User ID"
            ])


# ============================================================
# START REGISTRATION
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "🎓 CIPET STUDENT REGISTRATION\n\n"
        "Welcome!\n"
        "I will collect your details step by step.\n\n"
        "Please enter your Full Name."
    )

    return FULL_NAME


# ============================================================
# FULL NAME
# ============================================================

async def get_full_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    name = update.message.text.strip()

    if len(name) < 2:

        await update.message.reply_text(
            "Please enter a valid Full Name."
        )

        return FULL_NAME

    context.user_data["full_name"] = name

    await update.message.reply_text(
        "Great! 👍\n\n"
        "Now enter your Branch.\n\n"
        "Example:\n"
        "Computer Engineering"
    )

    return BRANCH


# ============================================================
# BRANCH
# ============================================================

async def get_branch(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    branch = update.message.text.strip()

    if len(branch) < 2:

        await update.message.reply_text(
            "Please enter a valid Branch."
        )

        return BRANCH

    context.user_data["branch"] = branch

    await update.message.reply_text(
        "Now enter your Enrollment Number."
    )

    return ENROLLMENT


# ============================================================
# ENROLLMENT NUMBER
# ============================================================

async def get_enrollment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    enrollment = update.message.text.strip()

    if len(enrollment) < 2:

        await update.message.reply_text(
            "Please enter a valid Enrollment Number."
        )

        return ENROLLMENT

    context.user_data["enrollment"] = enrollment

    await update.message.reply_text(
        "Now enter your Study Year.\n\n"
        "Example:\n"
        "2nd Year"
    )

    return STUDY_YEAR


# ============================================================
# STUDY YEAR
# ============================================================

async def get_study_year(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    study_year = update.message.text.strip()

    if len(study_year) < 1:

        await update.message.reply_text(
            "Please enter your Study Year."
        )

        return STUDY_YEAR

    context.user_data["study_year"] = study_year

    await update.message.reply_text(
        "Now enter your Phone Number.\n\n"
        "Example:\n"
        "9876543210"
    )

    return PHONE


# ============================================================
# PHONE NUMBER
# ============================================================

async def get_phone(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    phone = update.message.text.strip()

    clean_phone = (
        phone
        .replace(" ", "")
        .replace("-", "")
        .replace("+", "")
    )

    if not clean_phone.isdigit():

        await update.message.reply_text(
            "Please enter a valid Phone Number."
        )

        return PHONE

    if len(clean_phone) < 10:

        await update.message.reply_text(
            "Phone Number should contain at least 10 digits."
        )

        return PHONE

    context.user_data["phone"] = phone

    await update.message.reply_text(
        "Finally, enter your GR Number."
    )

    return GR_NUMBER


# ============================================================
# GR NUMBER
# ============================================================

async def get_gr_number(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    gr_number = update.message.text.strip()

    if len(gr_number) < 1:

        await update.message.reply_text(
            "Please enter a valid GR Number."
        )

        return GR_NUMBER

    context.user_data["gr_number"] = gr_number

    # --------------------------------------------------------
    # GET TELEGRAM USER DETAILS
    # --------------------------------------------------------

    user = update.effective_user

    if user is not None:

        telegram_user_id = user.id

        if user.username:

            telegram_username = "@" + user.username

        else:

            telegram_username = "No username"

    else:

        telegram_user_id = "Unknown"
        telegram_username = "Unknown"

    # --------------------------------------------------------
    # GET REGISTRATION DATA
    # --------------------------------------------------------

    full_name = context.user_data["full_name"]
    branch = context.user_data["branch"]
    enrollment = context.user_data["enrollment"]
    study_year = context.user_data["study_year"]
    phone = context.user_data["phone"]

    # --------------------------------------------------------
    # SAVE STUDENT DATA
    # --------------------------------------------------------

    try:

        with open(
            CSV_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                full_name,
                branch,
                enrollment,
                study_year,
                phone,
                gr_number,
                telegram_username,
                telegram_user_id
            ])

        csv_saved = True

    except Exception as error:

        print("CSV ERROR:", error)

        csv_saved = False

    # --------------------------------------------------------
    # CREATE TEACHER MESSAGE
    # --------------------------------------------------------

    teacher_message = (
        "🎓 NEW CIPET STUDENT REGISTRATION\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"

        "👤 Full Name: "
        + full_name
        + "\n"

        "🏫 Branch: "
        + branch
        + "\n"

        "🆔 Enrollment Number: "
        + enrollment
        + "\n"

        "📚 Study Year: "
        + study_year
        + "\n"

        "📱 Phone Number: "
        + phone
        + "\n"

        "🔢 GR Number: "
        + gr_number
        + "\n\n"

        "━━━━━━━━━━━━━━━━━━━━\n"
        "📲 TELEGRAM INFORMATION\n\n"

        "Username: "
        + telegram_username
        + "\n"

        "Telegram User ID: "
        + str(telegram_user_id)
        + "\n\n"

        "━━━━━━━━━━━━━━━━━━━━\n"

        "✅ Student registration completed."
    )

    # --------------------------------------------------------
    # SEND DATA TO TEACHER
    # --------------------------------------------------------

    teacher_notified = False

    try:

        await context.bot.send_message(
            chat_id=TEACHER_CHAT_ID,
            text=teacher_message
        )

        teacher_notified = True

        print("Teacher notification sent successfully.")

    except Exception as error:

        print("TEACHER NOTIFICATION ERROR:")
        print(error)

    # --------------------------------------------------------
    # STUDENT CONFIRMATION
    # --------------------------------------------------------

    if teacher_notified and csv_saved:

        await update.message.reply_text(
            "✅ REGISTRATION COMPLETED!\n\n"
            "Your details have been successfully submitted "
            "to your mentor/teacher.\n\n"
            "Thank you! 🎓"
        )

    elif csv_saved:

        await update.message.reply_text(
            "✅ Your registration has been saved.\n\n"
            "However, the teacher notification could not be sent.\n"
            "Please contact your mentor."
        )

    else:

        await update.message.reply_text(
            "⚠️ There was a problem saving your registration.\n\n"
            "Please try again or contact your mentor."
        )

    # Clear data after registration
    context.user_data.clear()

    return ConversationHandler.END


# ============================================================
# CANCEL REGISTRATION
# ============================================================

async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Registration cancelled.\n\n"
        "You can start again anytime by sending /start."
    )

    return ConversationHandler.END


# ============================================================
# MY ID
# ============================================================

async def myid(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user
    chat_id = update.effective_chat.id

    if user:

        name = user.full_name

        if user.username:

            username = "@" + user.username

        else:

            username = "No username"

    else:

        name = "Unknown"
        username = "Unknown"

    await update.message.reply_text(
        "YOUR TELEGRAM INFORMATION\n\n"
        "Name: "
        + name
        + "\n"

        "Username: "
        + username
        + "\n"

        "Chat ID: "
        + str(chat_id)
        + "\n\n"

        "Save this Chat ID."
    )


# ============================================================
# HELP
# ============================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🎓 CIPET STUDENT REGISTRATION BOT\n\n"
        "/start - Start registration\n"
        "/cancel - Cancel registration\n"
        "/myid - Get Telegram Chat ID\n"
        "/help - Show help"
    )


# ============================================================
# ERROR HANDLER
# ============================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    print()
    print("==============================================")
    print("BOT ERROR")
    print("==============================================")
    print(context.error)
    print()


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():

    print()
    print("==============================================")
    print("     CIPET STUDENT REGISTRATION BOT")
    print("==============================================")
    print()

    # Create CSV file
    create_csv_file()

    # Check Bot Token
    if (
        not BOT_TOKEN
        or BOT_TOKEN == "PASTE_YOUR_NEW_BOT_TOKEN_HERE"
    ):

        print("ERROR:")
        print("Please add your NEW BotFather token")
        print("inside BOT_TOKEN in bot.py")
        print()

        return

    # Check Teacher Chat ID
    if TEACHER_CHAT_ID == 123456789:

        print("WARNING:")
        print("Teacher Chat ID is still set to 123456789.")
        print("Change it to your teacher's actual Chat ID.")
        print()

    # Create Telegram application
    app = Application.builder().token(BOT_TOKEN).build()

    # --------------------------------------------------------
    # REGISTRATION HANDLER
    # --------------------------------------------------------

    registration_handler = ConversationHandler(

        entry_points=[
            CommandHandler(
                "start",
                start
            )
        ],

        states={

            FULL_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_full_name
                )
            ],

            BRANCH: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_branch
                )
            ],

            ENROLLMENT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_enrollment
                )
            ],

            STUDY_YEAR: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_study_year
                )
            ],

            PHONE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_phone
                )
            ],

            GR_NUMBER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_gr_number
                )
            ],
        },

        fallbacks=[
            CommandHandler(
                "cancel",
                cancel
            )
        ],

        allow_reentry=True
    )

    # Add registration handler
    app.add_handler(registration_handler)

    # Add other commands
    app.add_handler(
        CommandHandler(
            "myid",
            myid
        )
    )

    app.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    # Error handler
    app.add_error_handler(error_handler)

    # --------------------------------------------------------
    # START BOT
    # --------------------------------------------------------

    print("BOT STARTED SUCCESSFULLY")
    print("Waiting for student registrations...")
    print()
    print("Bot commands:")
    print("/start")
    print("/cancel")
    print("/myid")
    print("/help")
    print()

    app.run_polling(
        drop_pending_updates=True
    )


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()