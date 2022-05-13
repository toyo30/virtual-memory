
# ===== 클래스 정의 ==================================================================================== #

class Process:
    def __init__(self, pId, arrival, service, priority):
        self.pId = pId
        self.arrival = int(arrival)   # 일관적인 타입을 사용하는 게 좋을 것 같아 int() 추가했습니다.
        self.service = int(service) 
        self.priority = int(priority)           # 출력상 문제가 있어 간트차트 구현 이전까지는
        self.result = self.Result()             # 정수형으로 작업하는 게 좋을 것 같습니다.
    class Result:                               # 마침 정수형으로 시작했으니 우선은 정수형으로 작업하고, 
        def __init__(self):                     # 추후 float로 바꾸는 게 어떨까 싶어요. / 바꿔야 할 필요가 있나? 싶기도 함...
            self.waiting = 0
            self.turnaround = 0
            self.response = 0
            self.end = 0              # 끝나는 시간을 '기록'하는 공간을 만들었습니다.

    def print(self):    # 편의상 작성한 출력 함수. 'process_list[i].print()'와 같은 명령어로 하단의 내용을 출력할 수 있습니다.
        print('pId: {}, arrival: {}, service: {}, priority: {}'.format(self.pId, self.arrival, self.service, self.priority))
        print('pId: {}, waiting: {}, turnaround: {}, response: {}, end: {}\n'.format(self.pId, self.result.waiting, self.result.turnaround, self.result.response, self.result.end))

# ===== 함수 정의 ==================================================================================== #

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

    
# ===== 메인 ==================================================================================== #

# 입력
n = int(input())
process_list = []
for i in range(0, n):
    pId, arrival, service, priority = input().split() 
    process_list.append(Process(pId, arrival, service, priority))
time_quantum = int(input())
print(' ')

# FCFS 함수 실행
fcfs(n, process_list)
