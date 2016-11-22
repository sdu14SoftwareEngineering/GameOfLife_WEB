import threading

import time

from django.shortcuts import render

from game import models
from game.method.in_room import exit_room_by_id
from game.tool import strategy, room_tool
from game.tool.tools import *

# 所有房间布局
thread_fields = {}
# 轮到谁了
thread_turn = {}


# 计时线程
class Thread_count(threading.Thread):
    def __init__(self, users):
        threading.Thread.__init__(self)
        self.users = users
        self.turn_id = users[0]
        self.turn_index = 0

    def run(self):
        while True:
            time.sleep(10)
            t_index = self.turn_index
            t_index += 1
            if t_index == len(self.users):
                t_index = 0
            self.turn_index = t_index
            self.turn_id = self.users[t_index]


# 计算布局
class Thread_field(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num
        self.field = [[0] * 20 for i in range(20)]

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
        while True:
            time.sleep(5)
            self.next_field(self.field)

    def change(self, front_field):
        self.field = field_from_front_end(front_field)
        self.next_field(self.field)


# 实时获得房间信息 room_id
def get_room_info(request):
    room_id = int(request.POST['room_id'])
    room = room_tool.get_room_by_id(room_id)
    users_array = []
    for u_id in room.users:
        find_user = models.User.objects.filter(id=u_id)
        if find_user:
            find_user = find_user[0]
        u_dict = {
            'user_name': find_user.username,
            'win': find_user.win,
            'fail': find_user.fail,
            'user_status': room.users_status[u_id]
        }
        users_array.append(u_dict)
    # 结果
    response = {
        'status': False,
        'owner': room.owner,
        'users': users_array
    }
    return to_json(response)


# 更改准备状态 room_id user_id
def change_user_status(request):
    user_id = int(request.POST['user_id'])
    room_id = int(request.POST['room_id'])
    room = room_tool.get_room_by_id(room_id)
    u_status = room.users_status[user_id]
    room.users_status[user_id] = not u_status
    return to_json({'response_code': 1, 'user_status': not u_status})


# 房主开始游戏 user_id room_id
def begin_game(request):
    user_id = int(request.POST['user_id'])
    room_id = int(request.POST['room_id'])
    room = room_tool.get_room_by_id(room_id)
    if user_id == room.owner:
        room.users_status[user_id] = True
        f = True
        for u_status in room.users_status:
            if not u_status:
                f = False
        if f:
            # 计算布局线程,存入布局
            thread_fields[room_id] = Thread_field(len(room.users))
            thread_fields[room_id].start()
            # 开启计时线程,存入线程
            thread_turn[room_id] = Thread_count(room.users)
            thread_turn[room_id].start()
            return to_json({'response_code': 1})


# 实时获得棋盘布局 room_id
def get_field(request):
    room_id = int(request.POST['room_id'])
    field = thread_fields[room_id].field
    return to_json({
        'field': field_to_front_end(field),
        'turn_id': thread_turn[room_id].turn_id})


# 前端更改布局 field room_id
def change_field(request):
    room_id = int(request.POST['room_id'])
    field = request.POST['field']
    thread_fields[room_id].change(field)
    return to_json({'response_code': 1})


# 游戏结束，游戏结果
def get_game_result(request):
    return 0


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
