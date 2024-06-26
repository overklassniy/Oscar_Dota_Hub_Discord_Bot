# Документация модуля Tools

Модуль **Tools** включает утилиты, помогающие управлять взаимодействиями и контентом на сервере. Эти инструменты предназначены для упрощения задач по
управлению сервером, делая их более эффективными для администраторов и модераторов.

## Обзор

Этот модуль содержит команды, которые помогают в перемещении сообщений между каналами, управлении правами пользователей и выполнении других
административных задач, повышая функциональность бота и управление сервером.

## Команды

### Move (Переместить)

- **Описание**: Перемещает указанное сообщение в другой канал.
- **Использование**: `!move #<channel>`
- **Требуемые права**: Роль администратора / модератора / хелпера
- **Детали**:
  - `channel`: Целевой канал, куда будет перемещено сообщение.
    - Эта команда требует, чтобы пользователь вызвал команду в ответ на сообщение, которое он хочет переместить. Содержимое сообщения будет повторно
      опубликовано в указанном канале в виде встраиваемого сообщения (embed), а затем удалено из исходного канала.
    - Права: Эта команда ограничена пользователями с административными привилегиями или определенными ролями, указанными в конфигурации бота.

## Конфигурация

**Расположение файла**: `bot/cogs/Tools.py`

Модуль Tools является критически важным для эффективного управления сервером, позволяя быстро изменять размещение и видимость сообщений, что может
помочь поддерживать порядок и организацию в каналах общения сервера.

Для получения более подробных инструкций о том, как использовать и настроить модуль Tools, обратитесь к исходному коду, доступному в репозитории
GitHub.

[Вернуться к основной документации](https://github.com/overklassniy/Oscar_Dota_Hub_Discord_Bot/blob/master/docs/ru/Документация.md)
