import yt_dlp
from pathlib import Path

def download_video(url):
    videos_dir = Path('videos')
    videos_dir.mkdir(exist_ok=True)
    
    base_opts = {
        'noplaylist': True,
        'socket_timeout': 60,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'ffmpeg_args': [
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-preset', 'medium',
            '-crf', '23',
            '-movflags', '+faststart',
        ],
        'outtmpl': str(videos_dir / '%(title)s.%(ext)s'),
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

            print("Видео будет загружено и сконвертировано в MP4 с кодеком H264")
            
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