# BETA # Загрузчик для плейлистов

import yt_dlp
import os

def download_playlist(playlist_url, videos_dir):
    # Создаем папку для видео, если она не существует
    if not os.path.exists(videos_dir):
        os.makedirs(videos_dir)

    # Опции для yt-dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'noplaylist': False,
        'socket_timeout': 60,
        'outtmpl': os.path.join(videos_dir, '%(playlist)s/%(title)s.%(ext)s'),
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'  # Конвертация в mp4
            },
            {
                'key': 'FFmpegMetadata',
            },
            {
                'key': 'FFmpegFixupM4a'
            }
        ]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Получаем информацию о плейлисте
        playlist_info = ydl.extract_info(playlist_url, download=False)

        # Проверяем, содержит ли URL плейлист
        if 'entries' not in playlist_info:
            print("Указанный URL не является плейлистом.")
            return
        
        print(f"Начинается загрузка плейлиста: {playlist_info.get('title', 'Без названия')}")

        # Проходим по каждому видео в плейлисте
        for video in playlist_info['entries']:
            # Получаем URL видео
            video_url = video['webpage_url']
            print(f"Загрузка видео: {video.get('title', 'Без названия')}")

            # Обновляем параметры для загрузки конкретного видео
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'
            
            # Скачиваем видео
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        
        print("Все видео из плейлиста успешно загружены!")

if __name__ == '__main__':
    videos_dir = 'videos'
    playlist_url = input("Введите URL плейлиста: ")
    download_playlist(playlist_url, videos_dir)
