import yt_dlp
from pathlib import Path

def download_playlist(url):
    videos_dir = Path('videos')
    videos_dir.mkdir(exist_ok=True)
    
    base_opts = {
        'noplaylist': False,  # Разрешаем загрузку плейлистов
        'socket_timeout': 60,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }, {
            'key': 'FFmpegMetadata',
        }, {
            'key': 'FFmpegFixupM4a'
        }],
        'ffmpeg_args': [
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-preset', 'medium',
            '-crf', '23',
            '-movflags', '+faststart',
        ]
    }

    with yt_dlp.YoutubeDL(base_opts) as ydl:
        try:
            # Получаем информацию о плейлисте
            playlist_info = ydl.extract_info(url, download=False)
            
            # Проверяем, содержит ли URL плейлист
            if 'entries' not in playlist_info:
                print("Указанный URL не является плейлистом.")
                return
            
            # Создаем директорию для плейлиста
            playlist_name = playlist_info.get('title', 'Unnamed_Playlist').replace('/', '_')
            playlist_dir = videos_dir / playlist_name
            playlist_dir.mkdir(exist_ok=True)
            
            print(f"\nНазвание плейлиста: {playlist_name}")
            print(f"Количество видео: {len(playlist_info['entries'])}")

            # Получаем список всех доступных форматов из первого видео
            first_video = next((v for v in playlist_info['entries'] if v is not None), None)
            if not first_video:
                print("Не удалось получить информацию о форматах видео.")
                return

            formats = first_video.get('formats', [])
            
            if not formats:
                print("Нет доступных форматов")
                return

            # Фильтруем форматы, оставляя видео форматы
            filtered_formats = []
            for f in formats:
                if f.get('vcodec') != 'none':
                    f['height'] = f.get('height', 0)
                    filtered_formats.append(f)

            # Сортируем форматы по разрешению
            filtered_formats.sort(key=lambda x: (x.get('height', 0), x.get('tbr', 0)))

            print("\nДоступные форматы:")
            for i, fmt in enumerate(filtered_formats):
                filesize = fmt.get('filesize')
                if filesize is None:
                    filesize = fmt.get('filesize_approx', 0)
                
                filesize_display = '{:.2f}'.format(filesize / (1024 * 1024)) if filesize else '?'
                
                fps = fmt.get('fps', '?')
                if fps != '?' and isinstance(fps, (int, float)):
                    fps = int(round(fps))

                tbr = fmt.get('tbr', '?')
                if tbr != '?' and isinstance(tbr, (int, float)):
                    tbr = int(round(tbr))
                
                print(f"{i + 1} | {fmt.get('height', '?')}p | {fps} FPS | Битрейт: {tbr} kbit/s | {fmt.get('ext', '')} | {filesize_display} MB")

            while True:
                try:
                    choice = int(input("\nВыберите качество для всех видео плейлиста (введите номер): ")) - 1
                    if 0 <= choice < len(filtered_formats):
                        break
                    print("Неверный номер. Попробуйте снова.")
                except ValueError:
                    print("Введите число.")

            selected_format = filtered_formats[choice]
            
            # Создаем новые опции с выбранным форматом
            download_opts = base_opts.copy()
            format_id = selected_format['format_id']
            download_opts['format'] = f"{format_id}+bestaudio/best"
            download_opts['outtmpl'] = str(playlist_dir / '%(title)s.%(ext)s')

            print("\nНачинается загрузка плейлиста...")
            print("Все видео будут загружены и сконвертированы в MP4 с кодеком H264")
            
            # Загружаем видео
            with yt_dlp.YoutubeDL(download_opts) as ydl_download:
                for i, video in enumerate(playlist_info['entries'], 1):
                    if video is None:
                        print(f"\nВидео #{i}: Пропущено из-за ошибки получения информации")
                        continue
                    
                    print(f"\nЗагрузка видео #{i}: {video.get('title', 'Без названия')}")
                    video_url = video.get('webpage_url')
                    try:
                        ydl_download.download([video_url])
                    except Exception as e:
                        print(f"Ошибка при загрузке видео #{i}: {str(e)}")
                        continue
            
            print("\nЗагрузка плейлиста завершена!")
            print(f"Файлы сохранены в директории: {playlist_dir}")
            
        except Exception as e:
            print(f"\nОшибка при работе с плейлистом: {str(e)}")
            print("Полное описание ошибки:")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    playlist_url = input("Введите URL плейлиста: ")
    download_playlist(playlist_url)