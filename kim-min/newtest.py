class Process:
    def __init__(self, pId, arrival, service, priority):
        self.pId = pId
        self.arrival = int(arrival)
        self.service = int(service) 
        self.priority = int(priority)
        self.result = self.Result()

    class Result:        
        def __init__(self):
            self.waiting = 0
            self.turnaround = 0
            self.response = 0
            self.end = 0 
    def print(self):
        print('pId: {}, arrival: {}, service: {}, priority: {}'.format(self.pId, self.arrival, self.service, self.priority))
        print('pId: {}, waiting: {}, turnaround: {}, response: {}, end: {}\n'.format(self.pId, self.result.waiting, self.result.turnaround, self.result.response, self.result.end))

def sum_print(process_list):
    sum_waiting = 0
    sum_turnaround = 0
    sum_response = 0
    for i in range(0, n):
        sum_waiting += process_list[i].result.waiting
        sum_turnaround += process_list[i].result.turnaround
        sum_response += process_list[i].result.response
    average_waiting = sum_waiting / n
    average_turnaround = sum_turnaround / n
    average_response = sum_response / n

    print('average waiting time = {}'.format(average_waiting))
    print('average turnaround time = {}'.format(average_turnaround))
    print('average response time = {}'.format(average_response))

def fcfs(n, process_list):

    # 정렬한 후 간트 차트 작성 / end과 response 기록
    fcfs_process_list = sorted(process_list, key=lambda Process: Process.arrival)
    counter = 0
    for i in range(0, n):
        fcfs_process_list[i].result.response = counter - fcfs_process_list[i].arrival
        for j in range(0, fcfs_process_list[i].service): 
            print(fcfs_process_list[i].pId, end = ' ')
            counter += 1
        fcfs_process_list[i].result.end = counter
    print('\n')
    
    # 각 프로세스에 대하여 waiting과 turnaround 계산 및 출력
    for i in range(0, n):
        fcfs_process_list[i].result.turnaround = fcfs_process_list[i].result.end - fcfs_process_list[i].arrival
        fcfs_process_list[i].result.waiting = fcfs_process_list[i].result.turnaround - fcfs_process_list[i].service
    for i in range(0, n):
        fcfs_process_list[i].print()

    # 평균 계산 및 출력
    sum_waiting = 0
    sum_turnaround = 0
    sum_response = 0
    for i in range(0, n):
        sum_waiting += fcfs_process_list[i].result.waiting
        sum_turnaround += fcfs_process_list[i].result.turnaround
        sum_response += fcfs_process_list[i].result.response
    average_waiting = sum_waiting / n
    average_turnaround = sum_turnaround / n
    average_response = sum_response / n

    print('average waiting time = {}'.format(average_waiting))
    print('average turnaround time = {}'.format(average_turnaround))
    print('average response time = {}'.format(average_response))

def srtf(n, process_list):
    pList = sorted(process_list, key=lambda Process: Process.arrival)

    '''
    1. 카운터에 따라 대기 큐 갱신
    2. 카운터에 따라 대기 큐 정렬, key = Process.service
    '''
    total = 0
    for process in pList:
        total += process.service
    
    waitQ = []
    endQ = []
    gantt = []

    for counter in range(total):
        # 대기 큐 업데이트
        if pList:
            if pList[0].arrival == counter:
                waitQ.append(pList[0])
                del pList[0]
        
        waitQ = sorted(waitQ, key=lambda Process : Process.service)
        waitQ[0].service -= 1
        gantt.append(waitQ[0].pId)
        if waitQ[0].service == 0:
            waitQ[0].result.end = counter + 1
            endQ.append(waitQ[0])
            del waitQ[0]
    print(''.join(gantt))    
    print()

    endQ = sorted(endQ, key=lambda Process : Process.arrival)
    for process in endQ:
        pId = process.pId
        process.service = gantt.count(pId)
        process.result.turnaround = process.result.end - process.arrival
        process.result.waiting = process.result.turnaround - process.service
        process.result.response = gantt.index(pId) - process.arrival
        process.print()
    sum_print(endQ)

