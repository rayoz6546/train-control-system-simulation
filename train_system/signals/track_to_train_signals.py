class TracktoTrainSignals:
    def __init__(self) -> None:
        # train model
        self.passenger_mass = 0  # don't think we need this since train model calculates it
        self.passenger_count = 0  #how many people on each train
        self.passengers_departing = 0

        # get actual speed from train model to calc train occupanc?
        self.actual_velocity = 0.0
        self.signal_pickup_fault = False
        
        #outputs    
        self.lineChoice = '' #will be str blue, green, red
        self.track_grade_elev_blue = {} #dict key = block number, value is tuple of (grade, elevation), TODO add underground 
        self.track_speedLim_stat_blue = {}#dict key = block number, value is tuple of (speed limit, , station side:str)
        self.track_grade_elev_green = {} 
        self.track_speedLim_stat_green = {}
        self.track_grade_elev_red = {} 
        self.track_speedLim_stat_red = {}

        self.beacon = ""
        self.authority_fromTrack = 0
        self.commandedSpeed = 0
        self.currentBlock = 0
        self.time = 0