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

def sjf(n, process_list):
    # arrival time 기준으로 정렬
    pList = sorted(process_list, key=lambda Process: Process.arrival)

    # counter 올릴 total 시간
    # idle task까지 고려해서 넉넉하게
    total = 0
    for process in pList:
        total = total + process.service + process.arrival

    # 대기 큐, 실행이 끝난 큐, 간트 차트    
    waitQ = []
    endQ = []
    gantt = []

    # arrival time == 0인 process를 waiting queue에 추가
    if pList[0].arrival == 0:
        waitQ.append(pList[0])
        del pList[0]

    for counter in range(total):
        # waiting queue가 비어있다면(idle task), ' ' 출력
        if not waitQ:
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]
                gantt.append(' ')
            # process_list도 비어있고 waiting queue도 비어있을 때는 pass
            else:
                pass
        
        # waiting queue가 비어있지 않다면
        else:
            # 현재 process의 남은 service time 줄이고, 간트 차트에 pId 출력
            waitQ[0].service -= 1
            gantt.append(waitQ[0].pId)

            # waiting queue 업데이트: new arrival 확인
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]

            # 현재 process 삭제 여부 결정
            if waitQ[0].service == 0:
                waitQ[0].result.end = counter + 1
                endQ.append(waitQ[0])
                del waitQ[0]
                # 삭제할 때만 재정렬
                waitQ = sorted(waitQ, key=lambda Process : Process.service)

    # 간트 차트 출력
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

