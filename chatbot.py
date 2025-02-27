import os
import json
import openai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

# Load API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
firebase_project_id = os.getenv("FIREBASE_PROJECT_ID")

# Ensure API keys exist
if not openai.api_key or not telegram_bot_token:
    raise ValueError("Missing API keys. Ensure they are set as environment variables.")

async def process_message(update: Update, context) -> None:
    user_input = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": f"Generate an Android app project for: {user_input}"}]
    )
    app_code = response["choices"][0]["message"]["content"]

    with open("MainActivity.kt", "w") as file:
        file.write(app_code)

    await update.message.reply_text("App code generated and pushed to GitHub.")

    os.system("git add . && git commit -m 'AI generated code' && git push")

async def main():
    application = Application.builder().token(telegram_bot_token).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))
    await application.run_polling()
