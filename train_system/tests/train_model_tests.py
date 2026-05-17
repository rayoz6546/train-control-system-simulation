import sys
import os
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from train_system.train_model.train_model import TrainModel
from train_system.signals.train_signals import TrainSignals
from train_system.signals.track_signals import TrackSignals

class TrainModelUnitTests(unittest.TestCase):

    def test_brake_failure(self):
        train_sigs = TrainSignals()
        track_sigs = TrackSignals()
        tm = TrainModel(train_signals=train_sigs, track_signals=track_sigs)
        tm.set_brake_failure(1)
        self.assertTrue(tm.get_brake_failure())

    def test_force_calc(self):
        train_sigs = TrainSignals()
        track_sigs = TrackSignals()
        tm = TrainModel(train_signals=train_sigs, track_signals=track_sigs)
        # when v = 0 and on flat road
        tm.set_cmd_power(3000)
        tm.set_current_passenger_count(0)
        tm.set_elevation(0)
        tm.set_grade(0)
        tm.set_actual_velocity(0)
        tm.set_engine_failure(False)
        tm.set_signal_pickup_failure(False)
        tm.set_brake_failure(False)
        self.assertEqual(tm.calc_Force(), 122.7)  # force = total mass * (accel or decel limit) * friction coefficient
        # when v ! = 0 but on flat road
        tm.set_cmd_power(3000)
        tm.set_current_passenger_count(10)
        tm.set_elevation(0)
        tm.set_grade(0)
        tm.set_actual_velocity(20)
        tm.set_engine_failure(False)
        tm.set_signal_pickup_failure(False)
        tm.set_brake_failure(False)
        self.assertEqual(tm.calc_Force(), -99.482)  # force = P/v
        # when grade > 0 and elevation != 0
        tm.set_elevation(16)
        tm.set_grade(0.5)
        tm.set_actual_velocity(20)
        self.assertEqual(tm.calc_Force(), -700.909)  # force = -net force + (P/v), net force = mgsin(theta) - (f * mgcos(theta))
        # when grade < 0 and elevation != 0
        tm.set_elevation(16)
        tm.set_grade(-0.5)
        tm.set_actual_velocity(20)
        self.assertEqual(tm.calc_Force(), 5890.603)  # force = net force + (P/v), net force = mgsin(theta) - (f * mgcos(theta))
        # when there is a failure
        tm.set_engine_failure(True)
        self.assertEqual(tm.calc_Force(), 0)
        tm.set_signal_pickup_failure(True)
        self.assertEqual(tm.calc_Force(), 0)
        tm.set_brake_failure(True)
        self.assertEqual(tm.calc_Force(), 0)  # train should stop moving if there's a failure

    def test_acceleration_calc(self):
        train_sigs = TrainSignals()
        track_sigs = TrackSignals()
        tm = TrainModel(train_signals=train_sigs, track_signals=track_sigs)
        tm.set_current_passenger_count(10)
        tm.set_force(200)
        tm.set_engine_failure(False)
        tm.set_signal_pickup_failure(False)
        tm.set_brake_failure(False)
        tm.set_service_brake(False)
        tm.set_e_brake(False)
        # test accel calculation normally
        self.assertEqual(tm.calc_acceleration(), 0.005)

    def test_failure_modes(self):
        train_sigs = TrainSignals()
        track_sigs = TrackSignals()
        tm = TrainModel(train_signals=train_sigs, track_signals=track_sigs)
        # test for failure modes
        tm.set_engine_failure(True)
        self.assertEqual(tm.calc_acceleration(), 0)
        tm.set_signal_pickup_failure(True)
        self.assertEqual(tm.calc_acceleration(), 0)
        tm.set_brake_failure(True)
        self.assertEqual(tm.calc_acceleration(), 0)  # train should stop moving if there's a failure

    def test_service_decel_limits(self):
        train_sigs = TrainSignals()
        track_sigs = TrackSignals()
        tm = TrainModel(train_signals=train_sigs, track_signals=track_sigs)
        tm.set_current_passenger_count(10)
        tm.set_force(-50000)
        self.assertEqual(tm.calc_acceleration(), -1.2)

    def test_e_brake_decel_limits(self):
        train_sigs = TrainSignals()
        track_sigs = TrackSignals()
        tm = TrainModel(train_signals=train_sigs, track_signals=track_sigs)
        tm.set_current_passenger_count(10)
        tm.set_force(-200000)
        self.assertEqual(tm.calc_acceleration(), -2.73)

    def test_accel_limits(self):
        train_sigs = TrainSignals()
        track_sigs = TrackSignals()
        tm = TrainModel(train_signals=train_sigs, track_signals=track_sigs)
        # if acceleration > accel limit, cap it at the max accel rate
        tm.set_current_passenger_count(100)
        tm.set_force(65000)
        self.assertEqual(tm.calc_acceleration(), 0.5)

    def test_actual_velocity_calc(self):
        train_sigs = TrainSignals()
        track_sigs = TrackSignals()
        tm = TrainModel(train_signals=train_sigs, track_signals=track_sigs)
        # test for failure modes
        tm.set_engine_failure(True)
        self.assertEqual(tm.calc_actual_velocity(), 0)
        tm.set_signal_pickup_failure(True)
        self.assertEqual(tm.calc_actual_velocity(), 0)
        tm.set_brake_failure(True)
        self.assertEqual(tm.calc_actual_velocity(), 0)  # train should stop moving if there's a failure


if __name__ == "__main__":
    unittest.main()