def srtf(n, process_list):
    # arrival time 기준으로 정렬
    pList = sorted(process_list, key=lambda Process: Process.arrival)

    # counter 올릴 total 시간
    # idle task까지 고려해서 넉넉하게
    total = 0
    for process in pList:
        total = total + process.service + process.arrival

    # 대기 큐, 실행이 끝난 큐, 간트 차트    
    waitQ = []
    endQ = []
    gantt = []

    # arrival time == 0인 process를 waiting queue에 추가
    if pList[0].arrival == 0:
        waitQ.append(pList[0])
        del pList[0]

    for counter in range(total):
        # waiting queue가 비어있다면(idle task), ' ' 출력
        if not waitQ:
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]
                gantt.append(' ')
            # process_list도 비어있고 waiting queue도 비어있을 때는 pass
            else:
                pass
            
        # waiting queue가 비어있지 않다면
        else:
            # 현재 process의 남은 service time 줄이고, 간트 차트에 pId 출력
            waitQ[0].service -= 1
            gantt.append(waitQ[0].pId)

            # waiting queue 업데이트: new arrival 확인
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]

            # 현재 process 삭제 여부 결정
            if waitQ[0].service == 0:
                waitQ[0].result.end = counter + 1
                endQ.append(waitQ[0])
                del waitQ[0]

            # waiting queue를 남은 service time으로 정렬
            # sjf와 달리 매 counter마다 재정렬
            waitQ = sorted(waitQ, key=lambda Process : Process.service)

    # 간트 차트 출력
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
    # arrival time 기준으로 정렬
    pList = sorted(process_list, key=lambda Process: Process.arrival)
    quantum = time_quantum

    # counter 올릴 total 시간
    # idle task까지 고려해서 넉넉하게
    total = 0
    for process in pList:
        total = total + process.service + process.arrival

    # 대기 큐, 실행이 끝난 큐, 간트 차트    
    waitQ = []
    endQ = []
    gantt = []

    # arrival time == 0인 process를 waiting queue에 추가
    if pList[0].arrival == 0:
        waitQ.append(pList[0])
        del pList[0]

    for counter in range(total):
        # waiting queue가 비어있다면(idle task), ' ' 출력
        if not waitQ:
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]
                gantt.append(' ')
            # process_list도 비어있고 waiting queue도 비어있을 때는 pass
            else:
                pass

        # waiting queue가 비어있지 않다면
        else:   
            # 현재 process의 남은 service time 줄이고, 간트 차트에 pId 출력
            # time quantum도 줄임
            waitQ[0].service -= 1
            gantt.append(waitQ[0].pId)
            quantum -= 1

            # waiting queue 업데이트: new arrival 확인
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]

            # waiting queue 재정렬
            # service time == 0: 현재 프로세스 삭제
            if waitQ[0].service == 0:
                waitQ[0].result.end = counter + 1
                endQ.append(waitQ[0])
                del waitQ[0]

                if quantum == 0:
                    quantum = time_quantum
            # service time != 0: 뒤로 보내기
            else:                
                if quantum == 0:
                    quantum = time_quantum
                    waitQ.append(waitQ[0])
                    del waitQ[0]

    # 간트 차트 출력
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
    # arrival time 기준으로 정렬
    pList = sorted(process_list, key=lambda Process: Process.arrival)

    # counter 올릴 total 시간
    # idle task까지 고려해서 넉넉하게
    total = 0
    for process in pList:
        total = total + process.service + process.arrival

    # 대기 큐, 실행이 끝난 큐, 간트 차트    
    waitQ = []
    endQ = []
    gantt = []

    # arrival time == 0인 process를 waiting queue에 추가
    if pList[0].arrival == 0:
        waitQ.append(pList[0])
        del pList[0]

    for counter in range(total):
        # waiting queue가 비어있다면(idle task), ' ' 출력
        if not waitQ:
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]
                gantt.append(' ')
            # process_list도 비어있고 waiting queue도 비어있을 때는 pass
            else:
                pass
        
        # waiting queue가 비어있지 않다면
        else:
            # 현재 process의 남은 service time 줄이고, 간트 차트에 pId 출력
            waitQ[0].service -= 1
            gantt.append(waitQ[0].pId)

            # waiting queue 업데이트: new arrival 확인
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]
        
            # 현재 process 삭제 여부 결정
            if waitQ[0].service == 0:
                waitQ[0].result.end = counter + 1
                endQ.append(waitQ[0])
                del waitQ[0]
                # 삭제할 때만 재정렬
                waitQ = sorted(waitQ, key=lambda Process : Process.priority)

    # 간트 차트 출력
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
    # arrival time 기준으로 정렬
    pList = sorted(process_list, key=lambda Process: Process.arrival)

    # counter 올릴 total 시간
    # idle task까지 고려해서 넉넉하게
    total = 0
    for process in pList:
        total = total + process.service + process.arrival

    # 대기 큐, 실행이 끝난 큐, 간트 차트    
    waitQ = []
    endQ = []
    gantt = []

    # arrival time == 0인 process를 waiting queue에 추가
    if pList[0].arrival == 0:
        waitQ.append(pList[0])
        del pList[0]

    for counter in range(total):
        # waiting queue가 비어있다면(idle task), ' ' 출력
        if not waitQ:
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]
                gantt.append(' ')
            # process_list도 비어있고 waiting queue도 비어있을 때는 pass
            else:
                pass
            
        # waiting queue가 비어있지 않다면
        else:
            # 현재 process의 남은 service time 줄이고, 간트 차트에 pId 출력
            waitQ[0].service -= 1
            gantt.append(waitQ[0].pId)

            # waiting queue 업데이트: new arrival 확인
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]

            # 현재 process 삭제 여부 결정
            if waitQ[0].service == 0:
                waitQ[0].result.end = counter + 1
                endQ.append(waitQ[0])
                del waitQ[0]

            # waiting queue를 남은 service time으로 정렬
            # sjf와 달리 매 counter마다 재정렬
            waitQ = sorted(waitQ, key=lambda Process : Process.priority)

    # 간트 차트 출력
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
    # arrival time 기준으로 정렬
    pList = sorted(process_list, key=lambda Process: Process.arrival)
    quantum = time_quantum

    # counter 올릴 total 시간
    # idle task까지 고려해서 넉넉하게
    total = 0
    for process in pList:
        total = total + process.service + process.arrival

    # 대기 큐, 실행이 끝난 큐, 간트 차트    
    waitQ = []
    endQ = []
    gantt = []

    # arrival time == 0인 process를 waiting queue에 추가
    if pList[0].arrival == 0:
        waitQ.append(pList[0])
        del pList[0]

    for counter in range(total):
        # waiting queue가 비어있다면(idle task), ' ' 출력
        if not waitQ:
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]
                gantt.append(' ')
            # process_list도 비어있고 waiting queue도 비어있을 때는 pass
            else:
                pass

        # waiting queue가 비어있지 않다면
        else:
            # 현재 process의 남은 service time 줄이고, 간트 차트에 pId 출력
            # time quantum도 줄임
            waitQ[0].service -= 1
            gantt.append(waitQ[0].pId)
            quantum -= 1

            # waiting queue 업데이트: new arrival 확인
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]

            # waiting queue 재정렬
            if waitQ[0].service == 0:
                waitQ[0].result.end = counter + 1
                endQ.append(waitQ[0])
                del waitQ[0]

                if quantum == 0:
                    quantum = time_quantum
                    # quantum마다 재정렬
                    waitQ = sorted(waitQ, key=lambda Process : Process.priority)
            else:
                # 뒤로 보내기
                if quantum == 0:
                    quantum = time_quantum
                    waitQ.append(waitQ[0])
                    del waitQ[0]
                    # quantum마다 재정렬
                    waitQ = sorted(waitQ, key=lambda Process : Process.priority)
        
    # 간트 차트 출력
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

