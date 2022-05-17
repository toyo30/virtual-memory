import copy

class Process:
    def __init__(self, pId, arrival, service, priority):
        self.pId = pId
        self.arrival = int(arrival)
        self.service = int(service)
        self.remaining_service = int(service)
        self.priority = int(priority)
        self.result = self.Result()

    class Result:        
        def __init__(self):
            self.waiting = 0
            self.turnaround = 0
            self.response = 0
            self.end = 0         

def print_result(process_list, gantt):
    process_list = sorted(process_list, key=lambda Process : Process.arrival)
    print(''.join(gantt))
    print()

    for process in process_list:
        print('pId: {}, arrival: {}, service: {}, priority: {}'.format(process.pId, process.arrival, process.service, process.priority))
        print('pId: {}, waiting: {}, turnaround: {}, response: {}, end: {}\n'.format(process.pId, process.result.waiting, process.result.turnaround, process.result.response, process.result.end))

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
    print()

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

def sjf(process_list):
    not_arrived = copy.deepcopy(process_list)
    ready, end, gantt = [], [], []
    counter = 0
    # arrival time == 0인 process를 ready queue에 추가
    if not_arrived[0].arrival == 0:
        ready.append(not_arrived.pop(0))

    while True:
        # 모든 process 실행 완료
        if not ready and not not_arrived:
            break
        
        # idle task: not_arrived에는 아직 process가 있지만, ready queue는 비어있는 상태
        if not ready and not_arrived:
            if not_arrived[0].arrival == counter + 1:
                ready.append(not_arrived.pop(0))
            gantt.append(' ')
            counter += 1
        
        # 실행
        if ready: 
            current = ready[0] # 지금 실행할 프로세스 
            if current.remaining_service == current.service: # response time
                current.result.response = counter - current.arrival

            current.remaining_service -= 1
            gantt.append(current.pId)

            # new arrival 확인
            if not_arrived:
                if not_arrived[0].arrival == counter + 1:
                    ready.append(not_arrived.pop(0)) 

            # 현재 process 삭제 여부 결정, result 연산
            if current.remaining_service == 0:
                current.result.end = counter + 1 # end
                current.result.turnaround = current.result.end - current.arrival # turnaround
                current.result.waiting = current.result.turnaround - current.service # waiting
                end.append(ready.pop(0))
                ready = sorted(ready, key=lambda Process : Process.service) # 삭제할 때만 재정렬
            counter += 1
    # 결과
    print_result(end, gantt)

def srtf(process_list):
    not_arrived = copy.deepcopy(process_list)
    ready, end, gantt = [], [], []
    counter = 0
    # arrival time == 0인 process를 ready queue에 추가
    if not_arrived[0].arrival == 0:
        ready.append(not_arrived.pop(0))

    while True:
        # 모든 process 실행 완료
        if not ready and not not_arrived:
            break
        
        # idle task: not_arrived에는 아직 process가 있지만, ready queue는 비어있는 상태
        if not ready and not_arrived:
            if not_arrived[0].arrival == counter + 1:
                ready.append(not_arrived.pop(0))
            gantt.append(' ')
            counter += 1

        # 실행
        if ready: 
            current = ready[0] # 지금 실행할 프로세스 
            if current.remaining_service == current.service: # response time
                current.result.response = counter - current.arrival

            current.remaining_service -= 1
            gantt.append(current.pId)

            # new arrival 확인
            if not_arrived:
                if not_arrived[0].arrival == counter + 1:
                    ready.append(not_arrived.pop(0)) 

            # 현재 process 삭제 여부 결정, result 연산
            if current.remaining_service == 0:
                current.result.end = counter + 1 # end
                current.result.turnaround = current.result.end - current.arrival # turnaround
                current.result.waiting = current.result.turnaround - current.service # waiting
                end.append(ready.pop(0))

            # ready queue를 남은 remaining_service time으로 정렬
            ready = sorted(ready, key=lambda Process : Process.remaining_service)
            counter += 1

    print_result(end, gantt)

