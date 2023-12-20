
import telebot
import yt_dlp as youtube_dl
import key
import os


bot = telebot.TeleBot(key.api_key)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    youtube_link = message.text

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(youtube_link, download=False)
            mp3_filename = f"{video_info['title']}.mp3"
            print(mp3_filename)

        with youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}], 'outtmpl': video_info['title']}) as ydl:
            ydl.download([youtube_link])

        with open(mp3_filename, 'rb') as mp3_file:
            bot.send_audio(message.chat.id, mp3_file)


        # Delete the MP3 file after sending
        os.remove(mp3_filename)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")


bot.polling()