def preemptive_priority_with_RR(n, process_list, time_quantum):
    # arrival time 기준으로 정렬
    pList = sorted(process_list, key=lambda Process: Process.arrival)
    quantum = time_quantum

    # counter 올릴 total 시간
    # idle task까지 고려해서 넉넉하게
    total = 0
    for process in pList:
        total = total + process.service + process.arrival

    # 대기 큐, 실행이 끝난 큐, 간트 차트
    waitQ = []
    endQ = []
    gantt = []

    # arrival time == 0인 process를 waiting queue에 추가
    if pList[0].arrival == 0:
        waitQ.append(pList[0])
        del pList[0]

    for counter in range(total):
        # waiting queue가 비어있다면(idle task), ' ' 출력
        if not waitQ:
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]
                gantt.append(' ')
            # process_list도 비어있고 waiting queue도 비어있을 때는 pass
            else:
                pass

        # waiting queue가 비어있지 않다면
        else:
            # 현재 process의 남은 service time 줄이고, 간트 차트에 pId 출력
            # time quantum도 줄임
            waitQ[0].service -= 1
            gantt.append(waitQ[0].pId)
            quantum -= 1

            # waiting queue 업데이트: new arrival 확인
            if pList:
                if pList[0].arrival == counter + 1:
                    waitQ.append(pList[0])
                    del pList[0]

            # waiting queue 재정렬
            # 현재 process 삭제
            if waitQ[0].service == 0:
                waitQ[0].result.end = counter + 1
                endQ.append(waitQ[0])
                del waitQ[0]

                if quantum == 0:
                    quantum = time_quantum
                    # quantum마다 재정렬
                    waitQ = sorted(waitQ, key=lambda Process : Process.priority)
            else:
                # 뒤로 보내기        
                if quantum == 0:
                    quantum = time_quantum
                    waitQ.append(waitQ[0])
                    del waitQ[0]
                    # quantum마다 재정렬
                    waitQ = sorted(waitQ, key=lambda Process : Process.priority)
            
            # 비선점 priority with RR과 다른 케이스
            # quantum == 0 말고 그냥 priority로 뺏긴 케이스
            # 매 counter마다 재정렬
            if waitQ:
                temp = waitQ[0]
                tempQ = sorted(waitQ, key=lambda Process : Process.priority)
                if temp.pId == tempQ[0].pId:
                    waitQ = sorted(waitQ, key=lambda Process : Process.priority)
                else:
                    waitQ.append(waitQ[0])
                    del waitQ[0]
                    waitQ = sorted(waitQ, key=lambda Process : Process.priority)

        
    # 간트 차트 출력
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

'''
sample1
5
3 2 6 4
1 0 10 3
2 1 28 2
4 3 4 1
5 4 14 2
2

sample2
5
3 2 6 4
1 0 10 3
2 1 28 2
4 3 4 1
5 92 14 2
2

sample3
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
# sjf(n, process_list)
# srtf(n, process_list)
# rr(n, process_list, time_quantum)
# nonpreemptive_priority(n, process_list)
preemptive_priority(n, process_list)
# nonpreemptive_priority_with_RR(n, process_list, time_quantum)
# preemptive_priority_with_RR(n, process_list, time_quantum)