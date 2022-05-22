"""Модуль фитнес-трекера"""

from dataclasses import dataclass, fields


@dataclass()
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TRAINING_RESULTS = ('Тип тренировки: {0}; '
                        'Длительность: {1:.3f} ч.; '
                        'Дистанция: {2:.3f} км; '
                        'Ср. скорость: {3:.3f} км/ч; '
                        'Потрачено ккал: {4:.3f}.')

    def get_message(self) -> str:
        """Возвращает информационное сообщение о выполненной тренировке."""
        training_type = self.training_type
        duration = self.duration
        distance = self.distance
        speed = self.speed
        calories = self.calories
        return self.TRAINING_RESULTS.format(training_type, duration, distance,
                                            speed, calories)


@dataclass()
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM = 1000
    LEN_STEP = 0.65
    HOURS_IN_MIN = 60

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
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    MULTIPLIER_FOR_AVERAGE_SPEED = 18
    SUBTRACTED_FOR_AVERAGE_SPEED = 20

    def get_spent_calories(self) -> float:
        """Рассчитывает количество потраченных ккал за тренировку: бег."""
        return ((self.MULTIPLIER_FOR_AVERAGE_SPEED * self.get_mean_speed()
                 - self.SUBTRACTED_FOR_AVERAGE_SPEED)
                * self.weight / self.M_IN_KM * self.duration
                * self.HOURS_IN_MIN)


@dataclass()
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: int
    MULTIPLIER_FOR_WEIGHT_1 = 0.035
    MULTIPLIER_FOR_WEIGHT_2 = 0.029

    def get_spent_calories(self) -> float:
        """
        Рассчитывает количество потраченных ккал
        за тренировку: спортивная ходьба.
        """
        return ((self.MULTIPLIER_FOR_WEIGHT_1 * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.MULTIPLIER_FOR_WEIGHT_2 * self.weight)
                * self.duration * self.HOURS_IN_MIN)


@dataclass()
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    TERM_FOR_AVERAGE_SPEED = 1.1
    MULTIPLIER_FOR_AVERAGE_SPEED = 2

    def get_mean_speed(self) -> float:
        """Рассчитывает среднюю сокрость при тренировки: плавание."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Рассчитывает количество потраченных ккал за тренировку: плавание."""
        return ((self.get_mean_speed() + self.TERM_FOR_AVERAGE_SPEED)
                * self.MULTIPLIER_FOR_AVERAGE_SPEED * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_check = ('{} - не подходящий тип тренировки. Выберите, '
                          'пожалуйста, корректный тип тренировки.')
    checking_the_number_of_training_parameters = ('{} - недостаточное '
                                                  'количество принимаемых '
                                                  'параметров тренировки. '
                                                  'Проверьте, пожалуйста, '
                                                  'работу датчиков.')
    dictionary = dict([('SWM', Swimming), ('RUN', Running),
                       ('WLK', SportsWalking)])
    if workout_type not in dictionary.keys():
        print(workout_type_check.format(workout_type))
    if len(data) != len(fields(dictionary[workout_type])):
        print(checking_the_number_of_training_parameters.format(len(data)))
    return dictionary[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 80, 1, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
