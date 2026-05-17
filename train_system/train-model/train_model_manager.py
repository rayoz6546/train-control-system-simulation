from .train_model import TrainModel
from signals.train_signals import TrainSignals
from signals.track_signals import TrackSignals
from signals.track_to_train_signals import TracktoTrainSignals
from typing import DefaultDict
import threading


class TrainModelManager:
    def __init__(self, train_signals, track_to_train_signals) -> None:
        self._train_models = DefaultDict(TrainModel)
        self._train_signals = train_signals
        self._track_to_train_signals = track_to_train_signals
        self.update()

    # add update function
    def update(self, thread=True):
        track_to_train_keys = set(self._track_to_train_signals.keys())
        tm_keys = set(self._train_models.keys())

        trains_to_add = track_to_train_keys - tm_keys
        trains_to_remove = tm_keys - track_to_train_keys

        for k in trains_to_add:
            self.add(self._track_to_train_signals[k], k)

        for k in trains_to_remove:
            self.remove(k)

        for train in self._train_models.values():
            train.update()

        if thread:
            threading.Timer(0.01, self.update).start()

    def add(self, track_to_train_signals: TracktoTrainSignals, id):
        if id is None:
            id = len(self._train_models) + 1
        ts = TrainSignals()
        self._train_signals[id] = ts
        self._train_models[id] = TrainModel(ts, track_to_train_signals)

    # create remove function
    def remove(self, id: int):
        self._train_models.pop(id)
        self._train_signals.pop(id)

    def get_ids(self):
        return self._train_models.keys()

    def launch_ui(self, id: int):
        # add conditions for id
        if id in self._train_models:
            self._train_models[id].launch_tm_ui()
