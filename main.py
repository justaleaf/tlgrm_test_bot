import telebot
import os
import face_recognition
import subprocess
from mongo import db, fs

token = os.getenv("BUDGET_BOT")
bot = telebot.TeleBot(token)
bot_data = db.bot_data.user_audio


@bot.message_handler(content_types=['voice'])
def audio(message):
    save_dir = "/home/woghan/projects/budget_bot/audio"
    uid = message.from_user.id
    file_id = message.voice.file_id
    name = file_id + ".ogg"
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(save_dir + "/" + name, 'wb') as new_file:
        new_file.write(downloaded_file)
    #oga to wav
    src_filename = save_dir + "/" + name
    dest_filename = save_dir + "/" + file_id + '.wav'
    process = subprocess.run(['ffmpeg', '-i', src_filename, '-ar', '16000', dest_filename])

    with open(dest_filename, 'rb') as new_file:
        bot_data.update_one({"uid": uid}, {"$push": {"audios": fs.put(new_file)}}, True)


@bot.message_handler(content_types=['photo'])
def photo(message):
    save_dir = "/home/woghan/projects/budget_bot/images"
    file_id = message.photo[-1].file_id
    name = file_id + ".jpg"
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    if face_recognition.detectFace(downloaded_file):
        with open(save_dir + "/" + name, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "На картинке есть лицо - сохраним ее с названием {}".format(str(name)))
    else:
        bot.send_message(message.chat.id, "Тут нет лиц, сохранять не буду")


bot.polling()