import yt_dlp
from pathlib import Path

def download_playlist_audio(url):
    base_dir = Path('downloads')
    base_dir.mkdir(exist_ok=True)
    
    # Базовые настройки для получения информации о плейлисте
    info_opts = {
        'noplaylist': False,
        'extract_flat': True,  # Только получаем информацию о плейлисте
    }

    try:
        # Сначала получаем информацию о плейлисте
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False)
            
            if 'entries' not in playlist_info:
                print("Указанный URL не является плейлистом.")
                return
            
            # Создаем папку для плейлиста
            playlist_name = playlist_info.get('title', 'Unnamed_Playlist').replace('/', '_')
            playlist_dir = base_dir / playlist_name
            playlist_dir.mkdir(exist_ok=True)
            
            print(f"\nНазвание плейлиста: {playlist_name}")
            print(f"Количество треков: {len(playlist_info['entries'])}\n")
            
            # Настройки для загрузки аудио
            ydl_opts = {
                'noplaylist': True,  # Скачиваем по одному треку
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'outtmpl': str(playlist_dir / '%(title)s.%(ext)s'),
            }
            
            # Загружаем каждый трек из плейлиста
            for i, entry in enumerate(playlist_info['entries'], 1):
                if entry is None:
                    print(f"Трек #{i}: Пропущен (не удалось получить информацию)")
                    continue
                
                try:
                    video_url = entry['url']
                    print(f"Загрузка трека #{i}: {entry.get('title', 'Без названия')}")
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])
                        
                except Exception as e:
                    print(f"Ошибка при загрузке трека #{i}: {str(e)}")
                    continue
            
            print(f"\nЗагрузка плейлиста завершена!")
            print(f"Файлы сохранены в директории: {playlist_dir}")
            
    except Exception as e:
        print(f"\nОшибка при загрузке плейлиста: {str(e)}")

if __name__ == '__main__':
    playlist_url = input("Введите URL плейлиста для извлечения аудио: ")
    download_playlist_audio(playlist_url)