def sjf(n, process_list):
    pList = sorted(process_list, key=lambda Process: Process.arrival)

    '''
    1. 카운터에 따라 대기 큐 갱신
    2. 카운터에 따라 대기 큐 정렬, key = Process.service
    '''
    total = 0
    for process in pList:
        total += process.service
    
    waitQ = []
    endQ = []
    gantt = []
    for counter in range(total):
        # 대기 큐 업데이트
        if pList:
            if pList[0].arrival == counter:
                waitQ.append(pList[0])
                del pList[0]
        
        waitQ[0].service -= 1
        gantt.append(waitQ[0].pId)
        if waitQ[0].service == 0:
            waitQ[0].result.end = counter + 1
            endQ.append(waitQ[0])
            del waitQ[0]
            waitQ = sorted(waitQ, key=lambda Process : Process.service)
    print(''.join(gantt))    
    print()

    endQ = sorted(endQ, key=lambda Process : Process.arrival)
    for process in endQ:
        pId = process.pId
        process.service = gantt.count(pId)
        process.result.turnaround = process.result.end - process.arrival
        process.result.waiting = process.result.turnaround - process.service
        process.result.response = gantt.index(pId) - process.arrival
        process.print()
    sum_print(endQ)

def rr(n, process_list, time_quantum):
    quantum = time_quantum
    pList = sorted(process_list, key=lambda Process: Process.arrival)

    '''
    1. 카운터에 따라 대기 큐 갱신
    2. 카운터에 따라 대기 큐 정렬, key = Process.service
    '''
    total = 0
    for process in pList:
        total += process.service
    
    waitQ = []
    endQ = []
    gantt = []

    if pList:
        if pList[0].arrival == 0:
            waitQ.append(pList[0])
            del pList[0]

    for counter in range(total):
        # 연산 시작
        waitQ[0].service -= 1
        quantum -= 1
        gantt.append(waitQ[0].pId)
        # 연산 끝

        # waiting queue 업데이트: new arrival
        if pList:
            if pList[0].arrival == counter + 1:
                waitQ.append(pList[0])
                del pList[0]

        # waiting queue 업데이트: 끝난 process 뒤로
        if waitQ[0].service == 0:
            waitQ[0].result.end = counter + 1
            endQ.append(waitQ[0])
            del waitQ[0]

            if quantum == 0:
                quantum = 2
        else:                
            if quantum == 0:
                quantum = 2
                waitQ.append(waitQ[0])
                del waitQ[0]

    print(''.join(gantt))    
    print()

    endQ = sorted(endQ, key=lambda Process : Process.arrival)
    for process in endQ:
        pId = process.pId
        process.service = gantt.count(pId)
        process.result.turnaround = process.result.end - process.arrival
        process.result.waiting = process.result.turnaround - process.service
        process.result.response = gantt.index(pId) - process.arrival
        process.print()
    sum_print(endQ)

def nonpreemptive_priority(n, process_list):
    pList = sorted(process_list, key=lambda Process: Process.arrival)
    total = 0
    for process in pList:
        total += process.service
    
    waitQ = []
    endQ = []
    gantt = []

    # arrival time == 0인 process를 waiting queue에 올림
    if pList[0].arrival == 0:
        waitQ.append(pList[0])
        del pList[0]

    for counter in range(total):
        # 연산 시작
        waitQ[0].service -= 1
        gantt.append(waitQ[0].pId)
        # 연산 끝

        # 다음 waiting queue 업데이트
        if pList:
            if pList[0].arrival == counter:
                waitQ.append(pList[0])
                del pList[0]
        
        # 아까 연산했던 process 처리: 삭제 or 뒤로
        if waitQ[0].service == 0:
            waitQ[0].result.end = counter + 1
            endQ.append(waitQ[0])
            del waitQ[0]
            waitQ = sorted(waitQ, key=lambda Process : Process.priority)
    print(''.join(gantt))    
    print()

    endQ = sorted(endQ, key=lambda Process : Process.arrival)
    for process in endQ:
        pId = process.pId
        process.service = gantt.count(pId)
        process.result.turnaround = process.result.end - process.arrival
        process.result.waiting = process.result.turnaround - process.service
        process.result.response = gantt.index(pId) - process.arrival
        process.print()
    sum_print(endQ)

