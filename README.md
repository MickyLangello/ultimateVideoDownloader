# Загрузчик видео #

Работает для ВК, Ютуба, Твича, Тиктока и много чего ещё.

[Полный список](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) поддерживаемых ресурсов.

## Начало ##
## Руками ##
Для корректной работы установить [python](https://www.python.org/downloads/), [ffmpeg](https://github.com/GyanD/codexffmpeg/releases/), при необходимости [GoodbyeDPI](https://github.com/ValdikSS/GoodbyeDPI/releases).

### Установщиком Chocolatey###
Установить [Chocolatey](https://chocolatey.org/install).
После установки ввести:
```
choko install python ffmpeg
```
### Установщиком Winget ###
Он скорее всего у вас предустановлен.
В консоли:
```
winget install -e --id Python.Python.3.10
winget install -e --id=Gyan.FFmpeg  
```
## Установка ##
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