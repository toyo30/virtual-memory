import sys
import copy

from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import *
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QScrollBar
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QGroupBox
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QTableView

# Process Class def =============================================== #

class Process:
    def __init__(self, pId, arrival, service, priority, num):
        self.pId = pId
        self.arrival = int(arrival)
        self.service = int(service)
        self.remaining_service = int(service)
        self.priority = int(priority)
        self.num = int(num)
        self.result = self.Result()

    class Result:        
        def __init__(self):
            self.waiting = 0
            self.turnaround = 0
            self.response = 0
            self.end = 0       

# Algorithms Result def =============================================== #  

class algorithms_result:

    def __init__(self, name):
        self.name = name
        self.av_waiting = 0
        self.av_turnaround = 0
        self.av_response = 0
        self.process = []
        self.gantt = []

algorithms_names = ['FCFS', 'SJF', 'SRTF', 'RR', 'NonPreP', 'PreP', 'NonPreP\nwith RR', 'PreP\nwith RR', 'HRRN']
algorithms_num = len(algorithms_names)

result = []
for i in range (0, algorithms_num):
    result.append(algorithms_result(algorithms_names[i]))

# get_result def =============================================== # 

def get_result(process_list, gantt, al_num):
    n = len(process_list)
    process_list = sorted(process_list, key=lambda Process : Process.num)
    result[al_num].gantt = gantt

    i = 0
    for process in process_list:
        result[al_num].process[i].result.waiting = copy.deepcopy(process.result.waiting)
        result[al_num].process[i].result.turnaround = copy.deepcopy(process.result.turnaround)
        result[al_num].process[i].result.response = copy.deepcopy(process.result.response)
        result[al_num].process[i].result.end = copy.deepcopy(process.result.end)
        i += 1
    
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

    result[al_num].av_waiting = copy.deepcopy(average_waiting)
    result[al_num].av_turnaround = copy.deepcopy(average_turnaround)
    result[al_num].av_response = copy.deepcopy(average_response)

# ALGORITHMS FUNC def =============================================== # 

def fcfs(process_list):
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
            if not_arrived[0].arrival <= counter + 1:
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
                if not_arrived[0].arrival <= counter + 1:
                    ready.append(not_arrived.pop(0))

            # 현재 process 삭제 여부 결정, result 연산
            if current.remaining_service == 0:
                current.result.end = counter + 1 # end
                current.result.turnaround = current.result.end - current.arrival # turnaround
                current.result.waiting = current.result.turnaround - current.service # waiting
                end.append(ready.pop(0))
            counter += 1
            
    get_result(end, gantt, 0)

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
        
        # idle task: not_arrived에는 아직 proces5s가 있지만, ready queue는 비어있는 상태
        if not ready and not_arrived:
            if not_arrived[0].arrival <= counter + 1:
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
                if not_arrived[0].arrival <= counter + 1:
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
    get_result(end, gantt, 1)

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
            if not_arrived[0].arrival <= counter + 1:
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
                if not_arrived[0].arrival <= counter + 1:
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

    get_result(end, gantt, 2)

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
            if not_arrived[0].arrival <= counter + 1:
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
                if not_arrived[0].arrival <= counter + 1:
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
    get_result(end, gantt, 3)
    
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
            if not_arrived[0].arrival <= counter + 1:
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
                if not_arrived[0].arrival <= counter + 1:
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
    get_result(end, gantt, 4)

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
            if not_arrived[0].arrival <= counter + 1:
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
                if not_arrived[0].arrival <= counter + 1:
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
    get_result(end, gantt, 5)

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
            if not_arrived[0].arrival <= counter + 1:
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
                if not_arrived[0].arrival <= counter + 1:
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
    get_result(end, gantt, 6)

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
            if not_arrived[0].arrival <= counter + 1:
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
                if not_arrived[0].arrival <= counter + 1:
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
    get_result(end, gantt, 7)

def hrrn(process_list):
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
            if not_arrived[0].arrival <= counter + 1:
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
                if not_arrived[0].arrival <= counter + 1:
                    ready.append(not_arrived.pop(0)) 

            # 현재 process 삭제 여부 결정, result 연산
            if current.remaining_service == 0:
                current.result.end = counter + 1 # end
                current.result.turnaround = current.result.end - current.arrival # turnaround
                current.result.waiting = current.result.turnaround - current.service # waiting
                end.append(ready.pop(0))
                # -------------------------------
                # 여기서부터 SJF와 달라짐
                # ready 재정렬 기준이 service time에서 response ratio로 바뀜
                # Highest Response Ratio Next, 우선순위 "내림차순" 정렬
                ready = sorted(ready, key=lambda Process : -Process.priority)

            # HRRN, 매 counter마다 대기 시간 계산 필요함
            for process in ready:
                if process == current:
                    pass
                else:
                    process.result.waiting += 1                    
                    # Response Ratio = (service time + waiting time) / service time
                    process.priority = (process.service + process.result.waiting) / process.service     
            counter += 1            
    # 결과
    get_result(end, gantt, 8)

