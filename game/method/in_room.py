import random

import math

from django.shortcuts import render
from django.template import Context

from game.tool.room_tool import *
from game.tool.tools import *


def creat_test_room(request):
    # 新房间
    room = Room(len(rooms_list), 'test')
    room.owner = 111
    room.users = [111, 222]
    room.users_status = {111: False, 222: False}
    # 添加
    rooms_list.append(room)
    return to_json({'room_id': len(rooms_list)})


# 新建房间 user_id room_name,暂时不考虑重名
def new_room(request):
    user_id = int(request.POST.get('user_id'))
    room_name = request.POST.get('room_name')
    # 新房间
    room = Room(len(rooms_list), room_name)
    room.owner = user_id
    room.users.append(user_id)
    room.users_status.update({user_id: False})
    # 添加
    rooms_list.append(room)

    # 跳转至房间页面
    return to_json({'response_code': 1, 'room_id': room.id})


# 获取房间，分页 page
def get_rooms(request):
    print(rooms_list)
    page = int(request.POST.get('page'))
    if page is None:
        page = 0
    ready_rooms = []
    game_rooms = []
    for r in rooms_list:
        if r.status:
            game_rooms.append(r)
        else:
            ready_rooms.append(r)
    response_rooms = ready_rooms + game_rooms
    # 页数
    response_code = 1
    len_response_rooms = len(response_rooms)
    pages = len_response_rooms / 12.0
    need_rooms = []
    if 0 < pages - page < 1:
        last_page = len_response_rooms - page * 12
        need_rooms = response_rooms[len_response_rooms - last_page:len_response_rooms]
    elif pages - page >= 1:
        need_rooms = response_rooms[page * 12:(page * 12 + 12)]
    else:
        response_code = -1
    # 返回
    response_list = []
    for r in need_rooms:
        response_list.append({
            'id': r.id,
            'name': r.name,
            'owner': r.owner,
            'user_num': len(r.users),
            'status': r.status
        })
    if response_code == 1:
        print(response_list)
        return to_json({
            'response_code': response_code,
            'max_page': math.ceil(pages),
            'rooms': response_list
        })
    else:
        print(response_list)
        return to_json({'response_code': response_code})


# 加入指定房间 user_id room_id
def join_room_by_id(request):
    user_id = int(request.POST.get('user_id'))
    room_id = int(request.POST.get('room_id'))
    # 找到
    room = get_room_by_id(room_id)
    # 添加
    room.users.append(user_id)
    room.users_status.update({user_id: False})
    return to_json({'response_code': 1})


# 加入指定房间 user_id room_name
def join_room_by_name(request):
    user_id = request.POST.get('user_id')
    room_name = request.POST.get('room_name')
    # 找到
    room = get_room_by_name(room_name)
    # 添加
    room.users.append(user_id)
    room.users_status.update({user_id: False})
    return room.id


# 快速加入 user_id
def join_room_random(request):
    user_id = request.POST.get('user_id')
    r_list = []
    for r in rooms_list:
        if (not r.status) and len(r.users) < 4:
            r_list.append(r)

    # 如果没有空房间了
    if len(r_list) == 0:
        return to_json({
            'response_code': -1,
            'error_msg': '没有空房间'
        })

    # 随机出房间
    room = r_list[random.randint(0, len(r_list) - 1)]
    # 添加
    room.users.append(user_id)
    room.users_status.update({user_id: False})
    return to_json({
        'response_code': 1,
        'room_id': room.id
    })


# 退出房间 user_id room_id
def exit_room_by_id(request):
    user_id = int(request.POST.get('user_id'))
    room_id = int(request.POST.get('room_id'))
    # 找到房间
    room = get_room_by_id(room_id)
    f = False
    ff = False
    for u_id in room.users:
        if u_id == user_id:
            f = True
            break
    if not f:  # 如果这个房间没有此人
        for r in rooms_list:
            for u_id in r:
                if u_id == user_id:
                    ff = True
                    break
            if ff:
                room = r
                break

    if f or ff:
        room.users.remove(user_id)  # 移除此人
        room.users_status.pop(user_id)
        if len(room.users) > 0 and room.owner not in room.users:
            room.owner = room.users[0]  # 房主更换
        if len(room.users) == 0:
            rooms_list.remove(room)  # 房间没人，删除
    else:
        return HttpResponse(-1)  # 这个人不在房间中


# 搜索房间 room_name page
def search_room(request):
    room_name = request.POST.get('room_name')
    page = request.POST.get('page')
    result_rooms = []
    # 搜索
    for r in rooms_list:
        if room_name in r.name:
            result_rooms.append(r)

    # 页数
    response_code = 1
    len_result_rooms = len(result_rooms)
    pages = len_result_rooms / 12.0
    need_rooms = []
    if 0 < pages - page < 1:
        last_page = len_result_rooms - page * 12
        need_rooms = result_rooms[len_result_rooms - last_page:len_result_rooms]
    elif pages - page >= 1:
        need_rooms = result_rooms[page * 12:(page * 12 + 12)]
    else:
        response_code = -1

    # 返回
    response_list = []
    for r in need_rooms:
        response_list.append({
            'id': r.id,
            'name': r.name,
            'owner': r.owner,
            'user_num': len(r.users),
            'status': r.status
        })
    if response_code == 1:
        return to_json({
            'response_code': response_code,
            'max_page': math.ceil(pages),
            'rooms': need_rooms
        })
    else:
        return to_json({'response_code': response_code})
