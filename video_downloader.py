import yt_dlp
import os

def download_video(url, videos_dir):
    # Создаем папку videos, если она не существует
    if not os.path.exists(videos_dir):
        os.makedirs(videos_dir)

    # Опции для yt-dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'noplaylist': True,
        'socket_timeout': 60,
        'outtmpl': os.path.join(videos_dir, '%(title)s.%(ext)s'),
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4' # Конвертация в mp4
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
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])

        if not formats:
            print("Нет доступных форматов")
            return
        
        # Вывод доступных форматов
        print("Доступные форматы:")
        for i, fmt in enumerate(formats):
            filesize_display = '{:.2f} MB'.format(fmt['filesize'] / (1024 * 1024)) if fmt.get('filesize') is not None else '? MB'
            
            print(f"{i + 1} | {fmt['format']} | {fmt.get('fps', 'Не указано')} FPS | Битрейт: {fmt.get('tbr', 'Не указан')} kbit/s | {fmt.get('ext', '')} | {filesize_display}")

        # Запрос выбора качества
        try:
            choice = int(input("Выберите качество (введите номер): ")) - 1
            selected_format = formats[choice]
        except (IndexError, ValueError):
            print("Неверный выбор. Попробуйте снова.")
            return

        # Обновляем параметры для скачивания
        ydl_opts['format'] = selected_format['format_id']

        # Скачивание видео
        print(f"Загрузка видео в папку {videos_dir}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("Видео успешно загружено!")

if __name__ == '__main__':
    videos_dir = 'videos'
    video_url = input("Введите URL видео: ")
    download_video(video_url, videos_dir)