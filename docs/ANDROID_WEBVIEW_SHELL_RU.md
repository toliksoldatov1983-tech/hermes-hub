# Android WebView Shell App — сборка и запуск

## Что это

Android WebView Shell — минимальная Android-оболочка для Mobile Web UI Hermes-Clean.

Это НЕ полноценное приложение. Это scaffold, который открывает WebView с Mobile Web UI.

## Структура проекта

```
android/HermesWebViewShell/
├── app/
│   ├── src/main/
│   │   ├── java/com/hermes/webview/MainActivity.java
│   │   ├── res/layout/activity_main.xml
│   │   ├── res/values/strings.xml
│   │   ├── res/values/themes.xml
│   │   ├── res/xml/network_security_config.xml
│   │   └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle
├── settings.gradle
└── gradle.properties
```

## Как открыть в Android Studio

1. Установить Android Studio (если ещё нет)
2. File → Open → выбрать `android/HermesWebViewShell`
3. Дождаться синхронизации Gradle
4. Run → Run 'app'

## Как собрать debug APK

```bash
cd android/HermesWebViewShell
./gradlew assembleDebug
```

APK будет в: `app/build/outputs/apk/debug/app-debug.apk`

## Почему нет Play Market

- Это safe-local shell, а не consumer app
- Публикация требует production signing, политики конфиденциальности, иконок
- BATCH_096 — scaffold only. Публикация — future step.

## Почему нет production signing

- Debug APK достаточно для safe-local тестирования
- Production signing требует keystore + APPROVE_PRODUCTION_RELEASE gate

## Почему телефон не подключается через 127.0.0.1

На Android-телефоне `127.0.0.1` = сам телефон, а не ПК.

Для доступа к Hermes-Clean на ПК с телефона нужно:
1. Найти IP ПК в локальной сети (192.168.x.x)
2. Включить LAN mode (`APPROVE_LAN_MODE`)
3. Изменить API URL в shell-приложении на IP ПК

Или:
1. Настроить Tailscale/WireGuard VPN
2. Использовать Tailscale IP ПК

Это будет реализовано в BATCH_097.

## Разрешения Android

| Разрешение | Статус |
|------------|--------|
| INTERNET | ✅ Только для localhost |
| ACCESS_NETWORK_STATE | ❌ Не используется |
| CAMERA, MICROPHONE | ❌ Блокированы |
| STORAGE | ❌ Блокированы |
| LOCATION | ❌ Блокированы |

## Безопасность WebView

| Настройка | Значение |
|-----------|----------|
| JavaScript | ✅ Включён (нужен для Web UI) |
| File access | ❌ Выключен |
| Content access | ❌ Выключен |
| Android JS bridge | ❌ НЕ добавлен |
| Password saving | ❌ Выключен |
| Form data saving | ❌ Выключен |
| Mixed content | ❌ Блокирован |
| Cleartext traffic | ✅ Только localhost |

## CLI команды

```cmd
scripts\hermes.cmd android-shell-status
scripts\hermes.cmd android-shell-files
scripts\hermes.cmd android-shell-security-check
scripts\hermes.cmd android-shell-build-info
```
