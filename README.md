# Yandex Music Scripts
## In English
A set of Python-based mini-applications based on [unofficial API by MarshalX](https://github.com/MarshalX/yandex-music-api) aimed at fetching some basic information from Yandex Music streaming service.

In order to use it, you will have to get a token (see [here](https://yandex-music.readthedocs.io/en/main/token.html) (in Russian) how to get it) and insert it into the application code instead of “`YOUR_TOKEN`” where necessary.

### Scripts
Currently ready scripts and what they can do:
* [albums.py](https://github.com/wileyfoxyx/yam-scripts/blob/main/albums.py) - album title and its main artist, year and full release date of the album, full track list with all artists and track durations, information about the release label (taken from the “Label” and “Phonographic source” lines from the Yandex Music itself) and its distributor. [^1]
* [tracks.py](https://github.com/wileyfoxyx/yam-scripts/blob/main/tracks.py) - track title and its artist(s), year and full date of the release that includes this track, track duration, information about the release label (taken from the “Label” and “Phonographic source” lines from the Yandex Music itself) and its distributor.
* [videoshots.py](https://github.com/wileyfoxyx/yam-scripts/blob/main/videoshots.py) - track title and its artist(s), link to the videoshot [^2] attached to the track.

Each of the scripts accepts both a separate necessary ID (of a track or an album) as well as a full link to it.

If you have problems with the scripts, or have a suggestion on how to improve them, feel free to [create an issue](https://github.com/wileyfoxyx/yam-scripts/issues/new/choose).

[^1]: The workability of the script with podcasts and audiobooks has not been tested so far.
[^2]: Yandex Music's analogue of Spotify's Canvases. Can be uploaded only by the major labels and supported DIY distributors.

## На русском
Набор мини-приложений, написанных на языке Python и основанных на [неофициальном API от MarshalX](https://github.com/MarshalX/yandex-music-api), для получения некоторой базовой информации из стримингового сервиса "Яндекс Музыка".

Для использования вам потребуется получить токен (см. [здесь](https://yandex-music.readthedocs.io/en/main/token.html) как это сделать) и вставить его в код приложения вместо "`YOUR_TOKEN`" там, где необходимо.

### Описание скриптов
Готовые на данный момент скрипты и что они умеют делать:
* [albums.py](https://github.com/wileyfoxyx/yam-scripts/blob/main/albums.py) – название альбома и его основной исполнитель, год и полная дата выхода альбома, полный трек-лист со всеми исполнителями и продолжительностью треков, информация о лейбле релиза (берется из строки "Лейбл" и "Источник фонограммы" из обычной Я.Музыки) и его дистрибьюторе. [^3]
* [tracks.py](https://github.com/wileyfoxyx/yam-scripts/blob/main/tracks.py) – название трека и его исполнитель(-и), год и полная дата выхода релиза, в который включен данный трек, продолжительность трека, информация о лейбле релиза (берется из строки "Лейбл" и "Источник фонограммы" из обычной Я.Музыки) и его дистрибьюторе.
* [videoshots.py](https://github.com/wileyfoxyx/yam-scripts/blob/main/videoshots.py) – название трека и его исполнитель(-и), ссылка на прикрепленный к треку [видеошот](https://yandex.ru/support/music/ru/performers-and-copyright-holders/video-shot).

Каждый из скриптов принимает как отдельный небходимый ID (трека/альбома), так и полную ссылку на него.

Если возникли проблемы с работой скриптов, или есть предложение по их улучшению, смело [создавайте issue](https://github.com/wileyfoxyx/yam-scripts/issues/new/choose).

[^3]: Работоспособность скрипта с подкастами и аудиокнигами не проверена. 

