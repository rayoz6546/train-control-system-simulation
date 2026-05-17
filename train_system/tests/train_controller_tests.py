import sys
import os
import unittest


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from train_system.train_controller.train_controller import TrainController
from train_system.train_controller.train_controller_manager import (
    TrainControllerManager,
)
from train_system.signals.train_signals import TrainSignals


class TrainControllerTests(unittest.TestCase):
    def test_output_power(self):
        """Train outputs power"""
        tc = TrainController(signals=None, test=True)
        tc.set_gains(1, 0)
        tc.set_commanded_speed(20)
        tc.set_authority(100)
        tc.set_speed_limit(50)
        tc._actual_speed = 15
        self.assertEqual(tc.calculate_power(), 5)
        self.assertFalse(tc.get_emergency_brake())
        self.assertFalse(tc.get_service_brake())

    def test_train_faults(self):
        """Train reacts to faults"""
        tc = TrainController(signals=None, test=True)
        tc.set_commanded_speed(20)
        tc.set_authority(100)
        tc.set_speed_limit(50)
        tc.set_brake_fault(True)
        tc.calculate_power()
        self.assertTrue(tc.get_emergency_brake())

    def test_brakes(self):
        """Emergency brake cuts power"""
        ts = TrainSignals()
        tc = TrainController(signals=ts, test=True)

        ts.train_speed = 40
        ts.commanded_speed = 45
        ts.speed_limit = 43
        ts.authority = 10
        tc.update()

        self.assertFalse(ts.emergency_brake)
        tc.set_emergency_brake(True)
        tc.update()

        self.assertTrue(ts.emergency_brake)
        self.assertEqual(ts.power, 0)
        tc.set_emergency_brake(False)
        tc.set_service_brake(True)
        tc.update()

        self.assertTrue(ts.service_brake)
        self.assertFalse(ts.emergency_brake)
        self.assertEqual(ts.power, 0)

    def test_doors(self):
        """Train driver opens doors"""
        ts = TrainSignals()
        tc = TrainController(signals=ts, test=True)
        ts.left_door = False
        ts.right_door = False
        tc.toggle_mode(True)
        tc.set_doors(True, True)
        tc.set_doors(False, True)
        self.assertTrue(tc.get_doors()[0])
        self.assertTrue(tc.get_doors()[1])
        tc.update(thread=False)
        self.assertTrue(ts.left_door)
        self.assertTrue(ts.right_door)

    def test_lights(self):
        """Train driver controls lights"""
        ts = TrainSignals()
        tc = TrainController(signals=ts, test=True)
        ts.left_door = False
        ts.right_door = False
        tc.toggle_mode(True)
        self.assertFalse(ts.internal_lights)
        self.assertFalse(ts.external_lights)
        tc.toggle_ext_lights(True)
        tc.toggle_lights(True)
        tc.update(thread=False)
        self.assertTrue(ts.internal_lights)
        self.assertTrue(ts.external_lights)

    def test_automatic_lights(self):
        """Lights on underground and at night"""
        ts = TrainSignals()
        tc = TrainController(signals=ts, test=True)
        ts.time = 43400
        tc.update(thread=False)
        self.assertFalse(ts.internal_lights)
        self.assertFalse(ts.external_lights)
        ts.underground = True
        tc.update(thread=False)
        self.assertFalse(tc.get_time_of_day())
        self.assertTrue(ts.internal_lights)
        self.assertTrue(ts.external_lights)
        ts.underground = False
        tc.update(thread=False)
        self.assertFalse(ts.internal_lights)
        self.assertFalse(ts.external_lights)
        ts.time = 86400
        tc.update(thread=False)
        self.assertTrue(ts.internal_lights)
        self.assertTrue(ts.external_lights)

    def test_manager(self):
        """Train controller exists for every train model"""
        d = {1: TrainSignals(), 2: TrainSignals()}
        m = TrainControllerManager(d, True)
        m.update(False)
        self.assertEqual(list(m.get_ids()), [1, 2])

        d[3] = TrainSignals()
        m.update(False)
        self.assertEqual(list(m.get_ids()), [1, 2, 3])

        d.pop(1)
        m.update(False)
        self.assertEqual(list(m.get_ids()), [2, 3])

    def test_station_stop(self):
        b = "STATION; WHITED"
        ts = TrainSignals()
        tc = TrainController(signals=ts, test=True)
    
        ts.commanded_speed = 43
        ts.speed_limit = 43
        ts.authority = .095
        tc.update()
        ts.beacon = b
        ts.authority = 0
        tc.update()
        self.assertEqual(tc.get_station_name(), "WHITED")
        self.assertTrue(tc.get_service_brake())
        ts.train_speed = 0
        tc.update()
        self.assertTrue(ts.left_door)
        self.assertTrue(ts.right_door)

    def test_braking_distance(self):
        """Train controller calculates service brake and emergency braking distance"""
        ts = TrainSignals()
        tc = TrainController(signals=ts, test=True)
        dist = tc.calculate_braking_dist(43)
        dist2 = tc.calculate_ebraking_dist(43)
        self.assertAlmostEqual(dist, 0.0950698, places=2)
        self.assertAlmostEqual(dist2, 0.042, places=2)

        #Test braking from authority
        ts.train_speed = 43
        ts.speed_limit = 43
        ts.authority = .095
        self.assertFalse(tc.get_service_brake())
        tc.update()
        self.assertFalse(tc.get_emergency_brake())
        self.assertTrue(tc.get_service_brake())
        ts.authority = 0
        tc.update()
        self.assertTrue(tc.get_emergency_brake())


if __name__ == "__main__":
    unittest.main()
