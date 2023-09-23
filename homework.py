"""Модуль фитнес-трекера"""

from dataclasses import asdict, dataclass, fields


@dataclass()
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFO = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Возвращает информационное сообщение о выполненной тренировке."""
        return self.INFO.format(**asdict(self))


@dataclass()
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_HOUR = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Создаёт объект сообщения о результатах тренировки."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLIER = 18
    SPEED_SUBTRAHEND = 20

    def get_spent_calories(self) -> float:
        """Рассчитывает количество потраченных ккал за тренировку: бег."""
        return ((self.SPEED_MULTIPLIER * self.get_mean_speed()
                 - self.SPEED_SUBTRAHEND) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


@dataclass()
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: int
    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029

    def get_spent_calories(self) -> float:
        """
        Рассчитывает количество потраченных ккал
        за тренировку: спортивная ходьба.
        """
        return ((self.WEIGHT_MULTIPLIER_1 * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.WEIGHT_MULTIPLIER_2 * self.weight) * self.duration
                * self.MIN_IN_HOUR)


@dataclass()
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    SPEED_TERM = 1.1
    SPEED_MULTIPLIER = 2

    def get_mean_speed(self) -> float:
        """Рассчитывает среднюю сокрость при тренировки: плавание."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Рассчитывает количество потраченных ккал за тренировку: плавание."""
        return ((self.get_mean_speed() + self.SPEED_TERM)
                * self.SPEED_MULTIPLIER * self.weight)


WORKOUT_FAIL = (
    '{} - не подходящий тип тренировки. Выберите, пожалуйста, корректный тип '
    'тренировки.'
)

DATA_FAIL = (
    'У типа тренировки {} необходимое количество параметров тренировки'
    ' равно {}, но сейчас поступают данные только от {}, поэтому проверьте,'
    ' пожалуйста, работу датчиков.'
)

DATA_MATCHING = {
    'SWM': (Swimming, len(fields(Swimming))),
    'RUN': (Running, len(fields(Running))),
    'WLK': (SportsWalking, len(fields(SportsWalking)))
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in DATA_MATCHING:
        raise KeyError(WORKOUT_FAIL.format(workout_type))
    if len(data) not in DATA_MATCHING[workout_type]:
        raise TypeError(DATA_FAIL.format(
            DATA_MATCHING[workout_type][0].__name__,
            DATA_MATCHING[workout_type][1],
            len(data))
        )
    return DATA_MATCHING[workout_type][0](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
