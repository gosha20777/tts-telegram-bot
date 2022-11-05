from huggingsound import SpeechRecognitionModel
import telebot
import os

API_TOKEN = os.environ['BOT_API_TOKEN']

bot = telebot.TeleBot(API_TOKEN)
model = SpeechRecognitionModel(
    "jonatasgrosman/wav2vec2-large-xlsr-53-russian"
)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am TextToSpeechBot.
Give me a file and I'll return the transcription for you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(content_types=['document', 'audio'])
def echo_message(message: telebot.types.Message):
    idx = message.document.file_id
    file_name = message.document.file_name

    if not file_name.endswith('.wav'):
        bot.reply_to(message, "I can only work with .wav files")
        return

    path = os.path.join(
        './storage', f'{idx}_{file_name}'
    )
    file_info = bot.get_file(idx)
    downloaded_file = bot.download_file(file_info.file_path)
    open(path, 'wb').write(downloaded_file)
    bot.reply_to(message, f'Starting transcription for {file_name}')
    transcription = model.transcribe([path])[0].get('transcription')
    bot.reply_to(message, transcription)

bot.infinity_polling()