def rr(process_list):
    not_arrived = copy.deepcopy(process_list)
    ready, end, gantt = [], [], []
    quantum = time_quantum
    counter = 0
    # arrival time == 0인 process를 ready queue에 추가
    if not_arrived[0].arrival == 0:
        ready.append(not_arrived.pop(0))

    while True:
        # 모든 process 실행 완료
        if not ready and not not_arrived:
            break
        
        # idle task: not_arrived에는 아직 process가 있지만, ready queue는 비어있는 상태
        if not ready and not_arrived:
            if not_arrived[0].arrival == counter + 1:
                ready.append(not_arrived.pop(0))
            gantt.append(' ')
            counter += 1
        
        # 실행
        if ready: 
            current = ready[0] # 지금 실행할 프로세스 
            if current.remaining_service == current.service: # response time
                current.result.response = counter - current.arrival

            current.remaining_service -= 1
            gantt.append(current.pId)
            quantum -= 1

            # new arrival 확인
            if not_arrived:
                if not_arrived[0].arrival == counter + 1:
                    ready.append(not_arrived.pop(0)) 

            # 현재 process 삭제 여부 결정, result 연산
            if current.remaining_service == 0:
                current.result.end = counter + 1 # end
                current.result.turnaround = current.result.end - current.arrival # turnaround
                current.result.waiting = current.result.turnaround - current.service # waiting
                end.append(ready.pop(0))
                if quantum == 0:
                    quantum = time_quantum
            else:                
                if quantum == 0:
                    quantum = time_quantum
                    ready.append(ready.pop(0))
            counter += 1
    # 결과
    print_result(end, gantt)

def nonpreemptive_priority(process_list):
    not_arrived = copy.deepcopy(process_list)
    ready, end, gantt = [], [], []
    counter = 0
    # arrival time == 0인 process를 ready queue에 추가
    if not_arrived[0].arrival == 0:
        ready.append(not_arrived.pop(0))

    while True:
        # 모든 process 실행 완료
        if not ready and not not_arrived:
            break
        
        # idle task: not_arrived에는 아직 process가 있지만, ready queue는 비어있는 상태
        if not ready and not_arrived:
            if not_arrived[0].arrival == counter + 1:
                ready.append(not_arrived.pop(0))
            gantt.append(' ')
            counter += 1
        
        # 실행
        if ready: 
            current = ready[0] # 지금 실행할 프로세스 
            if current.remaining_service == current.service: # response time
                current.result.response = counter - current.arrival

            current.remaining_service -= 1
            gantt.append(current.pId)

            # new arrival 확인
            if not_arrived:
                if not_arrived[0].arrival == counter + 1:
                    ready.append(not_arrived.pop(0))
        
            # 현재 process 삭제 여부 결정, result 연산
            if current.remaining_service == 0:
                current.result.end = counter + 1 # end
                current.result.turnaround = current.result.end - current.arrival # turnaround
                current.result.waiting = current.result.turnaround - current.service # waiting
                end.append(ready.pop(0))
                # 삭제할 때만 재정렬
                ready = sorted(ready, key=lambda Process : Process.priority)
            counter += 1
    # 결과
    print_result(end, gantt)

def preemptive_priority(process_list):
    not_arrived = copy.deepcopy(process_list)
    ready, end, gantt = [], [], []
    counter = 0
    # arrival time == 0인 process를 ready queue에 추가
    if not_arrived[0].arrival == 0:
        ready.append(not_arrived.pop(0))

    while True:
        # 모든 process 실행 완료
        if not ready and not not_arrived:
            break
        
        # idle task: not_arrived에는 아직 process가 있지만, ready queue는 비어있는 상태
        if not ready and not_arrived:
            if not_arrived[0].arrival == counter + 1:
                ready.append(not_arrived.pop(0))
            gantt.append(' ')
            counter += 1
        
        # 실행
        if ready: 
            current = ready[0] # 지금 실행할 프로세스 
            if current.remaining_service == current.service: # response time
                current.result.response = counter - current.arrival

            current.remaining_service -= 1
            gantt.append(current.pId)

            # new arrival 확인
            if not_arrived:
                if not_arrived[0].arrival == counter + 1:
                    ready.append(not_arrived.pop(0))

        
            # 현재 process 삭제 여부 결정, result 연산
            if current.remaining_service == 0:
                current.result.end = counter + 1 # end
                current.result.turnaround = current.result.end - current.arrival # turnaround
                current.result.waiting = current.result.turnaround - current.service # waiting
                end.append(ready.pop(0))

            # 매 iteration마다 priority 기준으로 정렬
            ready = sorted(ready, key=lambda Process : Process.priority)
            counter += 1
    # 결과
    print_result(end, gantt)

