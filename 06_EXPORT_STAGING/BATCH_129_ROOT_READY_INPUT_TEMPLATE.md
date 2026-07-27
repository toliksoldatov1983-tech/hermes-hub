# ROOT_READY INPUT TEMPLATE

Для активации real-folder chain укажите точный путь к корню заказов:

```
ROOT_READY:
<точный путь к корню заказов>
```

Примеры:

```
ROOT_READY:
E:\Заказы
```

```
ROOT_READY:
D:\Заказы
```

```
ROOT_READY:
C:\Заказы
```

## Правило

После ROOT_READY следующий пакет делает controlled preflight указанного root.
Сразу copy в реальные папки НЕ выполняется.
