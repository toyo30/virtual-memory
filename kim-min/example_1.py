# https://dailyheumsi.tistory.com/67

import heapq

def solution(process:list) -> list:
    """[summary]
    SRTF Scheduling Algorithm 구현
    if) Processing_time is same, Next Priority: Process_id(Order by asc)
    
    Args:
        process (list): 작업들. [Arrival_time, Processing_time]

    Returns:
        list: 작업이 먼저 끝난 Process_id순으로
    """
    ans = []

    # 1. Order by Arrival time, Processing time, Process_id
    lst = []
    for i in range(len(process)):
        ## [Arrival_time, Processing_time, Process_id]
        lst.append([process[i][0], process[i][1], i+1])

    lst.sort()

    # 2. SRTF(Shortest Remaining Time First) Scheduling
    works = []
    heapq.heapify(works)
    ## element: [Processing_time, Process_id, Arrival_time]
    for arrival, service, pId in lst:
        print(arrival, service, pId)
        # idle task?
        if not works:
            heapq.heappush(works, [service, pId, arrival])
            continue
        
        running_time = arrival - works[0][2]
        # print(arrival)
        # print(works[0][0], works[0][1], works[0][2])
        works[0][0] -= running_time
        if works[0][0] <= 0:
            _, endQ, __ = heapq.heappop(works)
            ans.append(endQ)

        heapq.heappush(works, [service, pId, arrival])

    while works:
        _, endQ, __ = heapq.heappop(works)
        ans.append(endQ)

    return ans

print(solution([[2, 4], [0, 8], [5, 1], [9, 8], [3, 2]]))