def nonpreemptive_priority_with_RR(process_list):
    not_arrived = copy.deepcopy(process_list)
    ready, end, gantt = [], [], []
    quantum = time_quantum
    counter = 0
    # arrival time == 0인 process를 ready queue에 추가
    if not_arrived[0].arrival == 0:
        ready.append(not_arrived.pop(0))

    while True:
        # 모든 process 실행 완료
        if not ready and not not_arrived:
            break
        
        # idle task: not_arrived에는 아직 process가 있지만, ready queue는 비어있는 상태
        if not ready and not_arrived:
            if not_arrived[0].arrival == counter + 1:
                ready.append(not_arrived.pop(0))
            gantt.append(' ')
            counter += 1
        
        # 실행
        if ready: 
            current = ready[0] # 지금 실행할 프로세스 
            if current.remaining_service == current.service: # response time
                current.result.response = counter - current.arrival

            current.remaining_service -= 1
            gantt.append(current.pId)
            quantum -= 1

            # new arrival 확인
            if not_arrived:
                if not_arrived[0].arrival == counter + 1:
                    ready.append(not_arrived.pop(0))

            # 현재 process 삭제 여부 결정, result 연산
            if current.remaining_service == 0:
                current.result.end = counter + 1 # end
                current.result.turnaround = current.result.end - current.arrival # turnaround
                current.result.waiting = current.result.turnaround - current.service # waiting
                end.append(ready.pop(0))
                if quantum == 0:
                    quantum = time_quantum
                    ready = sorted(ready, key=lambda Process : Process.priority) # 재정렬
            else:
                # 뒤로 보내기
                if quantum == 0:
                    quantum = time_quantum
                    ready.append(ready.pop(0))
                    ready = sorted(ready, key=lambda Process : Process.priority) # 재정렬
            counter += 1
    # 결과
    print_result(end, gantt)

def preemptive_priority_with_RR(process_list):
    not_arrived = copy.deepcopy(process_list)
    ready, end, gantt = [], [], []
    quantum = time_quantum
    counter = 0
    # arrival time == 0인 process를 ready queue에 추가
    if not_arrived[0].arrival == 0:
        ready.append(not_arrived.pop(0))

    while True:
        # 모든 process 실행 완료
        if not ready and not not_arrived:
            break
        
        # idle task: not_arrived에는 아직 process가 있지만, ready queue는 비어있는 상태
        if not ready and not_arrived:
            if not_arrived[0].arrival == counter + 1:
                ready.append(not_arrived.pop(0))
            gantt.append(' ')
            counter += 1
        
        # 실행
        if ready: 
            current = ready[0] # 지금 실행할 프로세스 
            if current.remaining_service == current.service: # response time
                current.result.response = counter - current.arrival

            current.remaining_service -= 1
            gantt.append(current.pId)
            quantum -= 1
            
            # new arrival 확인
            if not_arrived:
                if not_arrived[0].arrival == counter + 1:
                    ready.append(not_arrived.pop(0))

            # 현재 process 삭제 여부 결정, result 연산
            if current.remaining_service == 0:
                current.result.end = counter + 1 # end
                current.result.turnaround = current.result.end - current.arrival # turnaround
                current.result.waiting = current.result.turnaround - current.service # waiting
                end.append(ready.pop(0))
                if quantum == 0:
                    quantum = time_quantum
                    ready = sorted(ready, key=lambda Process : Process.priority) # 재정렬
            else:
                # 뒤로 보내기
                if quantum == 0:
                    quantum = time_quantum
                    ready.append(ready.pop(0))
                    ready = sorted(ready, key=lambda Process : Process.priority) # 재정렬
            
            # 비선점 priority with RR과 다른 케이스
            # quantum == 0 말고 그냥 priority로 뺏긴 케이스
            # 매 counter마다 재정렬
            if ready:
                temp = ready[0]
                temp_queue = sorted(ready, key=lambda Process : Process.priority)
                if temp.pId == temp_queue[0].pId:
                    ready = sorted(ready, key=lambda Process : Process.priority)
                else:
                    ready.append(ready.pop(0))
                    ready = sorted(ready, key=lambda Process : Process.priority)
            counter += 1
    # 결과
    print_result(end, gantt)

# 메인
n = int(input())
process_list = []
for i in range(0, n):
    pId, arrival, service, priority = input().split() 
    process_list.append(Process(pId, arrival, service, priority))
process_list = sorted(process_list, key=lambda Process: Process.arrival)
global time_quantum
time_quantum = int(input())
print()

'''
[sample 1]
5
3 2 6 4
1 0 10 3
2 1 28 2
4 3 4 1
5 4 14 2
2

[sample 2]
6
1 0 20 5
2 25 25 30
3 30 25 30
4 60 15 10
5 100 10 40
6 105 10 35
10
'''

# fcfs(n, process_list)
sjf(process_list)
srtf(process_list)
rr(process_list)
nonpreemptive_priority(process_list)
preemptive_priority(process_list)
nonpreemptive_priority_with_RR(process_list)
preemptive_priority_with_RR(process_list)