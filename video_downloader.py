# Загрузчик видео. Работает для ВК, Ютуба, Твича и много чего ещё
# Полный список https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

import yt_dlp

def download_video(url):
    # Опции для yt-dlp
    ydl_opts = {
        'format': 'best',  # Загружаем лучшее доступное качество
        'noplaylist': True,  # Не загружать плейлисты
        'socket_timeout': 60,
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