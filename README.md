# Apple-TV стил начален екран за Chromecast с Google TV

Личен fork на [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) (MIT) — лаунчър `com.gathin.tvhome`,
променен за Chromecast HD с Google TV (Android 14), без реклами и с по-красив начален екран.

Какво е добавено спрямо оригинала:
- карта за времето (Open-Meteo, без ключ) със собствено нарисувани икони и **размазан фон** (blur) от тапета;
- тапети от собствени снимки, затъмнени за четимост, въртят се на случаен принцип;
- затъмняване отдолу за четим текст, по-ниска лента с приложения, скрит втори ред;
- нужно е разрешение `INTERNET` (за времето) — затова не е подходящ за upstream.

## Папки
- `launcher/` — Android проектът (JDK 17, Android SDK 34): `cd launcher && ./gradlew assembleRelease`.
- `my-theme/` — `config.json` и `wallpapers/` (+ `wallpapers-unused/` с генерирани тапети).
- `process-photos.sh` — подготвя снимки от `my-photos/` в тапети 1920x1080 (нужен е ImageMagick).
- `my-wallpapers/` — скриптове, които генерират абстрактни тапети (SVG).
- `restore-chromecast.sh` — връща стария Google TV лаунчър: `./restore-chromecast.sh <tv ip>:<порт>`.
- `tools/` — ADB инструментите от оригиналния проект.

## Как се ползва
1. Включи Developer options и Wireless debugging на Chromecast-а, свържи се с `adb pair` / `adb connect`.
2. Смени града в `launcher/app/src/main/res/values/config.xml` (`weather_city`, `weather_lat`, `weather_lon`).
3. Компилирай и инсталирай APK-то: `adb install -r launcher/app/build/outputs/apk/release/app-release.apk`.
4. Качи темата през доставчика на лаунчъра (`adb shell content write --uri content://com.gathin.tvhome.theme/<файл>`),
   не с `adb push`.
5. Направи го Home — прочети първо `tools/` и `launcher/build-and-install.sh`: ако изключиш `setupwraith`/`launcherx`
   неправилно, устройството може да влезе в boot loop. Първо прави backup и дръж `restore-chromecast.sh` подръка.

Внимание: когато `setupwraith` е изключен, кастването от телефон може да спре да работи. Изключи Wireless debugging, когато приключиш.
