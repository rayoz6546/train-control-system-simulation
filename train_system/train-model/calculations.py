import time
import math


class Calculations:
    # constructor

    # sample constructor
    def __init__(self, time):
        self._time = time
        self._current_time = self._time[0]
        self._prev_time = self._current_time
        self.cmd_power = 0
        self.cmd_velocity = 0
        self.Pmax = 120000.00  # datasheet says its 120kW
        self.force = 0
        self.passenger_mass = 0
        self.train_weight = 81800.00
        self.train_mass = 0
        self.total_mass = 0
        self.max_accel = 0
        self.acceleration = 0
        self.actual_velocity = 0
        self.decel = 0.0
        self.time = 0
        self.friction_coeff = 0.006

    def set_cmd_power(self, cmd_power: float):
        self.cmd_power = cmd_power

    def set_cmd_velocity(self, cmd_velocity: float):
        self.cmd_velocity = cmd_velocity

    def set_force(self, force: float):
        self.force = force

    def set_accel(self, acceleration: float):
        self.acceleration = acceleration

    def set_passenger_mass(self, passenger_mass: float):
        self.passenger_mass = passenger_mass

    def set_train_mass(self, train_mass: float):
        self.train_mass = (self.train_weight * 4.44822162) / 9.81

    def set_total_mass(self, train_mass: float, passenger_mass: float):
        self.total_mass = train_mass + passenger_mass

    # def set_accel(self, acceleration: float):
    #     self.acceleration = acceleration

    # force calculation
    def calc_force(self, power: float, velocity: float) -> float:
        self.force = power / velocity
        return self.force

    # acceleration calculation
    def calc_accel(self, force: float, mass: float) -> float:
        self.acceleration = force / mass
        return self.acceleration

    # actual velocity calculation
    def calc_Vactaul(self, accel: float) -> float:
        # print("v", self.actual_velocity)
        # calculating dt
        self._current_time = self._time[0]
        dt = self._current_time - self._prev_time
        # Check if time difference is greater than zero
        if dt < 0:
            return 0
        # calculate actual velocity according to change in acceleration over time
        self.actual_velocity += accel * dt
        self._prev_time = self._current_time
        if accel < 0 and self.actual_velocity < 0:
            self.actual_velocity = 0
        return self.actual_velocity

    # def calc_decel(self, accel: float) -> float:
    #     # calculating dt
    #     self._current_time = time.time()
    #     dt = self._current_time - self._prev_time
    #     # Check if time difference is greater than zero
    #     if dt <= 0:
    #         return 0
    #     # calculate acceleration according to change in deceleration over time
    #     self.decel = accel * dt
    #     self._prev_time = self._current_time
    #     return self.decel
