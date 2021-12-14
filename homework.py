from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    mes: str = ('Тип тренировки: {training_type}; '
                'Длительность: {duration:.3f} ч.; '
                'Дистанция: {distance:.3f} км; '
                'Ср. скорость: {speed:.3f} км/ч; '
                'Потрачено ккал: {calories:.3f}.'
                )

    def get_message(self) -> str:
        return self.mes.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration_h
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(type(self).__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    kcal_speed_multiplier: float = 18
    kcal_speed_sub: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        kcals_running = (
            (
                ((self.kcal_speed_multiplier * self.get_mean_speed()
                 - self.kcal_speed_sub) * self.weight_kg) / self.M_IN_KM
                * self.duration_h * self.MIN_IN_H
            )
        )
        return kcals_running


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    kcal_multiplier_sw_1: float = 0.035
    kcal_multiplier_sw_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        kcals_walk = (
            (
                     (self.kcal_multiplier_sw_1 * self.weight_kg
                      + (self.get_mean_speed() ** 2 // self.height_cm)
                      * self.kcal_multiplier_sw_2 * self.weight_kg)
                * self.duration_h * self.MIN_IN_H
            )
        )
        return kcals_walk


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    kcal_swim_sum: float = 1.1
    kcal_swim_multiplier: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed_swim = (
            (
                self.length_pool_m * self.count_pool
                / self.M_IN_KM / self.duration_h
            )
        )
        return speed_swim

    def get_spent_calories(self) -> float:
        kcals_swim = (
            (
                (self.get_mean_speed() + self.kcal_swim_sum)
                * self.kcal_swim_multiplier * self.weight_kg
            )
        )
        return kcals_swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings_list: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    what_trn = trainings_list[workout_type](*data)
    if workout_type not in trainings_list:
        raise ValueError('Тип тренировки отсутствует')
    return what_trn


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
