import yt_dlp
from pathlib import Path
import traceback

def download_video(url):
    videos_dir = Path('/home/micky/micky-share/Media/YouTube')
    videos_dir.mkdir(exist_ok=True)

    base_opts = {
        'noplaylist': True,  # Загрузка только одного видео
        'socket_timeout': 120,  # Установить таймаут соединения
        'outtmpl': str(videos_dir / '%(title)s.%(ext)s'),  # Шаблон сохранения файлов
        'proxy': 'socks5://127.0.0.1:10801',  # Прокси-сервер
        'http_chunk_size': 10485760,  # Чанковая загрузка
        'nocheckcertificate': True,  # Игнорировать SSL-сертификаты
        'merge_output_format': 'mkv',  # Формат для объединённых файлов
        'ffmpeg_location': '/usr/bin/ffmpeg',  # Путь к FFmpeg
        'prefer_ffmpeg': True,  # Предпочитать FFmpeg для обработки
        'keepvideo': False,  # Не сохранять исходные файлы
        'retries': 5,  # Количество попыток при неудаче
        'verbose': False,  # Подробный вывод для отладки
        'postprocessors': [],  # Отключить постпроцессинг
    }

    with yt_dlp.YoutubeDL(base_opts) as ydl:
        try:
            # Получение информации о видео
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])

            if not formats:
                print("Нет доступных форматов")
                return

            # Фильтруем форматы
            filtered_formats = [
                f for f in formats
                if f.get('vcodec') != 'none'  # Только видео форматы
                and f.get('ext') == 'webm'  # Только WebM
                and f.get('height', 0) <= 1080  # Не более 1080p
            ]

            if not filtered_formats:
                print("Не найдены подходящие WebM форматы")
                return

            # Сортируем форматы
            filtered_formats.sort(key=lambda x: (x.get('height', 0), x.get('tbr', 0)), reverse=True)

            # Выбираем лучший формат
            selected_format = filtered_formats[0]

            print(f"\nВыбран формат: {selected_format.get('height')}p")

            # Настройка загрузки с выбранным форматом
            download_opts = base_opts.copy()
            format_id = selected_format['format_id']
            download_opts['format'] = f"{format_id}+bestaudio/best"

            print("Начинаем загрузку...")

            # Загрузка видео
            with yt_dlp.YoutubeDL(download_opts) as ydl_download:
                ydl_download.download([url])

            print("\nВидео успешно загружено!")
            print(f"Файл сохранен в директории: {videos_dir}")

        except yt_dlp.utils.DownloadError as de:
            print(f"\nОшибка при загрузке: {str(de)}")
            print("Попробуйте проверить соединение или прокси.")
        except Exception as e:
            print(f"\nНеизвестная ошибка: {str(e)}")
            print("Полное описание ошибки:")
            traceback.print_exc()

if __name__ == '__main__':
    video_url = input("Введите URL видео: ")
    download_video(video_url)

