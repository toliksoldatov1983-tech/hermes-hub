# ARCHITECTURE

## Flow

Пользователь -> интерфейс / Telegram / CLI -> Hermes router -> safety gate -> task manager -> memory registry -> AI provider adapter -> modules -> reports / responses.

## Core

Hermes Core отвечает за маршрутизацию, безопасность, задачи, память, AI adapters, Telegram dry-run и review-loop.

## Malyarka module

Hermes core -> `hermes_modules.malyarka` -> parser / order preview / disputes / exports позже.

Malyarka не управляет всем Hermes.
