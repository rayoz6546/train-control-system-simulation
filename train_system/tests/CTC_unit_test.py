import sys
import os
import unittest


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from train_system.CTC.ctc import CTC
from train_system.signals.trackcontroller_signals import TrackCTCSignals



class TestCTC(unittest.TestCase):

    #set the authority for a new train
    def test_authority(self):
        ctc = CTC(signals=None, test = True)
        ctc.addTrain(73, 30, "Green")
        ctc.calcAuthority()
        assert ctc.trainList[0].authority == "G76", "Wrong authority for train being added to system"

    #suggested speed
    def test_suggested_speed(self):
        ctc = CTC(signals=None, test=True)
        ctc.addTrain(73, 30, "Green")
        ctc.calcAuthority()
        ctc.calcSuggestedSpeed()

        assert ctc.trainList[0].suggested_speed == 50, "Wrong speed for train being added to system"

    #set block for maintenance
    def test_maintenance(self):
        signal3 = TrackCTCSignals()
        ctc = CTC(signals=signal3, test=True)
        ctc.addTrain(77, 30, "Green")
        ctc.trainList[0].location == "76"

        ctc.calcAuthority()
        ctc.calcSuggestedSpeed()
        ctc.editTrack(2, 66, 0)

        assert ctc.maintenance[2][66] == 1, "Wrong maintenance value"


    #set maintenance and check speed and auth
    def test_auth_speed_maintenance(self):
        signal3 = TrackCTCSignals()
        ctc = CTC(signals=signal3, test=True)
        ctc.addTrain(77, 30, "Green")
        ctc.calcAuthority()
        ctc.calcSuggestedSpeed()
        assert ctc.trainList[0].authority == "G76", "Wrong auth for train being added to system"
        assert ctc.trainList[0].suggested_speed == 50, "Wrong speed for train being added to system"

        ctc.editTrack(2, 66, 0)

        ctc.calcAuthority()
        ctc.calcSuggestedSpeed()
        assert ctc.trainList[0].authority == "G63", "Wrong auth for train being added to system"
        assert ctc.trainList[0].suggested_speed == 0.0, "Wrong speed for train being added to system"

    #can set switch while in maintenance mode
    def test_switch_set(self):
        signal3 = TrackCTCSignals()
        ctc = CTC(signals=signal3, test=True)
        ctc.setSwitch("Left", 78, "Green")
        assert len(ctc.signals.switch_changes_green) == 0, "Switch Changed"
        ctc.editTrack(2, 77, 0)
        ctc.setSwitch("Left", 78, "Green")
        assert ctc.signals.switch_changes_green[0] == [78, False], "Switch not changed"

if __name__ == '__main__':
    unittest.main()
