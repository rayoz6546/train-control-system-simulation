import sys, os
import time
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from train_system.track_model.track_model import TrackModel
from train_system.track_model.file_handler import FileHandler
from signals.track_signals import TrackSignals
from train_system.track_model.track_model_ui import TrackModelMainUI

class tests(unittest.TestCase):
    def test_setget_greenline(self):
        sigs = TrackSignals()
        tm = TrackModel(sigs)
        green = {0 : [1, 2, 'testing', 'yay', 'ahhhh', ':)', ':(', ':D', ':P']}
        tm.setGreenLine(green)

        greenTest = tm.greenLine_set
        
        self.assertEqual(green, greenTest)
        print("getting and setting red line good :D")

    def test_setget_redline(self):
        sigs = TrackSignals()
        tm = TrackModel(sigs)
        red = {0 : [1, 2, 'testing', 'yay', 'ahhhh', ':)', ':(', ':D', ':P']}
        tm.setRedLine(red)

        redTest = tm.redLine_set
        
        self.assertEqual(red, redTest)
        print("getting and setting red line good :D")

    def test_Power_failure_green(self):
        sigs = TrackSignals()
        tm = TrackModel(sigs)
        block = 33
        broken = 1
        tm.setPowerFailure_green( block, broken)
        powerFails = sigs.powerFailure_green

        self.assertEqual(powerFails[block], broken)
        print("getting and setting power fail green line good! :D")

    def test_circuit_failure_green(self):
        """testing setting circuit failure, and being sent to track controller"""
        sigs = TrackSignals()
        tm = TrackModel(sigs)
        block = 33
        broken = 1
        tm.setCircuitFailure_green( block, broken)
        
        circuit_fails = sigs.circuitFailure_green

        self.assertEqual(circuit_fails[block], broken)
        print("getting and setting circuit fail green line good! :D")

    def test_broken_rail_green(self):
        """testing green line broken rail is being set and sent to track controller"""
        sigs = TrackSignals()
        tm = TrackModel(sigs)
        block = 33
        broken = 1
        tm.setBrokenRail_green( block, broken)
        powerFails = sigs.brokenRail_green

        self.assertEqual(powerFails[block], broken)
        print("getting and setting rail fail green line good! :D")

    def test_power_failure_red(self):
        """test setting and sending power failure to track controller"""
        sigs = TrackSignals()
        tm = TrackModel(sigs)
        block = 33
        broken = 1
        tm.setPowerFailure_red( block, broken)
        powerFails = sigs.powerFailure_red

        self.assertEqual(powerFails[block], broken)
        print("getting and setting power fail red line good! :D")

    def test_circuit_failure_red(self):
        """testing setting circuit failure, and being sent to track controller"""
        sigs = TrackSignals()
        tm = TrackModel(sigs)
        block = 33
        broken = 1
        tm.setCircuitFailure_red( block, broken)
        
        circuit_fails = sigs.circuitFailure_red

        self.assertEqual(circuit_fails[block], broken)
        print("getting and setting circuit fail red line good! :D")

    def test_broken_rail_red(self):
        """testing red line broken rail is being set and sent to track controller"""
        sigs = TrackSignals()
        tm = TrackModel(sigs)
        block = 33
        broken = 1
        tm.setBrokenRail_red( block, broken)
        powerFails = sigs.brokenRail_red

        self.assertEqual(powerFails[block], broken)
        print("getting and setting rail fail red line good! :D")

        
    def test_commandedSpeed(self):
        """test commanded speed is being sent and received correctly"""
        sigs = TrackSignals()
        tm = TrackModel(sigs)

        testSpeed = 45
        tm.setCommandedSpeed(testSpeed)

        speed = tm.commandedSpeed

        self.assertEqual(speed, testSpeed)
        print("commanded speed set and sent correctly")
    
    def test_red_switches(self):
        """test set and get red line switches"""
        sigs = TrackSignals()
        tm = TrackModel(sigs)
        
        switch = 27
        pos = 1

        tm.set_RedSwitch(switch, pos)
        switchPos = tm.redSwitches_set[27]
        self.assertEqual(switchPos, pos)

        switch = 27
        pos = 0

        tm.set_RedSwitch(switch, pos)
        switchPos = tm.redSwitches_set[27]
        self.assertEqual(switchPos, pos)

    def test_green_switches(self):
        """test set and get red line switches"""
        sigs = TrackSignals()
        tm = TrackModel(sigs)
        
        switch = 27
        pos = 1

        tm.set_GreenSwitch(switch, pos)
        switchPos = tm.greenSwitches_set[27]
        self.assertEqual(switchPos, pos)

        switch = 27
        pos = 0

        tm.set_GreenSwitch(switch, pos)
        switchPos = tm.greenSwitches_set[27]
        self.assertEqual(switchPos, pos)
    


if __name__ == '__main__':
    unittest.main()
