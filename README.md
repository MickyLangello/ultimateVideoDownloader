# Загрузчик видео #
Репозиторий содержит загрузчик для Google Drive - тестировался в [Google Collab](https://colab.research.google.com/)
Работает для ВК, Ютуба, Твича, Тиктока и много чего ещё.

[Полный список](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) поддерживаемых ресурсов.

## Начало ##
Дальнейшие шаги только для файла **video_downloader.py**
### Подготовка ###
#### Установщиком Winget ####
*(Простой вариант)*
Он скорее всего у вас предустановлен.
В консоли:
```
winget install -e --id Python.Python.3.10
winget install -e --id=Gyan.FFmpeg  
```
#### Установщиком Chocolatey ####
*(Альтернативный вариант)*
Установить [Chocolatey](https://chocolatey.org/install).
После установки ввести:
```
choko install python ffmpeg
```
### Из сурс файлов ###
*(Продвинутый вариант)*
Для корректной работы установить [python](https://www.python.org/downloads/), [ffmpeg](https://github.com/GyanD/codexffmpeg/releases/), при необходимости [GoodbyeDPI](https://github.com/ValdikSS/GoodbyeDPI/releases).

### Установка ###
Создать окружение:
```
python -m venv venv
```
Активировать окружение:
```
venv\Scripts\activate.bat
```
Установить библиотеку:
```
pip install yt_dlp
```