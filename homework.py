class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                training_type: str,
                duration: float,
                distance: float,
                speed: float,
                calories: float
                ) -> None:
                
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
        self.speed = self.get_distance() / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__,
                          self.duration,
                          self.get_distance(),
                          self.get_mean_speed(),
                          self.get_spent_calories())
        return info
        
    
class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        COEFF_CALORIE_1 = 18
        COEFF_CALORIE_2 = 20 
        ccal = ((COEFF_CALORIE_1 * self.get_mean_speed() - COEFF_CALORIE_2
            ) * self.weight / self.M_IN_KM * self.duration * 60)
        return ccal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
            action: int,
            duration: float,
            weight: float,
            height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) ->float:
        WCCAL_1 = 0.035
        WCCAL_2= 0.029
        ccal_walking = ((WCCAL_1 * self.weight + (self.get_mean_speed() ** 2
                     // self.height) * WCCAL_2 * self.weight) * self.duration * 60)
        return ccal_walking

class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 count_pool: int,
                 length_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        mean_speed = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        SWCCAL_1 = 1.1
        SWCCAL_2 = 2
        swim_ccal = (self.get_mean_speed() + SWCCAL_1) * SWCCAL_2 * self.weight
        return swim_ccal

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict ={
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_dict:
        return training_dict[workout_type](*data)
    else:
        print ('Неизвестный тип тренировки')
            
def main(training: Training) -> None:
    """Главная функция."""
    info:InfoMessage = training.show_training_info()
    print (info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

