import yt_dlp
from pathlib import Path

def download_audio(url):
    audio_dir = Path('downloads')
    audio_dir.mkdir(exist_ok=True)
    
    ydl_opts = {
        'noplaylist': True,
        'format': 'bestaudio/best',  # Выбираем лучшее качество аудио
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # Максимальное качество MP3
        }],
        'outtmpl': str(audio_dir / '%(title)s.%(ext)s'),
    }

    try:
        print("Загрузка аудио...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\nАудио успешно загружено!")
        print(f"Файл сохранен в директории: {audio_dir}")
            
    except Exception as e:
        print(f"\nОшибка при загрузке: {str(e)}")

if __name__ == '__main__':
    audio_url = input("Введите URL видео для извлечения аудио: ")
    download_audio(audio_url)