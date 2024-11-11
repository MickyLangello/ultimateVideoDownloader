import yt_dlp
from google.colab import drive
from google.colab import files

# Монтируем Google Drive
drive.mount('/content/drive')

def download_video(url):
    # Опции для yt-dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'noplaylist': True,
        'socket_timeout': 60,
        'outtmpl': '/content/drive/MyDrive/video_downloader/%(title)s.%(ext)s'
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

            print(f"{i + 1} | {fmt['format']} | {fmt.get('fps', 'Не указано')} FPS | Битрейт: {fmt.get('tbr', 'Не указан')} kbit/s | {fmt.get('ext', 'Не указано')} | {filesize_display}")

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
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("Видео успешно загружено!")

if __name__ == '__main__':
    video_url = input("Введите URL видео: ")
    download_video(video_url)