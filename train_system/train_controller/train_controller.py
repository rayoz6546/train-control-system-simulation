import threading
from typing import Tuple
from .controller import Controller, P_MAX
from .backup_controller import BackupController

DWELL_TIME = 60
BRAKING_DIFF = .5
BACKUP_THRESH = 2000
STOPPING_SPEED = 15
SLOW_DOWN_DIST = 0.0124

KP = 8000
KI = 10

NIGHT_HOUR = 7
DAY_HOUR = 7

TRAIN_MASS = 40900.0
SERVICE_BRAKE_FORCE = TRAIN_MASS * 1.2
E_BRAKE_FORCE = TRAIN_MASS * 2.73


class TrainController:
    """Train Controller class"""

    def __init__(self, signals, test=False) -> None:
        # Key
        self._speed_limit = 0
        self._commanded_speed = 0  # From CTC
        self._setpoint_speed = 0  # From Driver
        self._actual_speed = 0
        self._service_brake = False
        self._emergency_brake = False
        self._authority = 0
        self._beacon = ""
        self._station_name = ""
        self._manual_mode = False
        self._output_power = 0
        self._power = 0
        self._time = [0]
        self._prev_station = None
        self._dispatched = False
        # Faults
        self._signal_pickup_fail = False
        self._engine_fail = False
        self._brake_fail = False

        # Non-Vital
        self._left_door_open = False
        self._right_door_open = False
        self._door_side = ""
        self._lights_on = False
        self._ext_lights_on = False

        self._is_stop = False
        self._stop_time = 0
        self._slow_down = False
        self._e_slow_down = False
        self._underground = False

        self._controller = Controller(self._time)
        self._backup_controller = BackupController(self._time)

        self.set_gains(KP, KI)

        self._signals = signals

        self._ui = None
        self._e_ui = None
        if not test:
            self.update()

    def update(self, thread=False):
        """Update train controller values"""
        if not self._dispatched and self.get_current_speed() > 0:
            self._dispatched = True

        self.set_authority(self._signals.authority)
        self.set_train_speed(self._signals.train_speed)
        self.set_commanded_speed(self._signals.commanded_speed)
        self.set_speed_limit(self._signals.speed_limit)
        self.set_beacon(self._signals.beacon)
        self.set_engine_fault(self._signals.engine_fault)
        self.set_brake_fault(self._signals.brake_fault)
        self.set_signal_fault(self._signals.signal_pickup_fault)
        self._time[0] = self._signals.time
        self._door_side = self._signals.door
        self._underground = self._signals.underground

        self.control_lights()
        self._signals.internal_lights = self.get_lights()
        self._signals.external_lights = self.get_ext_lights()
        self._signals.left_door, self._signals.right_door = self.get_doors()
        self._signals.service_brake = self.get_service_brake()
        self._signals.emergency_brake = self.get_emergency_brake()
        self._signals.power = self.calculate_power()

        if thread:
            threading.Timer(0.1, self.update).start()

    def get_dispatched(self) -> bool:
        """Train's dispatch status"""
        return self._dispatched

    def set_train_speed(self, speed: int):
        self._actual_speed = speed

    def get_authority(self) -> float:
        return self._authority

    def set_authority(self, authority: float):
        self._authority = authority

    def get_beacon(self) -> str:
        return self._beacon

    def set_beacon(self, beacon: str):
        self._beacon = beacon

    def get_station_name(self):
        """Parses beacon if station, returns formatted name"""
        if self._beacon != "" and "STATION;" in self._beacon:
            if "Switch" in self._beacon:
                start = self._beacon.find("Switch")
                beacon = self._beacon[:start]
            else:
                beacon = self._beacon

            start_semi = beacon.find(";") + 2
            end_semi = beacon[start_semi:].find(";")
            if end_semi != -1:
                return beacon[start_semi:][:end_semi]
            return beacon[start_semi:]
        return ""

    def get_mode(self) -> bool:
        return self._manual_mode

    def toggle_mode(self, mode: bool):
        self._manual_mode = mode

    def toggle_lights(self, lights: bool):
        self._lights_on = lights

    def toggle_ext_lights(self, lights: bool):
        self._ext_lights_on = lights

    def control_lights(self):
        """Turns lights on at night and underground"""
        if not self.get_mode():
            if self._underground or self.get_time_of_day():
                self.toggle_lights(True)
                self.toggle_ext_lights(True)
            else:
                self.toggle_lights(False)
                self.toggle_ext_lights(False)

    def get_lights(self) -> bool:
        return self._lights_on

    def get_ext_lights(self) -> bool:
        return self._ext_lights_on

    def get_speed_limit(self) -> float:
        return self._speed_limit

    def set_speed_limit(self, speed_limit: float):
        self._speed_limit = int(speed_limit)

    def set_gains(self, kp: float, ki: float):
        """Sets kp and ki of controllers"""
        self._controller.set_gains(kp=kp, ki=ki)
        self._backup_controller.set_gains(kp=kp, ki=ki)

    def get_gains(self) -> Tuple[float, float]:
        return (self._controller.kp, self._controller.ki)

    def set_setpoint_speed(self, setpoint_speed):
        self._setpoint_speed = min(self.get_speed_limit(), setpoint_speed)

    def get_setpoint_speed(self) -> float:
        return self._setpoint_speed

    def set_commanded_speed(self, commanded_speed):
        self._commanded_speed = commanded_speed

    def get_commanded_speed(self) -> float:
        return self._commanded_speed

    def get_time(self) -> int:
        return self._time[0]

    def get_time_of_day(self) -> bool:
        hour = self.get_time() // 3600
        return hour > NIGHT_HOUR + 12 or hour <= DAY_HOUR

    def update_stop(self):
        """Stop train and open doors at stop"""
        if (
            self.get_station_name() != ""
            and not self._is_stop
            and self._prev_station != self.get_station_name()
            and self.get_authority() <= 0
        ):
            self._is_stop = True
            self._stop_time = self.get_time()
            self.set_service_brake(True)

            if self._door_side == "Left":
                self.set_doors(True, True)
            elif self._door_side == "Right":
                self.set_doors(False, True)
            else:
                self.set_doors(False, True)
                self.set_doors(True, True)

        # Checks if train should leave
        if (
            self._is_stop
            and self.get_time() >= self._stop_time + DWELL_TIME
            or self.get_mode()
        ):
            self._is_stop = False
            self.set_service_brake(False)
            self.set_doors(False, False)
            self.set_doors(True, False)

        self._prev_station = self.get_station_name()

    def calculate_power(self) -> float:
        """Calculate output power"""
        if not self.get_mode():
            self.update_stop()
        if any(self.get_faults()):
            self._emergency_brake = True

        if self._manual_mode:
            speed = self._setpoint_speed
        else:
            speed = self._commanded_speed

        if (
            self._authority <= 0
            or self.get_emergency_brake()
            or self.get_service_brake()
        ):
            self._controller.update(curr_value=self._actual_speed, desired_value=0.0)
            self._backup_controller.update(
                curr_value=self._actual_speed, desired_value=0.0
            )
            power = 0.0
        else:
            power = self._controller.update(
                curr_value=self._actual_speed, desired_value=speed
            )
            backup_power = self._backup_controller.update(
                curr_value=self._actual_speed, desired_value=speed
            )

            if abs(power - backup_power) > BACKUP_THRESH:
                power = (power + backup_power) / 2

            power = round(power, 2) if power > 0 else 0.0

        s_brake_dist = self.calculate_braking_dist(self.get_current_speed())
        e_brake_dist = self.calculate_ebraking_dist(self.get_current_speed())

        if self._actual_speed > speed + BRAKING_DIFF:
            self._slow_down = True
        elif self.get_authority() <= 0 and s_brake_dist > SLOW_DOWN_DIST:
            self._e_slow_down = True
        elif self.get_authority() < s_brake_dist:
            self._slow_down = True
        else:
            self._slow_down = False
            self._e_slow_down = False
        self.get_service_brake()

        self._power = power if power < P_MAX else P_MAX

        return self._power

    def set_engine_fault(self, state: bool):
        self._engine_fail = state

    def set_brake_fault(self, state: bool):
        self._brake_fail = state

    def set_signal_fault(self, state: bool):
        self._signal_pickup_fail = state

    def get_faults(self) -> Tuple[bool, bool, bool]:
        return (self._engine_fail, self._signal_pickup_fail, self._brake_fail)

    def set_doors(self, left_door: bool, door_open: bool):
        if left_door:
            self._left_door_open = door_open
        else:
            self._right_door_open = door_open

    def get_doors(self) -> Tuple[bool, bool]:
        return (self._left_door_open, self._right_door_open)

    def set_service_brake(self, brake: bool):
        self._service_brake = brake

    def get_service_brake(self) -> bool:
        if self._slow_down:
            return True
        return self._service_brake

    def set_emergency_brake(self, brake: bool):
        self._emergency_brake = brake

    def get_emergency_brake(self) -> bool:
        if (self.get_authority() <= 0 and not self._is_stop) or self._e_slow_down:
            return True
        return self._emergency_brake

    def get_current_speed(self) -> float:
        return self._actual_speed

    def calculate_braking_dist(self, speed) -> float:
        """Calculate braking distance for emergency brake
        Args:
            speed: Speed to calculate braking distance at

        Returns:
            Estimated braking distance at current speed
        """
        return (
            0.000621371
            * (0.5 * TRAIN_MASS * (speed * 0.44704) ** 2)
            / SERVICE_BRAKE_FORCE
        )

    def calculate_ebraking_dist(self, speed) -> float:
        """Calculate braking distance for emergency brake
        Args:
            speed: Speed to calculate braking distance at

        Returns:
            Estimated braking distance at current speed
        """
        return 0.000621371 * (0.5 * TRAIN_MASS * (speed * 0.44704) ** 2) / E_BRAKE_FORCE

    def launch_driver_ui(self):
        from train_controller.driver_ui import DriverUI

        self._ui = DriverUI(self)

    def launch_engineer_ui(self):
        from train_controller.engineer_ui import EngineerUI

        if not self._dispatched:
            self._e_ui = EngineerUI(self)
