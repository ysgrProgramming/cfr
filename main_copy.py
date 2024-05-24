from typing import Literal
from heapq import heappush, heappop, heapify
from collections import deque

# container mode: {'stored', 'appearing', 'done'}
class Container:
    def __init__(self, idx: int, in_spot: int, out_spot: int, in_order: int, out_order: int):
        self.idx = idx
        self.in_spot = in_spot
        self.out_spot = out_spot
        self.in_order = in_order
        self.out_order = out_order
        self.x: int = 0
        self.y: int = in_spot
        self.mode: Literal['stored', 'appearing', 'done'] = 'stored'
    
    def __repr__(self):
        return f"{self.__class__.__name__}: idx={self.idx}, point={(self.x, self.y)}, mode={self.mode}"

# clane mode: {'free', 'catching', 'suicide'}
class Clane:
    def __init__(self, idx: int, init_x: int, init_y: int):
        self.idx = idx
        self.x: int = init_x
        self.y: int = init_y
        self.dest: tuple[int, int] | None = None
        self.mode: Literal['free', 'catching', 'suicide'] = 'free'
    
    def __repr__(self):
        return f"{self.__class__.__name__}: idx={self.idx}, point={(self.x, self.y)}, mode={self.mode}"

class PowerClane(Clane):
    pass

def find_course(clane_idx, x0, y0, t0, dest_x, dest_y, container_map, clane_map, free=True):
    course_map = [[[None]*n for _ in range(n)]]
    course_map[0][y0][x0] = 0
    todo = deque([(x0, y0, 0)])
    dir_list = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
    while todo:
        x, y, t = todo.popleft()
        for i, (dx, dy) in enumerate(dir_list):
            if not (0 <= x+dx < n and 0 <= y+dy < n): continue
            if clane_map[t+t0+1][y+dy][x+dx] != None: continue
            if clane_map[t+t0+1][y][x] != None and clane_map[t+t0][y+dy][x+dx] == clane_map[t+t0+1][y][x]: continue
            if free == False and clane_idx != 0 and container_map[t+t0+1][y+dy][x+dx] != None and (not (x == 0 and dx == dy == 0)): continue
            if len(course_map) == t+1: course_map.append([[None]*n for _ in range(n)])
            if course_map[t+1][y+dy][x+dx] != None: continue
            course_map[t+1][y+dy][x+dx] = i
            if x == x+dx == dest_x and y == y+dy == dest_y: break
            todo.append((x+dx, y+dy, t+1))
        else:
            continue
        break
    else:
        return None
    x, y = dest_x, dest_y
    course_inv = [(x, y)]
    for i in range(len(course_map)-1, 0, -1):
        if course_map[i][y][x] == None:
            print(course_map)
            print(course_inv)
        dx, dy = dir_list[course_map[i][y][x]]
        x, y = x-dx, y-dy
        course_inv.append((x, y))
    return course_inv[::-1]

def register_course(clane_idx, course, clane_map, t0):
    dir_list = [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]
    dir_str = "LU.DR"
    dir_dict = {d: s for d, s in zip(dir_list, dir_str)}
    for t, (x, y) in enumerate(course):
        clane_map[t+t0][y][x] = clane_idx
    stamp = []
    for i in range(len(course)-1):
        x1, y1 = course[i]
        x2, y2 = course[i+1]
        dx, dy = x2-x1, y2-y1
        s = dir_dict[(dx, dy)]
        stamp.append(s)
    return stamp

def argmin(li):
    min_ele = li[0]
    min_idx = 0
    for i, k in enumerate(li):
        if k < min_ele:
            min_ele = k
            min_idx = i
    return min_idx
        
