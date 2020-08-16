import numpy as np
import matplotlib.pyplot as plt
from copy import copy

ACTION_SIZE = 8


def read_input_txt(file):
    with open(file) as f:
        mat = f.read()
    mat_lst = list(mat)
    m_cnt, n_cnt, m, n = 0, 0, 0, 0
    for c in mat_lst:
        if c== '\n':
            m_cnt += 1
            n = max(n_cnt, n)
            n_cnt = 0
        else:
            n_cnt += 1
    m = m_cnt
    # print(mat_lst)
    # print(m, n)

    m_cnt = 0
    last_line_num = 0
    for c in mat_lst:

        if m_cnt == m:

            if c is not ' ':
                last_line_num += 1

        if c == '\n':
            m_cnt += 1

    m = m +1
    n = max(last_line_num, n)
    # print(m, n)

    encode_mat = np.zeros((m,n), dtype=np.uint8)

    idx_m = 0
    idx_n = 0
    for c in mat_lst:
        if c == ' ' :
            encode_mat[idx_m][idx_n] = 0
            idx_n +=1
        elif c == '#':
            encode_mat[idx_m][idx_n] = 1
            idx_n += 1
        elif c == 'B':
            encode_mat[idx_m][idx_n] = 2
            idx_n += 1
        elif c == '.':
            encode_mat[idx_m][idx_n] = 3
            idx_n += 1
        elif c == 'X':
            encode_mat[idx_m][idx_n] = 4
            idx_n += 1
        elif c == '&':
            encode_mat[idx_m][idx_n] = 5
            idx_n += 1
        elif c == '\n':
            idx_m+=1
            idx_n=0
        else:
            raise Exception("not recognize char", c)

        if idx_m==m-1 and idx_n==n-1:
            break


    print(encode_mat)
    return encode_mat


encode_mat = read_input_txt('level3.txt')
# read_input_txt('level2.txt')
# read_input_txt('level3.txt')
# read_input_txt('test1.txt')
# read_input_txt('test2.txt')
# read_input_txt('test3.txt')


(SIZE_M, SIZE_N) = encode_mat.shape
# print(SIZE_M, SIZE_N)

class Actor:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init
    #
    # def __str__(self):
    #     return "{}, {}".format(self.x, self.y)

    def __sub__(self, other):
        return np.abs(self.x - other.x)+np.abs(self.y - other.y)

    def action(self, choice):
        if choice == 0:
            self.move(0, 1)
        elif choice == 1:
            self.move(0, -1)
        elif choice == 2:
            self.move(-1, 0)
        elif choice == 3:
            self.move(1, 0)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


        if self.x <0:
            self.x = 0
        elif self.x > SIZE_M-1:
            self.x = SIZE_M -1

        if self.y < 0:
            self.y = 0
        elif self.y > SIZE_N - 1:
            self.y = SIZE_N - 1


for i in range(SIZE_M):
    for j in range(SIZE_N):
        if encode_mat[i][j]==5:
            player = Actor(i, j)
            print("player at i j:",i,j)
            break

box_lst = []
goal_lst = []
wall_lst = []
for i in range(SIZE_M):
    for j in range(SIZE_N):
        if encode_mat[i][j] == 1:
            wall_lst.append(Actor(j, i))
        elif encode_mat[i][j] == 2:
            box_lst.append(Actor(j, i))
        elif encode_mat[i][j] == 3:
            goal_lst.append(Actor(j, i))
        elif encode_mat[i][j] == 4:
            box_lst.append(Actor(j, i))
            goal_lst.append(Actor(j, i))

assert (len(box_lst) == len(goal_lst))
print('box number:', len(box_lst))
print('wall number:', len(wall_lst))


