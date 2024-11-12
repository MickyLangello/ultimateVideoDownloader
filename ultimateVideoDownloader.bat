@echo off
chcp 65001
cls

:menu
color 0B
echo ╔══════════════════════════════════════════╗
echo ║     Ultimate YouTube Downloader v1.0     ║
echo ╠══════════════════════════════════════════╣
echo ║ Выберите тип загрузки:                   ║
echo ║                                          ║
echo ║ [1] Загрузить одно видео                 ║
echo ║ [2] Загрузить плейлист видео             ║
echo ║ [3] Загрузить аудио из видео             ║
echo ║ [4] Загрузить аудио из плейлиста         ║
echo ║                                          ║
echo ║ [0] Выход                                ║
echo ╚══════════════════════════════════════════╝

set /p choice="Введите номер (0-4): "

if "%choice%"=="1" (
    cls
    echo ╔══════════════════════════════════════════╗
    echo ║             Загрузка видео               ║
    echo ╚══════════════════════════════════════════╝
    python scripts/video_downloader.py
    echo.
    echo Нажмите любую клавишу для возврата в меню...
    pause > nul
    goto menu
)

if "%choice%"=="2" (
    cls
    echo ╔══════════════════════════════════════════╗
    echo ║        Загрузка плейлиста видео          ║
    echo ╚══════════════════════════════════════════╝
    python scripts/video_playlist_downloader.py
    echo.
    echo Нажмите любую клавишу для возврата в меню...
    pause > nul
    goto menu
)

if "%choice%"=="3" (
    cls
    echo ╔══════════════════════════════════════════╗
    echo ║             Загрузка аудио               ║
    echo ╚══════════════════════════════════════════╝
    python scripts/audio_downloader.py
    echo.
    echo Нажмите любую клавишу для возврата в меню...
    pause > nul
    goto menu
)

if "%choice%"=="4" (
    cls
    echo ╔══════════════════════════════════════════╗
    echo ║        Загрузка плейлиста аудио          ║
    echo ╚══════════════════════════════════════════╝
    python scripts/audio_playlist_downloader.py
    echo.
    echo Нажмите любую клавишу для возврата в меню...
    pause > nul
    goto menu
)

if "%choice%"=="0" (
    cls
    echo ╔══════════════════════════════════════════╗
    echo ║               До свидания!               ║
    echo ╚══════════════════════════════════════════╝
    timeout /t 2 > nul
    exit
)

echo.
echo Неверный выбор! Попробуйте снова...
timeout /t 2 > nul
cls
goto menu