def preemptive_priority(n, process_list):
    pList = sorted(process_list, key=lambda Process: Process.arrival)

    '''
    1. 카운터에 따라 대기 큐 갱신
    2. 카운터에 따라 대기 큐 정렬, key = Process.service
    '''
    total = 0
    for process in pList:
        total += process.service
    
    waitQ = []
    endQ = []
    gantt = []

    if pList[0].arrival == 0:
        waitQ.append(pList[0])
        del pList[0]

    for counter in range(total):
        waitQ[0].service -= 1
        gantt.append(waitQ[0].pId)

        if pList:
            if pList[0].arrival == counter + 1:
                waitQ.append(pList[0])
                del pList[0]

        if waitQ[0].service == 0:
            waitQ[0].result.end = counter + 1
            endQ.append(waitQ[0])
            del waitQ[0]
        waitQ = sorted(waitQ, key=lambda Process : Process.priority)
    print(''.join(gantt))    
    print()

    endQ = sorted(endQ, key=lambda Process : Process.arrival)
    for process in endQ:
        pId = process.pId
        process.service = gantt.count(pId)
        process.result.turnaround = process.result.end - process.arrival
        process.result.waiting = process.result.turnaround - process.service
        process.result.response = gantt.index(pId) - process.arrival
        process.print()
    sum_print(endQ)

def nonpreemptive_priority_with_RR(n, process_list, time_quantum):
    quantum = time_quantum
    pList = sorted(process_list, key=lambda Process: Process.arrival)

    '''
    1. 카운터에 따라 대기 큐 갱신
    2. 카운터에 따라 대기 큐 정렬, key = Process.service
    '''
    total = 0
    for process in pList:
        total += process.service
    
    waitQ = []
    endQ = []
    gantt = []

    if pList[0].arrival == 0:
        waitQ.append(pList[0])
        del pList[0]

    for counter in range(total):
        # 연산 시작
        waitQ[0].service -= 1
        quantum -= 1
        gantt.append(waitQ[0].pId)
        # 연산 끝

        # waiting queue 업데이트: new arrival
        if pList:
            if pList[0].arrival == counter + 1:
                waitQ.append(pList[0])
                del pList[0]

        # waiting queue 업데이트: 끝난 process 뒤로
        if waitQ[0].service == 0:
            waitQ[0].result.end = counter + 1
            endQ.append(waitQ[0])
            del waitQ[0]

            if quantum == 0:
                quantum = 2
                waitQ = sorted(waitQ, key=lambda Process : Process.priority)
        else:                
            if quantum == 0:
                quantum = 2
                waitQ.append(waitQ[0])
                del waitQ[0]
                waitQ = sorted(waitQ, key=lambda Process : Process.priority)
        

    print(''.join(gantt))    
    print()

    endQ = sorted(endQ, key=lambda Process : Process.arrival)
    for process in endQ:
        pId = process.pId
        process.service = gantt.count(pId)
        process.result.turnaround = process.result.end - process.arrival
        process.result.waiting = process.result.turnaround - process.service
        process.result.response = gantt.index(pId) - process.arrival
        process.print()
    sum_print(endQ)

# 메인
n = int(input())
process_list = []
for i in range(0, n):
    pId, arrival, service, priority = input().split() 
    process_list.append(Process(pId, arrival, service, priority))
time_quantum = int(input())
print(' ')

# fcfs(n, process_list)
# sjf((n, process_list)
# srtf(n, process_list)
# rr(n, process_list, time_quantum)
# nonpreemptive_priority(n, process_list)
# preemptive_priority(n, process_list)
nonpreemptive_priority_with_RR(n, process_list, time_quantum)