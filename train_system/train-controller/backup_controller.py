import time
from .controller import Controller, P_MAX


class BackupController(Controller):
    """Trapezoidal Rule PI Controller implementation"""

    def __init__(self, sim_time) -> None:
        super().__init__(sim_time=sim_time)
        self._prev_error = 0

    def update(self, curr_value: float, desired_value: float) -> float:
        """Calculate output based off gains and error"""
        self._current_time = self._time[0]
        dt = self._current_time - self._prev_time
        error = desired_value - curr_value

        self._p_term = self.kp * error
        error_rate = (dt / 2) * (error + self._prev_error)
        if self._i_term + error_rate < P_MAX:
            self._i_term += error_rate

        self._prev_error = error
        self._prev_time = self._current_time
        return self._p_term + (self.ki * self._i_term)
