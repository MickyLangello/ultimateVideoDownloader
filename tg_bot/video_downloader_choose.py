import yt_dlp
from pathlib import Path

def download_video(url):
    videos_dir = Path('downloads')
    videos_dir.mkdir(exist_ok=True)
    base_opts = {
        'noplaylist': True,
        'socket_timeout': 120,
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': str(videos_dir / '%(title)s.%(ext)s'),
        # 'proxy': 'socks5://127.0.0.1:10801',
        'http_chunk_size': 10485760,
        'nocheckcertificate': True,
        'merge_output_format': 'mkv',
        'writethumbnail': False,
        'postprocessors': [],
        'retries': 5,
        # 'ffmpeg_location': '/usr/bin/ffmpeg',
        'prefer_ffmpeg': True,
        'keepvideo': False,
    }
    with yt_dlp.YoutubeDL(base_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            
            if not formats:
                print("Нет доступных форматов")
                return

            # Фильтруем форматы, оставляя видео форматы
            filtered_formats = []
            for f in formats:
                # Проверяем только что это видео формат (не только аудио)
                if f.get('vcodec') != 'none':
                    # Добавляем дополнительную информацию для сортировки
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
                    choice = int(input("\nВыберите качество (введите номер): ")) - 1
                    if 0 <= choice < len(filtered_formats):
                        break
                    print("Неверный номер. Попробуйте снова.")
                except ValueError:
                    print("Введите число.")

            selected_format = filtered_formats[choice]
            
            # Создаем новые опции с выбранным форматом
            download_opts = base_opts.copy()
            
            # Устанавливаем формат для загрузки
            format_id = selected_format['format_id']
            download_opts['format'] = f"{format_id}+bestaudio/best"
            
            # Загружаем видео
            with yt_dlp.YoutubeDL(download_opts) as ydl_download:
                ydl_download.download([url])
            
            print("\nВидео успешно загружено и сконвертировано!")
            print(f"Файл сохранен в директории: {videos_dir}")
            
        except Exception as e:
            print(f"\nОшибка при загрузке: {str(e)}")
            print("Полное описание ошибки:")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    video_url = input("Введите URL видео: ")
    download_video(video_url)
