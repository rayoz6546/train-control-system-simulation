# import sys,os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from train_model.calculations import Calculations
from signals.train_signals import TrainSignals
from signals.track_signals import TrackSignals
import math
import random

# from calculations import Calculations
import threading
import numpy


class TrainModel(object):
    def __init__(self, train_signals: TrainSignals, track_signals: TrackSignals):
        # for calculations:
        self.cmd_power = 0.0
        self.actual_velocity = 0.0
        self.Pmax = 120000.00  # datasheet says its 120kW
        self.force = 0.0
        self.current_passenger_count = 0
        self.passenger_mass = 0.0
        self.train_mass = 40900.0
        self.total_mass = 0.0
        self.accel_limit = 0.0
        self.acceleration = 0.0
        self.actual_velocity = 0.0
        self.friction_coeff = 0.006
        self.theta = 0.0
        self.mgsine_theta = 0.0
        self.mgcos_theta = 0.0
        self.net_force = 0.0
        self.commanded_speed = 0.0
        self.time = 0
        self.block = 0
        self.local_time = 0
        self.beacon = ""
        self.line = ""
        self.authority = 0.0
        self.speed_limit = 0.0
        self.accel_limit = 0.5  # set in the data sheet
        self.eBrake_decel_limit = -2.73  # set in the data sheet
        self.service_Brake_decel_limit = -1.2  # set in the data sheet
        self.gravity = 9.8  # acceleration of gravity = 9.8 m/s^2
        self.elevation = 0.0
        self.grade = 0.0
        self.temperature = 0.0
        self.setpoint_temp = 0.0
        self.max_current_passenger_count = 222  # combine max standing & seating passengers
        self.passengers_departing = 0.0
        self.prev_passenger_count = 0.0
        self.signal_pickup_failure = False
        self.brake_failure = False
        self.engine_failure = False
        self.service_brake = False
        self.e_brake = False
        self.internal_lights = False
        self.external_lights = False
        self.right_doors = False
        self.left_doors = False
        self.door = ""
        self.station_side = ""
        self.time = [0]
        self.underground = False
        self.line = ""
        self.doors_open = False

        self._calculations = Calculations(self.time)
        self._train_signals = train_signals
        self._track_signals = track_signals
        self.update()

    def update(self, thread=False):

        # read in inputs from train controller
        self.set_external_lights(self._train_signals.external_lights)
        self.set_internal_lights(self._train_signals.internal_lights)
        self.set_left_doors(self._train_signals.left_door)
        self.set_right_doors(self._train_signals.right_door)
        self.set_service_brake(self._train_signals.service_brake)
        self.set_e_brake(self._train_signals.emergency_brake)
        self.set_cmd_power(self._train_signals.power)

        # read in inputs from track model
        self.set_authority(self._track_signals.authority_fromTrack)
        self.set_beacon(self._track_signals.beacon)
        self.set_current_passenger_count(self._track_signals.passenger_count)
        self.set_commanded_speed(self._track_signals.commandedSpeed)
        self.time[0] = self._track_signals.time
        
        self.block = self._track_signals.currentBlock  # update to the next block
        self.line = self._track_signals.lineChoice  # read if we are on the green or red line

        # get grade and elev dict from track model
        if (self.block in self._track_signals.track_grade_elev_green) and self.line == "green":
            # update grade and elevation as long as block number is in dictionary
            self.set_grade(float(self._track_signals.track_grade_elev_green[self.block][0]))
            self.set_elevation(float(self._track_signals.track_grade_elev_green[self.block][1]))
            # check if train in underground
            self.set_underground(self._track_signals.track_grade_elev_green[self.block][2])
        elif (self.block in self._track_signals.track_grade_elev_red) and self.line == "red":
            # update grade and elevation as long as block number exists in dictionary
            self.set_grade(float(self._track_signals.track_grade_elev_red[self.block][0]))
            self.set_elevation(float(self._track_signals.track_grade_elev_red[self.block][1]))
            # check if train in underground
            self.set_underground(self._track_signals.track_grade_elev_red[self.block][2])

        # get speed limit and station side from track model
        if (self.block in self._track_signals.track_speedLim_stat_green) and self.line == "green":
            # update speed limit and station side as long as block number is in dictionary
            self.set_speed_limit(float(self._track_signals.track_speedLim_stat_green[self.block][0]))
            self.set_station_side(self._track_signals.track_speedLim_stat_green[self.block][1])
        elif (self.block in self._track_signals.track_speedLim_stat_red) and self.line == "red":
            # update speed limit and station side as long as block number exists in dictionary
            self.set_speed_limit(float(self._track_signals.track_speedLim_stat_red[self.block][0]))
            self.set_station_side(self._track_signals.track_speedLim_stat_red[self.block][1])

        # send outputs to train controller
        self.calc_actual_velocity()
        self._train_signals.train_speed = (2.23694 * self.actual_velocity)  # convert to mph
        self.calc_Force()
        self.calc_acceleration()
        self._train_signals.commanded_speed = self._track_signals.commandedSpeed
        self._train_signals.engine_fault = self.get_engine_failure()
        self._train_signals.signal_pickup_fault = self.get_signal_pickup_failure()
        self._train_signals.brake_fault = self.get_brake_failure()
        self._train_signals.authority = self._track_signals.authority_fromTrack
        self._train_signals.door = self.get_station_side()
        self._train_signals.speed_limit = self.get_speed_limit()
        self._train_signals.time = self.time[0]
        self._train_signals.beacon = self.get_beacon()
        self._track_signals.underground = self.get_underground()

        # update previous passenger count if a beacon is present
        if self.beacon != "":
            self.prev_passenger_count = self.get_current_passenger_count()
            # print(self.prev_passenger_count)
        else:
            self.prev_passenger_count = 0
            # print(self.prev_passenger_count)

        # send passengers departing only if we are at a stop
        if not self.doors_open and (self.get_right_doors() or self.get_left_doors()):
            self.doors_open = True
            if self.prev_passenger_count > 0:
                # make sure everyone gets off at the last station before the yard
                if (self.line == "Green" and self.block == 56) or (self.line == "Red" and self.block == 16):
                    self._track_signals.passenger_count = 0
                    self._track_signals.passengers_departing = self.get_current_passenger_count()
                else:
                    self._track_signals.passenger_count = random.randint(0, self.get_current_passenger_count())
                    self._track_signals.passengers_departing = random.randint(0, self.get_current_passenger_count())
            else:
                # otherwise, if there is no one on the train, no one will get off
                self._track_signals.passenger_count = self.get_current_passenger_count()
                self._track_signals.passengers_departing = 0
        elif self.doors_open and not(self.get_right_doors() or self.get_left_doors()):
            self.doors_open = False
        # send outputs to track model
        self._track_signals.actual_velocity = (2.23694 * self.actual_velocity)  # convert to mph

        # train model sets the internal train temp
        self.set_temperature(self.setpoint_temp)

        # enable threading
        if thread:
            threading.Timer(0.01, self.update).start()

    def set_time(self, time: int):
        self.time = time

    def get_time(self) -> int:
        return self.time

    def set_authority(self, authority: float):
        self.authority = authority

    def get_authority(self) -> float:
        return round(self.authority, 1)

    def set_grade(self, grade: float):
        self.grade = grade

    def get_grade(self) -> float:
        return self.grade

    def set_elevation(self, elevation: float):
        self.elevation = elevation

    def get_elevation(self) -> float:
        return round(self.elevation*0.3048, 1)

    def set_speed_limit(self, speed_limit: float):
        self.speed_limit = speed_limit

    def get_speed_limit(self) -> float:
        return self.speed_limit

    def set_station_side(self, station_side: str):
        self.station_side = station_side

    def get_station_side(self) -> str:
        return self.station_side

    def set_cmd_power(self, cmd_power: float):
        self.cmd_power = cmd_power

    def get_cmd_power(self) -> float:
        return self.cmd_power

    def set_force(self, force: float):
        self.force = force

    def get_force(self) -> float:
        return self.force

    def set_accel(self, acceleration: float):
        self.acceleration = acceleration

    def get_accel(self) -> float:
        return self.acceleration

    def set_current_passenger_count(self, current_passenger_count: int):
        self.current_passenger_count = current_passenger_count

    def get_current_passenger_count(self) -> int:
        return self.current_passenger_count

    def set_passenger_mass(self, current_passenger_count: float):
        self.passenger_mass = current_passenger_count * 150

    def get_passenger_mass(self) -> float:
        return self.current_passenger_count * 150

    def set_total_mass(self, total_mass: float):
        self.total_mass = total_mass

    def get_total_mass(self) -> float:
        return (0.453592 * self.get_passenger_mass()) + self.train_mass  # convert mass to kg

    def set_actual_velocity(self, actual_velocity: float):
        self.actual_velocity = actual_velocity

    def get_actual_velocity(self) -> float:
        return self.actual_velocity

    def set_beacon(self, beacon: str):
        self.beacon = beacon

    def get_beacon(self) -> str:
        return self.beacon

    def set_temperature(self, temp: float):
        if self.setpoint_temp != temp:
            self.local_time = self.time[0]
            self.setpoint_temp = temp
        self.temperature = round(self.setpoint_temp * (1 - math.exp(-(self.time[0] - self.local_time))), 0)

    def get_temperature(self) -> float:
        return self.temperature

    def set_signal_pickup_failure(self, signal_pickup_failure: bool):
        self.signal_pickup_failure = signal_pickup_failure

    def get_signal_pickup_failure(self) -> bool:
        return self.signal_pickup_failure

    def set_brake_failure(self, brake_failure: bool):
        self.brake_failure = brake_failure

    def get_brake_failure(self) -> bool:
        return self.brake_failure

    def set_engine_failure(self, engine_failure: bool):
        self.engine_failure = engine_failure

    def get_engine_failure(self) -> bool:
        return self.engine_failure

    def set_service_brake(self, service_brake: bool):
        self.service_brake = service_brake

    def get_service_brake(self) -> bool:
        return self.service_brake

    def set_e_brake(self, e_brake: bool):
        self.e_brake = e_brake

    def get_e_brake(self) -> bool:
        return self.e_brake

    def set_underground(self, underground: bool):
        self.underground = underground

    def get_underground(self) -> bool:
        return self.underground

    def set_internal_lights(self, internal_lights: bool):
        self.internal_lights = internal_lights

    def get_internal_lights(self) -> bool:
        return self.internal_lights

    def set_external_lights(self, external_lights: bool):
        self.external_lights = external_lights

    def get_external_lights(self) -> bool:
        return self.external_lights

    def set_door(self, door: str):
        self.door = door

    def get_door(self) -> bool:
        return self.door

    def set_right_doors(self, right_doors: bool):
        self.right_doors = right_doors

    def get_right_doors(self) -> bool:
        return self.right_doors

    def set_left_doors(self, left_doors: bool):
        self.left_doors = left_doors

    def get_left_doors(self) -> bool:
        return self.left_doors

    def set_commanded_speed(self, commanded_speed: float):
        self.commanded_speed = commanded_speed

    def get_commanded_speed(self) -> float:
        return self.commanded_speed

    def calc_Force(self) -> float:
        # if commanded power > Pmax
        if self.cmd_power > self.Pmax:
            self.force = self.get_total_mass() * self.accel_limit * self.friction_coeff
        # if train is on flatroad
        if self.elevation == 0.0 and self.grade == 0.0:
            # if commanded power < Pmax & v = 0
            if self.actual_velocity == 0:
                # limit to max power when v = 0
                if self.cmd_power < 0:
                    self.force = (self.get_total_mass() * self.eBrake_decel_limit * self.friction_coeff)  # TODO: leave as ebrake for now
                elif self.cmd_power > 0:
                    self.force = (self.get_total_mass() * self.accel_limit * self.friction_coeff)
            # if commanded power < Pmax & v != 0
            else:
                self.force = abs(self._calculations.calc_force(power=self.cmd_power, velocity=self.actual_velocity)) \
                             - (self.get_total_mass() * self.friction_coeff)  # F = P/v
        # force changes according to grade level
        else:
            # first, find angle of the hill
            self.theta = numpy.arctan(self.get_grade())
            self.mgsine_theta = self.get_total_mass() * self.gravity * numpy.sin(self.theta * (3.14/180))
            self.mgcos_theta = self.get_total_mass() * self.gravity * numpy.cos(self.theta * (3.14/180))
            self.net_force = self.mgsine_theta - (self.friction_coeff * self.mgcos_theta)
            # if commanded power < Pmax & v = 0
            if self.actual_velocity == 0:
                if self.cmd_power < 0:
                    self.force = self.net_force + (self.get_total_mass() * self.eBrake_decel_limit)
                elif self.cmd_power > 0:
                    self.force = -1*self.net_force + self.cmd_power
            # if commanded power < Pmax & v != 0
            else:
                self.force = (-1*self.net_force + self._calculations.calc_force(power=self.cmd_power, velocity=self.actual_velocity))
        # if brakes are pulled:
        if self.get_service_brake():
            self.force += self.get_total_mass() * self.service_Brake_decel_limit
        elif self.get_e_brake():
            self.force += self.get_total_mass() * self.eBrake_decel_limit
        # if there are any faults, stop the train from moving
        if self.get_engine_failure() or self.get_brake_failure() or self.get_signal_pickup_failure():
            self.force = 0
        return round(self.force, 3)

    # acceleration calculation
    def calc_acceleration(self) -> float:
        self.acceleration = self._calculations.calc_accel(force=self.force, mass=self.get_total_mass())  # a = F/M
        # limit acceleration to max acceleration:
        if self.acceleration > self.accel_limit:
            self.acceleration = self.accel_limit
        # if there are any faults, stop the train from moving
        if self.get_engine_failure() or self.get_brake_failure() or self.get_signal_pickup_failure():
            self.acceleration = 0
        # if the brakes are pulled and the velocity = 0
        if (self.get_service_brake() or self.get_e_brake()) and self.actual_velocity == 0:
            self.acceleration = 0
        # cap the decel limits
        if self.acceleration < -2.73:
            self.acceleration = self.eBrake_decel_limit
        if -2.73 < self.acceleration < -1.2:
            self.acceleration = self.service_Brake_decel_limit
        return round(self.acceleration, 3)

    # actual velocity calculation
    def calc_actual_velocity(self) -> float:
        # v = integrate acceleration over time
        self.actual_velocity = max(self._calculations.calc_Vactaul(accel=self.acceleration), 0)
        # if there are any faults, stop the train from moving
        if self.get_engine_failure() or self.get_brake_failure() or self.get_signal_pickup_failure():
            self.actual_velocity = 0
        return round(self.actual_velocity, 3)

    # create instance of the train model UI for the launcher
    # this is the gui that has buttons to launch each individual module's UI
    def launch_tm_ui(self):
        from train_model.main_ui import Ui_MainUI
        from train_model.advertisements import ImagePopup
        self._ui = Ui_MainUI(self)
        self.ads = ImagePopup(popup_time=10)