# GUI def =============================================== #

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CPU Scheduler | 9조 | 김민재, 김주영, 박호경, 백민기')
        self.setGeometry(50, 50, 1600, 900)
        self.setFixedSize(1900, 900)
        self.center()
        self.show()

    # box_main def =============================================== #

        box_main = QHBoxLayout()
        self.setLayout(box_main)
        box_left = QVBoxLayout()
        self.n = 1
        self.col_n = 0
        self.selected = -1
        self.color = 0

    # box_table def =============================================== #

        box_table = QGridLayout()
    
        table_input = QtWidgets.QTableWidget(self)
        table_output = QtWidgets.QTableWidget(self)
        table_input.setColumnCount(4)
        table_output.setColumnCount(3)        
        table_input.setRowCount(self.n)
        table_output.setRowCount(self.n)
        table_input.setFixedSize(530, 550)
        table_output.setFixedSize(400, 550)

        head_names = ['Process\nID', 'Arrival\nTime', 'Service\nTime', 'Priority']
        table_input.setHorizontalHeaderLabels(head_names)
        head_names = ['Waiting\nTime', 'Turnaround\nTime', 'Response\nTime']
        table_output.setHorizontalHeaderLabels(head_names)
        table_output.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        table_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        table_output.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        box_table.addWidget(table_input, 0, 0)
        box_table.addWidget(table_output, 0, 1)

    # box_switch def =============================================== #

        box_switch = QGridLayout()

        def edit_input_row():
            n = self.n
            new_n = int(num_LineEdit.text())
            if (n == new_n): return
            if (n > new_n):
                temp = n - new_n
                for i in range (0, temp):
                    n = table_input.rowCount() - 1
                    table_input.removeRow(n)
                    n = table_output.rowCount() - 1
                    table_output.removeRow(n)
                self.n = new_n
                return
            if (n < new_n):
                temp = new_n - n
                for i in range (0, temp):
                    table_input.insertRow(n)
                    table_output.insertRow(n)                    
                self.n = new_n
                return

        input_switch = QHBoxLayout()
        input_switch.addStretch(0)
        # input_switch.setFixedWidth(550)

        temp_Label = QLabel('Process 개수:')
        input_switch.addWidget(temp_Label, alignment=Qt.AlignRight)

        num_LineEdit = QLineEdit()
        num_LineEdit.setFixedSize(50, 38)
        num_LineEdit.setValidator(QIntValidator())
        if self.n != None: num_LineEdit.setText(str(self.n))
        input_switch.addWidget(num_LineEdit, alignment=Qt.AlignRight)

        num_Button = QPushButton('편집')
        num_Button.setFixedSize(80, 40)
        num_Button.clicked.connect(edit_input_row)
        input_switch.addWidget(num_Button, alignment=Qt.AlignRight) 

        def switchColor():
            if (self.color): self.color = 0
            else: self.color = 1

        def tableColor(color, i, j):
            gantt_Table[i].item(0, j).setForeground(QtGui.QColor(255,255,255))
            if (color): gantt_Table[i].item(0, j).setBackground(QtGui.QColor(20,20,20))
            else: gantt_Table[i].item(0, j).setBackground(QtGui.QColor(100,100,100))

        def tableMerge():
            for i in range(0, algorithms_num):
                self.color = 0
                temp_merge = 0
                count = 0
                for j in range(0, self.col_n): 
                    # self.col_n-1 / 뒤의 것과 같을 때
                    # 뒤의 것과 다른데 count가 0 / 뒤의 것과 달라서 merge해야 함
                    if (j == self.col_n - 1):
                        if (count != 0): 
                            tableColor(self.color, i, j)                            
                            gantt_Table[i].setSpan(0, temp_merge, 1, count + 1)
                        else: 
                            tableColor(self.color, i, j) 
                            break

                    elif (result[i].gantt[j] == result[i].gantt[j + 1]): 
                        tableColor(self.color, i, j)
                        count += 1

                    elif (count == 0): 
                        temp_merge = j + 1
                        tableColor(self.color, i, j)
                        switchColor()

                    else: # 다를 때
                        tableColor(self.color, i, j)
                        switchColor()
                        gantt_Table[i].setSpan(0, temp_merge, 1, count + 1)
                        temp_merge = j + 1
                        count = 0

        def execute():          
            diff = self.n - len(result[0].process)
            if(diff > 0):
                for i in range(0, algorithms_num):
                    for j in range(0, diff):
                        result[i].process.append(Process('', 0, 0, 0, 0))
                    
            for i in range(0, algorithms_num):
                for j in range(0, self.n):
                    result[i].process[j].pId = table_input.item(j, 0).text()
                    result[i].process[j].arrival = table_input.item(j, 1).text()
                    result[i].process[j].service = table_input.item(j, 2).text()
                    result[i].process[j].priority = table_input.item(j, 3).text()
                    result[i].process[j].num = j

            process_list = []
            for i in range(0, self.n):
                process_list.append(Process(result[0].process[i].pId, result[0].process[i].arrival, result[0].process[i].service, result[0].process[i].priority, result[0].process[i].num))
            process_list = sorted(process_list, key=lambda Process: Process.arrival)
            global time_quantum
            time_quantum = int(tq_LineEdit.text())

            fcfs(process_list)
            sjf(process_list)
            srtf(process_list)
            rr(process_list)
            nonpreemptive_priority(process_list)
            preemptive_priority(process_list)
            nonpreemptive_priority_with_RR(process_list)
            preemptive_priority_with_RR(process_list)
            hrrn(process_list)

            if (self.selected == -1): 
                self.selected = 0
                gantt_Button[self.selected].toggle()

            for i in range(0, self.n):
                table_output.setItem(i, 0, QTableWidgetItem(str(result[self.selected].process[i].result.waiting)))
                table_output.setItem(i, 1, QTableWidgetItem(str(result[self.selected].process[i].result.turnaround)))
                table_output.setItem(i, 2, QTableWidgetItem(str(result[self.selected].process[i].result.response)))

            av_Label[0].setText(str(result[self.selected].av_waiting))
            av_Label[1].setText(str(result[self.selected].av_turnaround))
            av_Label[2].setText(str(result[self.selected].av_response))

            best_waiting = 0
            best_turnaround = 0
            best_response = 0

            for i in range(1, algorithms_num): # algorithms_num
                if (result[best_waiting].av_waiting > result[i].av_waiting): best_waiting = i
                if (result[best_turnaround].av_turnaround > result[i].av_turnaround): best_turnaround = i
                if (result[best_response].av_response > result[i].av_response): best_response = i
            
            best_Label[0].setText(str(result[best_waiting].name))
            best_Label[1].setText(str(result[best_turnaround].name))
            best_Label[2].setText(str(result[best_response].name))

            self.col_n = len(result[0].gantt)
            for i in range(0, algorithms_num):
                gantt_Table[i].clearSpans()
                gantt_Table[i].setColumnCount(self.col_n)
                gantt_Table[i].setRowCount(1)
                for j in range(0, self.col_n):
                    if (str(result[i].gantt[j]) == ' '): result[i].gantt[j] = 'idle'
                    item = QTableWidgetItem(str(result[i].gantt[j]))
                    item.setTextAlignment(Qt.AlignCenter)
                    gantt_Table[i].setItem(0, j, item)
                for j in range(0, self.col_n): gantt_Table[i].setColumnWidth(j, 4)

            tableMerge()
            return

        output_switch = QHBoxLayout()
        output_switch.addStretch(0)
        # output_switch.setFixedWidth(400)

        temp_Label = QLabel('Time Quantum:')
        output_switch.addWidget(temp_Label, alignment=Qt.AlignRight)

        tq_LineEdit = QLineEdit()
        tq_LineEdit.setFixedSize(50, 38)
        tq_LineEdit.setValidator(QIntValidator())
        if self.n != None: tq_LineEdit.setText('0')
        output_switch.addWidget(tq_LineEdit, alignment=Qt.AlignRight)

        execute_Button = QPushButton('실행')
        execute_Button.setFixedSize(80, 40)
        execute_Button.clicked.connect(execute)
        output_switch.addWidget(execute_Button, alignment=Qt.AlignRight)

        space_a = 20
        space_b = 9
        for i in range(0, space_a): 
            temp_Label = QLabel(' ')
            temp_Label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            box_switch.addWidget(temp_Label, 0, i)
        box_switch.addLayout(input_switch, 0, space_a)
        space_a += 1
        for i in range(0, space_b): 
            temp_Label = QLabel(' ')
            temp_Label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            box_switch.addWidget(temp_Label, 0, i + space_a)
        box_switch.addLayout(output_switch, 0, space_a + space_b)

    # box_result def =============================================== #

        box_result = QGridLayout()
        temp_Label = QLabel()
        bold_font = temp_Label.font()
        bold_font.setBold(True)

        names = ['', '', '']
        coords = [(0, j) for j in range(0, 3)]
        for name, coord in zip(names, coords):
            temp_Label = QLabel(name)
            temp_Label.setAlignment(Qt.AlignCenter)
            temp_Label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            box_result.addWidget(temp_Label, *coord, alignment=Qt.AlignCenter)

        names = ['Average\nWaiting Time', 'Average\nTurnaround Time', 'Average\nResponse Time']
        coords = [(1, j) for j in range(0, 3)]
        for name, coord in zip(names, coords):
            temp_Label = QLabel(name)
            temp_Label.setFont(bold_font)
            temp_Label.setAlignment(Qt.AlignCenter)
            temp_Label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            box_result.addWidget(temp_Label, *coord, alignment=Qt.AlignCenter)

        names = ['0.0', '0.0', '0.0']
        coords = [(2, j) for j in range(0, 3)]
        av_Label = []
        i = 0
        for name, coord in zip(names, coords):
            av_Label.append(QLabel(name))
            av_Label[i].setAlignment(Qt.AlignCenter)
            av_Label[i].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            box_result.addWidget(av_Label[i], *coord, alignment=Qt.AlignCenter)
            i += 1

        names = ['', '', '']
        coords = [(3, j) for j in range(0, 3)]
        for name, coord in zip(names, coords):
            temp_Label = QLabel(name)
            temp_Label.setAlignment(Qt.AlignCenter)
            box_result.addWidget(temp_Label, *coord, alignment=Qt.AlignCenter)

        names = ['Best\nWaiting Time', 'Best\nTurnaround Time', 'Best\nResponse Time']
        coords = [(4, j) for j in range(0, 3)]
        for name, coord in zip(names, coords):
            temp_Label = QLabel(name)
            temp_Label.setFont(bold_font)
            temp_Label.setAlignment(Qt.AlignCenter)
            temp_Label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            box_result.addWidget(temp_Label, *coord, alignment=Qt.AlignCenter)

        names = ['None', 'None', 'None']
        coords = [(5, j) for j in range(0, 3)]
        best_Label = []
        i = 0
        for name, coord in zip(names, coords):
            best_Label.append(QLabel(name))
            best_Label[i].setAlignment(Qt.AlignCenter)
            best_Label[i].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            box_result.addWidget(best_Label[i], *coord, alignment=Qt.AlignCenter)
            i += 1

        names = ['', '', '']
        coords = [(6, j) for j in range(0, 3)]
        for name, coord in zip(names, coords):
            temp_Label = QLabel(name)
            temp_Label.setAlignment(Qt.AlignCenter)
            temp_Label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            box_result.addWidget(temp_Label, *coord, alignment=Qt.AlignCenter)

    # box_gantt def =============================================== #

        box_gantt = QGridLayout()

        def gantt_button():
            if (self.selected == -1):
                for i in range(0, algorithms_num): gantt_Button[i].setChecked(False)
                return
            clicked = -1
            for i in range(0, algorithms_num):
                if (gantt_Button[i].isChecked() and i != self.selected):
                    clicked = i
                    self.selected = clicked
                if (clicked != -1): break
            for i in range(0, algorithms_num):
                if (i != clicked): gantt_Button[i].setChecked(False)
                if (i == clicked): gantt_Button[i].setChecked(True)
            result_button()
            return

        def result_button():
            for i in range(0, self.n):
                table_output.setItem(i, 0, QTableWidgetItem(str(result[self.selected].process[i].result.waiting)))
                table_output.setItem(i, 1, QTableWidgetItem(str(result[self.selected].process[i].result.turnaround)))
                table_output.setItem(i, 2, QTableWidgetItem(str(result[self.selected].process[i].result.response)))

            av_Label[0].setText(str(result[self.selected].av_waiting))
            av_Label[1].setText(str(result[self.selected].av_turnaround))
            av_Label[2].setText(str(result[self.selected].av_response))

        coords = [(j, 1) for j in range(0, algorithms_num)]
        gantt_Button = []
        for i in range(0, algorithms_num):
            gantt_Button.append(QPushButton(result[i].name))
            gantt_Button[i].setCheckable(True)
            gantt_Button[i].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            gantt_Button[i].released.connect(gantt_button)
            box_gantt.addWidget(gantt_Button[i], i, 1)

        gantt_Table = []
        for i in range(0, algorithms_num):
            gantt_Table.append(QtWidgets.QTableWidget(self))
            gantt_Table[i].setColumnCount(self.col_n)
            gantt_Table[i].setRowCount(0)
            gantt_Table[i].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            gantt_Table[i].verticalHeader().setVisible(False)
            gantt_Table[i].setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            box_gantt.addWidget(gantt_Table[i], i, 2)     

    # box_main add =============================================== #

        # box_main.addStretch(0)
        box_left.addLayout(box_table)
        box_left.addLayout(box_switch)
        box_left.addLayout(box_result)
        box_main.addLayout(box_left)
        box_main.addLayout(box_gantt)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
   app = QApplication(sys.argv)

   fontDB = QFontDatabase()
   fontDB.addApplicationFont('./조선일보명조.ttf')
   app.setFont(QFont('조선일보명조'))

   ex = MyApp()
   sys.exit(app.exec_())