# REALTIME EDIT PERMISSION MATRIX v2

Дата: 2026-07-03 · Статус: **V2 DRAFT**

---

## УРОВНИ БЕЗОПАСНОСТИ

| Уровень | Правило |
|---------|---------|
| ✅ Preview+Confirm | Показать preview → подтверждение → сохранить |
| 📝 Draft first | Сначала draft → confirmed только после подтверждения |
| 💾 Backup | Сделать backup перед изменением |
| 🔒 Owner only | Только после отдельного подтверждения владельца |
| 🚫 No Telegram | Через Telegram нельзя |

---

## МАТРИЦА v2

| # | Блок | Preview+Confirm | Draft first | Backup | Owner only | No Telegram |
|---|------|:---:|:---:|:---:|:---:|:---:|
| 1 | Цены | ✅ | 📝 | 💾 | | |
| 2 | ЛКМ | ✅ | 📝 | | | |
| 3 | Материалы | ✅ | 📝 | 💾 | | |
| 4 | Склад | ✅ | | 💾 | 🔒 | |
| 5 | Заказы | ✅ | | 💾 | | |
| 6 | Правила | ✅ | 📝 | 💾 | 🔒 | |
| 7 | Статусы | ✅ | | | | |
| 8 | Версии | ✅ | | 💾 | | |
| 9 | Доступ / роли | | | 💾 | 🔒 | 🚫 |
| 10 | Backup / защита | | | | 🔒 | 🚫* |

> *Backup через Telegram: можно запустить по просьбе владельца.  
> Нельзя через Telegram: менять настройки backup, пути, политику защиты.

---

## КОММЕНТАРИИ v2

### 1. Цены — Draft first
Новые цены → draft. Active только после подтверждения. Старые заказы не пересчитываются.

### 2. ЛКМ — Draft first
Новые рецепты, профили, нормы → draft. Confirmed после подтверждения. Unknown норма → спросить.

### 3. Материалы — Draft first
Новые закупочные цены и единицы → draft. Confirmed после проверки.

### 4. Склад
Preview + confirm + backup + owner. Критично для производства.

### 5. Заказы
Preview + confirm + backup.

### 6. Правила — Full gate
Preview + confirm + draft first + backup + owner confirm. Меняют логику системы.

### 7. Статусы
Безопасный блок. Preview + confirm.

### 8. Версии
Preview + confirm + backup.

### 9. Доступ / роли
Owner only + no Telegram + backup. Критично. Public/client/staff — запрещены до отдельного плана.

### 10. Backup / защита — особый
- Запустить backup через Telegram: можно по просьбе владельца.
- Менять настройки backup через Telegram: нельзя.
- Менять пути, политику защиты: только owner, только Desktop.

---

## СВОДКА ИЗМЕНЕНИЙ v1→v2

| Блок | Изменение |
|------|-----------|
| Цены | ➕ Draft first |
| ЛКМ | ➕ Draft first |
| Материалы | ➕ Draft first |
| Правила | ➕ Preview+Confirm, ➕ Draft first |
| Backup | 🟡 Telegram: запуск OK, настройки — нет |

---

## СТАТУС

**TELEGRAM_PERMISSION_MATRIX_V2_DRAFT**
