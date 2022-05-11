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
#Process라는 이름의 class 설정
#__init__메소드를 사용하여 클래스가 생성됨과 동시에 변수를 넣어주고자했음.

#변수 설정
#파라미터 변수 / pId, arrival_time ,service_time, priority
#pId: process Id의
#arrival_time: arrival_time의 약자
#service_time: service_time의 약자
#priority: priority


#내부클래스 Result 생성
#7번 라인의 self.result = self.Result()를 추가하여 객체(프로세스) 생성 때 부터 Result 클래스를 생성함.

#waiting, turnaround, reponse를 속성으로 가지도록 만들었음.
#입력 전이기 때문에 값을 0으로 초기화하였음.

#추가적으로 Result 클래스 내의 함수를 호출하려면, 
#Proces함수 내의 

'''
def outer_disp(self): 
    self.result.inner_disp(self.pId)
와 같은 함수를 만들고, 

Result클래스 내부에
def inner_disp(self, pId): 
    print(pId)
를 만들면, 

상위 클래스의 속성을 받아서 사용할 수 있음
'''




#입력값 예시


'''
4
P0 0 7 3
P1 2 4 2
p2 3 1 4
p3 6 3 1
2

5
P0 0 7 3
P1 2 4 2
p2 3 1 4
p3 6 3 1
p4 7 8 6
2

'''

#입력하여 객체를 만들어주는 코드

n = int(input())
#가장 처음 n개의 변수를 받을 것이다. 
#n은 프로세스를 몇 개 입력받을지 결정한다. 
for i in range(0, n):
    pId, arrival_time, service_time, priority = input().split() #문자열로 입력받기, class 내부에서 정수형은 정수형으로 변경해줄 것이다.
    globals()['P{}'.format(i)] = Process(pId, arrival_time, service_time, priority)
#입력받은 변수 n을 반복문을 통해서 각 개체를 만들어준다. 
#객체 이름을 각 순서에 맞게 설정해준다.
#객체 안에 __init__을 사용하여 생성할 파라미터를 넣어준다. 

time_quantum = int(input())
#전역변수에 time_quantum을 입력받기

#의도한 대로 잘 출력되는지 확인하기
print('P0 pId: {}, arrival_time: {}, service_time: {}, priority: {}'.format(P0.pId, P0.arrival_time, P0.service_time, P0.priority))
print('P0 pId: {}, waiting: {}, turnaround: {}, response: {}'.format(P0.pId, P0.result.waiting, P0.result.turnaround, P0.result.response))
print('P1 pId: {}, arrival_time: {}, service_time: {}, priority: {}'.format(P1.pId, P1.arrival_time, P1.service_time, P1.priority))
print('P1 pId: {}, waiting: {}, turnaround: {}, response: {}'.format(P1.pId, P1.result.waiting, P1.result.turnaround, P1.result.response))
print('P2 pId: {}, arrival_time: {}, service_time: {}, priority: {}'.format(P2.pId, P2.arrival_time, P2.service_time, P2.priority))
print('P2 pId: {}, waiting: {}, turnaround: {}, response: {}'.format(P2.pId, P2.result.waiting, P2.result.turnaround, P2.result.response))
print('P3 pId: {}, arrival_time: {}, service_time: {}, priority: {}'.format(P3.pId, P3.arrival_time, P3.service_time, P3.priority))
print('P3 pId: {}, waiting: {}, turnaround: {}, response: {}'.format(P3.pId, P3.result.waiting, P3.result.turnaround, P3.result.response))
print('P4 pId: {}, arrival_time: {}, service_time: {}, priority: {}'.format(P4.pId, P4.arrival_time, P4.service_time, P4.priority))
print('P4 pId: {}, waiting: {}, turnaround: {}, response: {}'.format(P4.pId, P4.result.waiting, P4.result.turnaround, P4.result.response))
