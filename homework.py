"""Модуль фитнес-трекера"""


class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        """Инициизирует атрибуты информационного сообщения о тренировке."""
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Возвращает информационное сообщение о выполненной тренировке."""
        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    HOURS_TO_MIN: int = 60
    action: int
    duration: float
    weight: float

    def __init__(self, action: int, duration: float, weight: float) -> None:
        """Инициизирует атрибуты базового класса тренировки."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Создаёт объект сообщения о результатах тренировки."""
        training_type: str = self.__class__.__name__
        duration: float = self.duration
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    coeff_cal_1: float
    coeff_cal_2: float

    def __init__(self, action: int, duration: float, weight: float) -> None:
        """
        Инициизирует атрибуты класса-родителя.
        Затем инициизирует атрибуты, специфические для тренировки: бег.
        """
        super().__init__(action, duration, weight)
        self.coeff_cal_1 = 18
        self.coeff_cal_2 = 20

    def get_spent_calories(self) -> float:
        """Рассчитывает количество потраченных ккал за тренировку: бег."""
        spent_calories: float = ((self.coeff_cal_1
                                  * self.get_mean_speed()
                                  - self.coeff_cal_2) * self.weight
                                 / self.M_IN_KM
                                 * self.duration * self.HOURS_TO_MIN)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: int
    coeff_cal_1: float
    coeff_cal_2: float

    def __init__(self, action: int, duration: float, weight: float,
                 height: int) -> None:
        """
        Инициизирует атрибуты класса-родителя.
        Затем инициизирует атрибуты, специфические
        для тренировки: спортивная ходьба.
        """
        super().__init__(action, duration, weight)
        self.coeff_cal_1 = 0.035
        self.coeff_cal_2 = 0.029
        self.height = height

    def get_spent_calories(self) -> float:
        """
        Рассчитывает количество потраченных ккал
        за тренировку: спортивная ходьба.
        """
        spent_calories: float = ((self.coeff_cal_1 * self.weight
                                  + (self.get_mean_speed() ** 2
                                     // self.height) * self.coeff_cal_2
                                  * self.weight) * self.duration
                                 * self.HOURS_TO_MIN)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    lenght_pool: int
    count_pool: int
    coeff_cal_1: float
    coeff_cal_2: float

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        """
        Инициизирует атрибуты класса-родителя.
        Затем инициизирует атрибуты, специфические для тренировки: плавание.
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.coeff_cal_1 = 1.1
        self.coeff_cal_2 = 2

    def get_mean_speed(self) -> float:
        """Рассчитывает среднюю сокрость при тренировки: плавание."""
        mean_speed: float = (self.length_pool * self.count_pool / self.M_IN_KM
                             / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Рассчитывает количество потраченных ккал за тренировку: плавание."""
        spent_calories: float = ((self.get_mean_speed() + self.coeff_cal_1)
                                 * self.coeff_cal_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    if workout_type == 'RUN':
        return Running(data[0], data[1], data[2])
    return SportsWalking(data[0], data[1], data[2], data[3])


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
