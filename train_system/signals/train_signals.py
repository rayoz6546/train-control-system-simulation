class TrainSignals:
    def __init__(self) -> None:
        # from train model
        self.beacon = ""  # from the track model
        self.signal_pickup_fault = False
        self.engine_fault = False
        self.brake_fault = False
        self.emergency_brake = False
        self.commanded_speed = 0  # from the track model
        self.train_speed = 0  # actual velocity
        self.authority = 0  # from the track model
        self.door = ""
        self.time = 0
        self.speed_limit = 0
        self.underground = False

        # to train model
        self.power = 0
        self.left_door = False
        self.right_door = False
        self.internal_lights = False
        self.external_lights = False
        self.service_brake = False
