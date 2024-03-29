# Модуль фитнес трекера

## Содержание:

- [Описание проекта](#описание-проекта)
- [Технологический стек](#технологический-стек)
- [Как развернуть проект](#как-развернуть-проект)
- [Запуск приложения](#запуск-приложения)
- [Над проектом работал](#над-проектом-работал)

---

### Описание проекта:

Программный модуль фитнес-трекера, который обрабатывает данные для трёх видов
тренировок: бега, спортивной ходьбы и плавания.

#### Функции, которые выполняет модуль:

- принимает от блока датчиков информацию о прошедшей тренировке,
- определяет вид тренировки,
- рассчитывает результаты тренировки,
- выводит информационное сообщение о результатах тренировки.

#### Информационное сообщение, которое выводит модуль, включает следующие данные:

- тип тренировки (бег, ходьба или плавание);
- длительность тренировки;
- дистанция, которую преодолел пользователь, в километрах;
- среднюю скорость на дистанции, в км/ч;
- расход энергии, в килокалориях.

---

### Технологический стек:

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)

---

### Как развернуть проект:

Клонировать репозиторий и перейти в него в терминале используя команду

```bash
cd
```

```bash
git clone git@github.com:aleksandr-miheichev/fitness_tracker.git
```

Создать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

---

### Запуск приложения:

Чтобы запустить модуль, необходимо в терминале использовать команду:

```bash
python .\homework.py
```

---

### Над проектом работал:

- [Михеичев Александр](https://github.com/aleksandr-miheichev)