class Env:
    def __init__(self, wall_lst, box_lst, goal_lst, player):
        self.wall_lst = wall_lst
        self.box_lst = box_lst
        self.goal_lst = goal_lst
        self.player = player
        self.action_dict = {0:'move up',
                            1:'move down',
                            2:'move left',
                            3:'move right',
                            4: 'push up',
                            5: 'push down',
                            6: 'push left',
                            7: 'push right'}


    def obs(self):
        # obs_mat = np.zeros((len(self.wall_lst)+1,2), np.uint8)
        # for i in range(len(self.wall_lst)):
        #     obs_mat[i][0] = self.wall_lst[i].x
        #     obs_mat[i][1] = self.wall_lst[i].y
        #
        # obs_mat[-1][0] = player.x
        # obs_mat[-1][1] = player.y
        #
        # # print(obs_mat)

        obs_tuple_x = tuple()
        obs_tuple_y = tuple()
        for i in range(len(self.wall_lst)):
            obs_tuple_x = obs_tuple_x +(self.wall_lst[i].x,)
            obs_tuple_y = obs_tuple_y +(self.wall_lst[i].y,)

        obs_tuple_x = obs_tuple_x + (self.player.x,)
        obs_tuple_y = obs_tuple_y + (self.player.y,)
        return (obs_tuple_x, obs_tuple_y)

    def display(self):
        encode_mat = np.zeros((SIZE_M,SIZE_N), dtype=np.uint8)
        for actor in self.wall_lst:
            encode_mat[actor.y][actor.x] += 1
        for actor in self.box_lst:
            encode_mat[actor.y][actor.x] += 2
        for actor in self.goal_lst:
            encode_mat[actor.y][actor.x] += 3

        for i in range(SIZE_M):
            for j in range(SIZE_N):
                if encode_mat[i][j] == 5:
                    encode_mat[i][j] = 4

        encode_mat[self.player.y][self.player.x] = 5

        print(encode_mat)
        raw_mat = np.zeros((SIZE_M, SIZE_N), dtype=np.str)

        str = ''
        for i in range(SIZE_M):
            for j in range(SIZE_N):
                a = encode_mat[i][j]
                if a == 0:
                    raw_mat[i][j] = ' '
                elif a == 1:
                    raw_mat[i][j] = '#'
                elif a == 2:
                    raw_mat[i][j] = 'B'
                elif a == 3:
                    raw_mat[i][j] = '.'
                elif a == 4:
                    raw_mat[i][j] = 'X'
                elif a == 5:
                    raw_mat[i][j] = '&'

                str = str + raw_mat[i][j]
            str = str + '\n'
        print(str)

    def action(self, action):
        if action == 0 or action == 1 or action == 2 or action == 3:
            new_player = copy(self.player)
            new_player.action(action)
            if not self.is_move_fail(new_player):
                self.player = new_player

        elif action == 4 or action == 5 or action == 6 or action == 7:
            new_player = copy(self.player)
            new_player.action(action-4)

            fail_push = False
            is_neighborBox = False
            for idx in range(len(self.box_lst)):
                if new_player - self.box_lst[idx] == 0:
                    is_neighborBox = True
                    neighbor_idx = idx
                    break

            if not is_neighborBox:
                fail_push = True
            else:
                new_box = copy(self.box_lst[idx])
                new_box.action(action-4)
                for i in range(len(self.wall_lst)):
                    if new_box - self.wall_lst[i] == 0:
                        fail_push = True
                        break
                for i in range(len(self.box_lst)):
                    if new_box - self.box_lst[i] == 0 and i is not neighbor_idx:
                        fail_push = True
                        break

            if not fail_push:
                self.player = new_player
                self.box_lst[neighbor_idx] = new_box


    def is_move_fail(self, new_player):
        fail_move = False
        for actor in self.wall_lst:
            if new_player-actor ==0:
                fail_move = True
                break
        for actor in self.box_lst:
            if new_player-actor ==0:
                fail_move = True
                break

        return fail_move




env = Env(wall_lst, box_lst, goal_lst,player)
# env.obs()
env.display()
action =2
print(f"next action: {action}, {action} is {env.action_dict[action]}")
env.action(action)
env.display()

action =3
print(f"next action: {action}, {action} is {env.action_dict[action]}")
env.action(action)
env.display()

action =7
print(f"next action: {action}, {action} is {env.action_dict[action]}")
env.action(action)
env.display()

# input_str = None
# while input_str is not 'q':
#     print('press q for quit')
#     print("press w,s,a,d -> move up, down, left, right")
#     print("press i,k,j,l -> push up, down, left, right")
#     input_str = input("Please Enter your command: ")
#     c = input_str[0]
#     action = None
#     if c == 's':
#         action = 0
#     elif c == 'w':
#         action = 1
#     elif c == 'a':
#         action = 2
#     elif c == 'd':
#         action = 3
#     elif c == 'k':
#         action = 4
#     elif c == 'i':
#         action = 5
#     elif c == 'j':
#         action = 6
#     elif c == 'l':
#         action = 7
#
#     if action is not None:
#         print(f"next action: {action}, {action} is {env.action_dict[action]}")
#         env.action(action)
#         env.display()

obs_tuple = env.obs()
q_table = {}
q_table[obs_tuple] = 0
print(q_table)


