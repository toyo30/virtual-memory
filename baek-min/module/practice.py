class Process:
    def __init__(self, pId, arrival_time, service_time, priority):
        self.pId = pId
        self.arrival_time = arrival_time
        self.service_time = int(service_time)
        self.priority = int(priority)
        self.result = self.Result()
    class Result:
        def __init__(self):
            self.waiting = 0
            self.turnaround = 0
            self.response = 0
    
    # def outer_disp(self):
    #     self.inner.inner_disp(self.pId)
    
    
        # def inner_disp(self,details):
        #     print(details, "From Inner Class") 


P0 = Process('P0', '5', '6', '2')

print(P0.result.waiting)