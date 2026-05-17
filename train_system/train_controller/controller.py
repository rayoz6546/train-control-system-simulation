import time

P_MAX = 120000


class Controller:
    """Forward Euler PI Controller implementation"""

    def __init__(self, sim_time) -> None:
        self._time = sim_time
        self._current_time = self._time[0]
        self._prev_time = self._current_time
        self.kp = 0
        self.ki = 0
        self._p_term = 0
        self._i_term = 0

    def set_gains(self, kp: float, ki: float):
        self.kp = kp
        self.ki = ki

    def update(self, curr_value: float, desired_value: float) -> float:
        """Calculate output based off gains and error"""
        self._current_time = self._time[0]
        dt = self._current_time - self._prev_time
        error = desired_value - curr_value

        self._p_term = self.kp * error
        error_rate = error * dt
        if self._i_term + error_rate < P_MAX:
            self._i_term += error_rate

        self._prev_time = self._current_time
        return self._p_term + (self.ki * self._i_term)
