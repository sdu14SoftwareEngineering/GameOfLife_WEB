import threading

import time

from django.shortcuts import render

from game import models
from game.method.in_room import exit_room_by_id
from game.tool import strategy, room_tool
from game.tool.tools import *

# 所有房间布局
thread_fields = {}


# 计时线程,计算布局
class Thread_field(threading.Thread):
    def __init__(self, users):
        threading.Thread.__init__(self)
        self.num = len(users)
        self.users = users
        self.turn_id = users[0]
        self.turn_index = 0
        self.field = [[0] * 20 for i in range(20)]
        self.is_end = False
        self.winner = []
        self.loser = []

    def next_field(self, old_field):
        if self.num == 1:
            self.field = strategy.one_gamer_strategy(old_field)
        elif self.num == 2:
            self.field = strategy.two_gamer_strategy(old_field)
        elif self.num == 3:
            self.field = strategy.three_gamer_strategy(old_field)
        elif self.num == 4:
            self.field = strategy.four_gamer_strategy(old_field)

    def run(self):
        current_time = 0
        while True:
            current_time += 5
            time.sleep(5)
            t_index = self.turn_index
            t_index += 1
            if t_index == len(self.users):
                t_index = 0
            self.turn_index = t_index
            self.turn_id = self.users[t_index]
            self.next_field(self.field)
            if current_time >= 180:
                self.is_end = True
                self.new_result()
                self._stop()
                break

    def new_result(self):
        front_field = field_to_front_end(self.field)
        result = []
        max = 0
        for i in range(self.num):
            result[i] = len(front_field[i])
            if result[i] > max:
                max = result[i]
        for i in range(result):
            if result[i] == max:
                self.winner.append(self.users[i])
            else:
                self.loser.append(self.users[i])

    def change(self, front_field):
        self.field = field_from_front_end(front_field)
        self.next_field(self.field)
        print('next field:%s' % self.field)


# 实时获得棋盘布局 room_id
def get_field(request):
    room_id = int(request.POST['room_id'])
    thread_field = thread_fields[room_id]
    field = thread_field.field
    print(field_to_front_end(field))
    return to_json({
        'field': field_to_front_end(field),
        'turn_id': thread_field.turn_id,
        'is_end': thread_field.is_end})


# 前端更改布局 field room_id
def change_field(request):
    room_id = int(request.POST['room_id'])
    field = json.loads(request.POST['field'])
    print('front post:%s' % field)
    thread_fields[room_id].change(field)
    return to_json({'response_code': 1})


# 游戏结束，游戏结果 room_id
def get_game_result(request):
    room_id = int(request.POST['room_id'])
    thread_field = thread_fields[room_id]
    winner = thread_field.winner
    loser = thread_field.loser
    thread_fields.pop(thread_field)
    response_dict = {}
    for w in winner:
        response_dict.update({w: True})
    for l in loser:
        response_dict.update({l: False})
    return to_json(response_dict)


# 退出房间
def exit_game(request):
    response = exit_room_by_id(request)
    return render(request, 'RoomSelect.html')

# def get_field_test(request):
#     field = strategy.one_gamer_strategy(strategy.field)
#     strategy.field = field
#     return HttpResponse(to_show(field))
#
#
# def to_show(a):
#     b = ''
#     for aa in a:
#         for aaa in aa:
#             if aaa == 0:
#                 aaa = '&nbsp'
#             b += str(aaa) + '&nbsp&nbsp'
#         b += '<br>'
#     b = '<a style="font-size:20px">' + b + '</a>'
#     return b
