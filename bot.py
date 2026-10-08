import os
from pyrogram import Client, filters
import yt_dlp

# بيانات البوت الخاص بك
API_ID = 6  # رقم افتراضي عام لـ Telegram API
API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"  # هاش افتراضي عام
BOT_TOKEN = "8997473075:AAG9oNfj8FIzs4Cx3F92tGl2grnW---gKNQ"

app = Client("media_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text(
        "أهلاً بك! أنا بوت تحميل الوسائط والملفات.\n"
        "أرسل لي أي رابط فيديو (من يوتيوب، إنستغرام، تيك توك، وغيرها) وسأقوم بتحميله لك فوراً."
    )

@app.on_message(filters.text & ~filters.command("start"))
def download_media(client, message):
    url = message.text.strip()
    status_msg = message.reply_text("جاري المعالجة والتحميل... ⏳")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'max_filesize': 50 * 1024 * 1024, # حد أقصى 50 ميجابايت للتليجرام
    }
    
    try:
        os.makedirs("downloads", exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        status_msg.edit_text("جاري إرسال الملف... 📤")
        message.reply_video(video=filename)
        status_msg.delete()
        
        # حذف الملف من الخادم بعد الإرسال لتوفير المساحة
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        status_msg.edit_text(f"حدث خطأ أثناء التحميل:\n{str(e)}")

print("Bot is running...")
app.run()
