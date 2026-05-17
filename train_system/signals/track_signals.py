class TrackSignals:
    def __init__(self) -> None:
        #inputs
        self.switchPos = 0      #from track controller
        self.crossings = 0
        self.commandedSpeed = 0
        self.authority_fromWayside = "" #FIXME authority will be sent to specific signals class instantiated from specific train model
        self.lights = 0
        self.redSwitches_set = {}
        self.blueSwitches_set = {}
        self.greenSwitches_set = {}
        self.time = 0 #formate seconds passed
        self.currentSpeed = 0 #FIXME needed?
        self.lights_blue = [[None]*3,[None]*3,[None]*3] #green, yellow, red (block 5, block 6, block 11)
        
        self.train_info = {}  #key = train #, [0]auth [1]sug speed [2]route [3]location [4] passenger info 
    
        # train model
        self.passenger_mass = 0  # don't think we need this since train model calculates it
        self.passenger_count = 0  #how many people on each train
        self.passengers_departing = 0

        # get actual speed from train model to calc train occupanc?
        self.actual_velocity = 0.0
        self.signal_pickup_fault = False

        #outputs    
        self.signals_trackToTrain = {} #dict key train num, value is signal class track_to_train_signals instance


        self.lineChoice = '' #will be str blue, green, red
        self.track_grade_elev_blue = {} #dict key = block number, value is tuple of (grade, elevation), TODO add underground 
        self.track_speedLim_stat_blue = {}#dict key = block number, value is tuple of (speed limit, , station side:str)
        self.track_grade_elev_green = {} 
        self.track_speedLim_stat_green = {}
        self.track_grade_elev_red = {} 
        self.track_speedLim_stat_red = {}

        #TODO make beacon with switch/station/name
        self.trackLayout = {}
        self.redLine_set = {}  #note list: Block Number [0],Block Length (m) [1],Block Grade (%) [2],Speed Limit (Km/Hr)[3],Infrastructure [4],station side [5], ELEVATION (M) [6],CUMALTIVE ELEVATION (M) [7]
        self.greenLine_set = {}
        self.blueLine_set = {}

        self.brokenRail_blue = [0] *15
        self.circuitFailure_blue = [0] * 15
        self.powerFailure_blue = [0] *15 #index is block number, 0 = no fail, 1 = fail
        self.brokenRail_green = [0] *150
        self.circuitFailure_green = [0] * 150
        self.powerFailure_green = [0] *150
        self.brokenRail_red = [0] *76
        self.circuitFailure_red = [0] * 76
        self.powerFailure_red = [0] * 76

        self.blueLineOccupancy = [0] * 15 #index is block number, 0 is not occupied, 1 is occupied
        self.greenLineOccupancy = [0] * 150
        self.redLineOccupancy = [0] * 76

        self.authority_fromTrack = 0
        self.beacon = "" 
        self.commandedSpeed = 0
        self.currentBlock = 0
        self.ticketSales = [0, 0, 0] #list of ticket sales per line, 0:blue, 1:green, 2:red


        # traffic lights from track controller

        self.traffic_lights_green = {}   # example: {63:[False,True,False]} ==> yellow lights on block 63 (index0 in list--> green, index1-->yellow, index2-->red)
        self.switch_positions_green = {}  # example: {63: True} ==> switch on block 63 is right
        self.traffic_lights_red = {}   
        self.switch_positions_red = {}  