def main(n, a_list):
    # make container_list
    cntn_list: list[Container] = []
    for i, a_line in enumerate(a_list):
        for j, a in enumerate(a_line):
            cntn = Container(a, i, a//n, j, a%n)
            cntn_list.append(cntn)
    cntn_list.sort(key=lambda x: x.idx)

    # make clane_list
    clane_list: list[Clane] = []
    clane_list.append(PowerClane(0, 0, 0))
    for i in range(1, n):
        clane = Clane(i, i, i)
        clane_list.append(clane)

    # make efficient queue
    cntn_idx_set_list: list[set[int] | None] = [None]*((n+1)**n)
    queue_list: list[list[int]] = [None]*((n+1)**n)
    min_eval_list: list[tuple[int, int]] = [(n*n, 0)]*((n+1)**n)
    min_eval_list[0] = (0, 0)
    queue_list[0] = []

    state = [0]*n
    for i in range(1, (n+1)**n):
        for j in range(n):
            if state[j] == n:
                state[j] = 0
            else:
                state[j] += 1
                break

        cntn_idx_set = set()
        for j in range(n):
            for k in range(state[j]):
                cntn_idx_set.add(a_list[j][k])
        
        for j in range(n):
            for k in range(n):
                idx = j*n+k
                if idx not in cntn_idx_set: break
                cntn_idx_set.remove(idx)
        cntn_idx_set_list[i] = cntn_idx_set

        min_length, min_score = n*n, 0
        queue = []
        for j in range(n):
            if state[j] == 0: continue
            prev = i - ((n+1)**j)
            prev_length, prev_score = min_eval_list[prev]
            if (prev_length, prev_score) < (min_length, min_score):
                min_length, min_score = prev_length, prev_score + len(cntn_idx_set)**2
                queue = queue_list[prev] + [a_list[j][state[j]-1]]
        min_length = max(min_length, len(cntn_idx_set))
        min_eval_list[i] = (min_length, min_score)
        queue_list[i] = queue

    print(min_eval_list[-1])
    #print(len(queue_list[-1]))
    print(queue_list[-1])

    # place planning
    priority_map = [
        [10, 8, 2, 0, 23],
        [14, 12, 6, 4, 21],
        [16, 17, 18, 19, 20],
        [15, 13, 7, 5, 22],
        [11, 9, 3, 1, 24]
    ]
    priority_list: list[tuple[int, int]] = [None]*(n**2)
    for y in range(n):
        for x in range(n):
            p = priority_map[y][x]
            priority_list[p] = (x, y)

    task_list = []
    stage = dict()
    ac_set = {i*n for i in range(n)}
    pri_list = [i for i in range(n**2)]
    heapify(pri_list)
    for i in queue_list[-1]:
        in_y = cntn_list[i].in_spot
        if i in ac_set:
            out_y = cntn_list[i].out_spot
            task = (i, (0, in_y), (n-1, out_y))
            task_list.append(task)
            zzz = i + 1
            ac_set.add(zzz)
            while zzz in stage:
                fr = stage.pop(zzz)
                to = (n-1, zzz//n)
                task = (zzz, fr, to)
                task_list.append(task)
                zzz += 1
                heappush(pri_list, priority_map[fr[1]][fr[0]])
                ac_set.add(zzz)
        else:
            pri_idx = heappop(pri_list)
            fr = (0, in_y)
            to = priority_list[pri_idx]
            task = (i, fr, to)
            stage[i] = to
            task_list.append(task)
    
    #print(len(task_list))
    print(task_list)
    #print(count_list)

    # course planning
    turn_size = 10000
    container_map: list[list[list[int | None]]] = [[[None]*n for _ in range(n)] for _ in range(turn_size)]
    for i in range(turn_size):
        for j in range(n):
            container_map[i][j][0] = 100
    
    clane_map: list[list[list[int | None]]] = [[[None]*n for _ in range(n)] for _ in range(turn_size)]
    
    clane_cursors = [(0, 0, i) for i in range(n)]
    clane_history = [[] for _ in range(n)]
    for i, (x0, y0), (dest_x, dest_y) in task_list:
        #print(clane_cursors)
        #print(clane_history)
        #print()
        idx = argmin(clane_cursors)
        t0, clane_x, clane_y = clane_cursors[idx]
        history = []
        course = find_course(idx, clane_x, clane_y, t0, x0, y0, container_map, clane_map, free=True)
        if course == None:
            max_len = max(len(hist) for hist in clane_history)
            for i in range(n):
                if max_len > len(clane_history[i]): clane_history[i].append('B')
            print(*["".join(hist) for hist in clane_history], sep="\n")
        s = register_course(idx, course, clane_map, t0)
        s[-1] = "P"
        history.extend(s)

        t1 = t0+len(history)
        course = find_course(idx, x0, y0, t1, dest_x, dest_y, container_map, clane_map, free=False)
        if course == None:
            for i in range(n):
                max_len = max(len(hist) for hist in clane_history)
                if max_len > len(clane_history[i]): clane_history[i].append('B')
            print(*["".join(hist) for hist in clane_history], sep="\n")
        course.append((dest_x, dest_y))
        s = register_course(idx, course, clane_map, t1)
        s[-1] = "Q"
        history.extend(s)

        clane_cursors[idx] = (t0+len(history), dest_x, dest_y)
        clane_history[idx].extend(history)
    max_len = max(len(hist) for hist in clane_history)
    for i in range(n):
        if max_len > len(clane_history[i]): clane_history[i].append('B')
    print(*["".join(hist) for hist in clane_history], sep="\n")
    for i in range(max_len):
        print(f"turn {i}")
        a = np.array(clane_map[i])
        print(np.where(a == None, -1, a)+1)
        print()
import numpy as np

n = 5
a_list = np.arange(n**2, dtype=int)
np.random.shuffle(a_list)
a_list = a_list.reshape((n, n))
#n = int(input())
#a_list = [list(map(int, input().split())) for _ in range(n)]
print(n)
print(a_list)
main(n, a_list)