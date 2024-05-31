[![OS - Windows](https://img.shields.io/badge/OS-Windows-blue?logo=windows&logoColor=white)](https://www.microsoft.com/")
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![MIT](https://img.shields.io/github/license/trottling/Bender)](https://github.com/trottling/Bender?tab=MIT-1-ov-file#)
[![Commits](https://img.shields.io/github/commit-activity/m/trottling/Bender)](https://github.com/trottling/Bender/commits/main/)
[![Downloads](https://img.shields.io/github/downloads/trottling/Bender/total)](https://github.com/trottling/Bender/releases/latest)
[![Last release](https://img.shields.io/github/v/release/trottling/Bender)](https://github.com/trottling/Bender/releases/latest)

RU | [EN](https://github.com/trottling/Bender/blob/main/README.md)

# Bender - Cканер уязвимостей Windows

<div align="center">
  <img alt="page" src="https://raw.githubusercontent.com/trottling/Bender/main/media/bender.png" width="200"/>
</div>

**Bender - это простое и портативное приложение для поиска уязвимостей в системе Windows с красивым пользовательским интерфейсом, написанное на Python 3.12** (более ранние версии также поддерживаются).
> **NOTE**
>
> Это приложение предназначено для сканирования ТОЛЬКО ВАШЕГО ПК. Автор не несет ответственности за незаконные действия, в которых использовался Bender.
>
> Bender - это бесплатный проект с открытым исходным кодом, который не ведет никакой коммерческой деятельности.
>
> Bender выполняет ТОЛЬКО ЧТЕНИЕ ТОЛЬКО системных файлов, папок или реестра.

![START](https://raw.githubusercontent.com/trottling/Bender/main/media/start.png)

## Оглавление

1. [Требования](#требования)
2. [Как установить](#как-установить)
3. [Особенности](#особенности)
4. [Пример отчета сканирования](#пример-отчета-о-сканировании)
5. [Стек](#стек)
6. [Поддерживаемые БД уязвимостей](#текущие-используемые-базы-данных-уязвимостей)
7. [TODO](#TODO)
8. [Как я могу помочь этому проекту?](#как-я-могу-помочь-этому-проекту)
9. [Запуск или сборка из исходного кода](#запуск-или-сборка-из-исходного-кода)

## Требования

- Windows 8, 8.1, 10 или 11 и новее*
- Права администратора для доступа к системной информации
- Вот и все!

> * Требуется библиотекой PyQT6 и ограничено во избежание ошибок при использовании системных вызовов из старых версий Windows

## Как установить

1. Скачайте [последнюю сборку](https://github.com/trottling/Bender/releases/latest)
2. Получите API-ключ Vulners.com, смотрите [страницу помощи](https://github.com/trottling/Bender/blob/main/.docs/RU/VULNERS-API-KEY-HELP.md)
3. Добавьте в исключения антивируса, если вы получаете сообщения о Bender.exe
> Это происходит потому, что pyinstaller распаковывает файлы и интерпретатор python в папку temp, поэтому антивирусы не любят такие программы.
4. Запустите от имени администратора
5. Готово!

## Особенности

- Сканирование установленных системных и пользовательских приложений на наличие CVE
- Сканирование драйверов в C:\windows\system32\drivers на наличие уязвимостей
- Сканирование установленных Windows KB на наличие CVE
- Сканирование локальных и внешних портов
- Сканирование общей системной информации
- Сохранение отчета в виде изображения

## Пример отчета о сканировании

![image](https://raw.githubusercontent.com/trottling/Bender/main/media/scan_result.png)

## Стек

| Часть проекта            | Автор(ы)               | Описание                                                              |
|--------------------------|------------------------|-----------------------------------------------------------------------|
| Pretty Icons             | icons8.com             | Курируемая графика, приложения для дизайна и инструменты AI           |
| StyleSheets              | [GTRONICK/QSS]         | Шаблоны таблиц стилей QT                                              |
| CVE Info DB Api          | [mitre.org]            | Решение проблем для более безопасного мира                            |
| БД уязвимых драйверов    | [loldrivers.io]        | курируемый список всех злоупотребляемых драйверов Windows             |
| GUI                      | [PyQT6]                | официальная привязка Python для Qt                                    |
| Обнаружение темной темы  | [darkdetect]           | Обнаружение темного режима ОС из Python                               |
| Сеть                     | [httpx]                | HTTP-клиент нового поколения                                          |
| Взаимодействие с Windows | [windows_tools]        | Коллекция различных интерфейсов для функциональности Windows          |
| Vulners.com API          | [vulners]              | Обертка Vulners.com API v3 для Python                                 |
| HW Info                  | [cpuinfo]              | Модуль для получения информации о процессоре на чистом Python         |
| MAC-адрес                | [getmac]               | Платформонезависимый модуль на чистом Python для получения MAC-адреса |

## Текущие используемые базы данных уязвимостей

- vulners.com
- loldrivers.io

## TODO

- Пока здесь пусто

## Как я могу помочь этому проекту

- Во-первых, посмотрите [TODO лист](#TODO)
- Если у вас есть идеи по доработке, напишите мне в [Telegram](https://t.me/trottling) или откройте [new issue](https://github.com/trottling/Bender/issues/new/choose)
- Исследуйте БЕСПЛАТНЫЕ базы данных уязвимостей с API

## Запуск или сборка из исходного кода

1. Клонируйте или [Скачайте](https://github.com/trottling/Bender/archive/refs/heads/main.zip) исходный код
   `git clone https://github.com/trottling/Bender/tree/main`
2. Перейдите в папку с исходным кодом
   `cd Bender`
3. Установите требования
   `pip install -r requirements.txt`.

- Запуск
  `python main.py`
- Сборка
  `build.bat`

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[PyQT6]: <https://doc.qt.io/qtforpython-6/>

[windows_tools]: <https://github.com/netinvent/windows_tools>

[httpx]: <https://www.python-httpx.org/>

[vulners]: <https://pypi.org/project/vulners/>

[darkdetect]: <https://github.com/albertosottile/darkdetect>

[GTRONICK/QSS]: <github.com/GTRONICK/QSS>

[mitre.org]: <mitre.org>

[loldrivers.io]: <loldrivers.io>

[cpuinfo]: <https://github.com/workhorsy/py-cpuinfo>

[getmac]: <https://github.com/GhostofGoes/getmac>

[PortScan]: <https://github.com/Aperocky/PortScan>
