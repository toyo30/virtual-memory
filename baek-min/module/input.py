class Process:
    def __init__(self, pId, aTime ,sTime, priority):
        self.pId = pId
        self.aTime = int(aTime)
        self.sTime = int(sTime)
        self.priority = int(priority)

#Process라는 이름의 class 설정
#__init__메소드를 사용하여 클래스가 생성됨과 동시에 변수를 넣어주고자했음.

#변수 설정
# 파라미터 변수 / pId, aTime ,sTime, priority
# pId: process Id의
# aTime: arrival_time의 약자
# sTime: service_time의 약자
# priority: priority

#결과값 몇 개가 들어오든지 간에 결국 다 받아서 출력만 되면 된다. 

'''
4
P0 0 7 3
P1 2 4 2
p2 3 1 4
p3 6 3 1
2
'''

n = int(input())
#가장 처음 n개의 변수를 받을 것이다. 
#프로세스
for i in range(0, n):
    pId, aTime ,sTime, priority = input().split() #문자열로
    globals()['P{}'.format(i)] = Process(pId, aTime, sTime, priority)

time_quantum = int(input())

print('P0 pId: {}, aTime: {}, sTime: {}, priority: {}'.format(P0.pId, P0.aTime ,P0.sTime, P0.priority))
print('P1 pId: {}, aTime: {}, sTime: {}, priority: {}'.format(P1.pId, P1.aTime ,P1.sTime, P1.priority))
print('P2 pId: {}, aTime: {}, sTime: {}, priority: {}'.format(P2.pId, P2.aTime ,P2.sTime, P2.priority))
print('P3 pId: {}, aTime: {}, sTime: {}, priority: {}'.format(P3.pId, P3.aTime ,P3.sTime, P3.priority))
