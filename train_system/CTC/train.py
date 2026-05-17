
class Train():
    def __init__(self):
        #train info
        self.completed = 0
        self.prevBlock = 0
        self.route = [] #list containing the block numbers in the order of traversal
        self.authority = "" # first index = line (R,G,B) next index = block #(1-16)
        self.line = ""
        self.destinationList = []
        self.suggested_speed = 0
        self.train_id = 0
        self.arrival_time = "" #hour:min:second
        self.destination = 0 #station letter/name
        self.passengers = 0
        self.location = int(63) #block number #indicates the train is starting in the yard

    def update(self, type: int):
        self.type = type

    def setMode(self, type: int):
        self.mode = type

    def setAuthority(self, auth: str):
        self.authority = auth

    def setSuggestedSpeed(self, speed: int):
        self.speed = speed

    def setTrainID(self, id: int):
        self.train_id = id

    def setArrival_time(self, time: str):
        self.arrival_time = time

    def setDestination(self, destination: int):
        self.destination = destination
