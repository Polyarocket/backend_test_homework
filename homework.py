class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""       
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration, 
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        
        
class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        coeff_kcal_1 = 18
        coeff_kcal_2 = 20
        hour: float = 60
        kcals_running = (
            (
                ((coeff_kcal_1 * self.get_mean_speed() 
                - coeff_kcal_2) * self.weight) / self.M_IN_KM 
                * self.duration * hour
            )
        )
        return kcals_running


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_kcal_3 = 0.035
        coeff_kcal_4 = 0.029
        hour = 60
        kcals_walk = (
            (
                (coeff_kcal_3 * self.weight + (self.get_mean_speed() 
                ** 2 // self.height) 
                * coeff_kcal_4 * self.weight) * self.duration * hour
            )
                     )
        return kcals_walk


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed_swim = (
            (
                self.length_pool * self.count_pool 
                / self.M_IN_KM / self.duration
            )
        )
        return speed_swim

    def get_spent_calories(self) -> float:
        coeff_kcal_5 = 1.1
        kcals_swim = (self.get_mean_speed() + coeff_kcal_5) * 2 * self.weight
        return kcals_swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    package = {
        'RUN' : Running ,
        'WLK' : SportsWalking ,
        'SWM' : Swimming
    }
    what_trn = package[workout_type](*data)
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