from .train_controller import TrainController
from typing import DefaultDict, Dict
import threading


class TrainControllerManager:
    """Manager class for train controllers"""

    def __init__(self, train_signals, test: bool = False) -> None:
        self._train_controllers = DefaultDict(TrainController)
        self._train_signals = train_signals
        if not test:
            self.update()

    def update(self, thread: bool = True):
        """Runs every 10ms"""
        ts_keys = set(self._train_signals.keys())
        tc_keys = set(self._train_controllers.keys())

        trains_to_add = ts_keys - tc_keys
        trains_to_remove = tc_keys - ts_keys

        for k in trains_to_add:
            self.add(self._train_signals[k], k)

        for k in trains_to_remove:
            self.remove(k)

        for train in self._train_controllers.values():
            train.update()

        if thread:
            threading.Timer(0.01, self.update).start()

    def add(self, signals, i: int = None):
        """Add new train controller"""
        if i is None:
            i = len(self._train_controllers) + 1
        self._train_controllers[i] = TrainController(signals=signals)

    def remove(self, i: int):
        """Remove a train controller"""
        self._train_controllers.pop(i)

    def get_ids(self):
        """Get id's of existing train controllers"""
        return self._train_controllers.keys()

    def launch_ui(self, i: int):
        """Launch given train controller's ui"""
        if i in self._train_controllers:
            self._train_controllers[i].launch_driver_ui()
            self._train_controllers[i].launch_engineer_ui()
