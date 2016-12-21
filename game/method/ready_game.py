from game import models
from game.method.in_game import thread_fields, Thread_field
from game.tool.room_tool import *
from game.tool.tools import to_json


# 实时获得房间信息 room_id
def get_room_info(request):
    room_id = int(request.POST['room_id'])
    room = get_room_by_id(room_id)
    print(room_id)
    print(room.users_status)
    users_array = []
    for u_id in room.users:
        find_user = models.User.objects.filter(id=u_id)
        if find_user:
            find_user = find_user[0]
        u_dict = {
            'user_id': find_user.id,
            'user_name': find_user.username,
            'win': find_user.win,
            'fail': find_user.fail,
            'user_status': room.users_status[u_id]
        }
        users_array.append(u_dict)
    # 结果
    response = {
        'status': room.status,
        'owner': room.owner,
        'users': users_array
    }
    print(response)
    return to_json(response)


# 更改准备状态 room_id user_id
def change_user_status(request):
    user_id = int(request.POST['user_id'])
    room_id = int(request.POST['room_id'])
    room = get_room_by_id(room_id)
    u_status = room.users_status[user_id]
    room.users_status[user_id] = not u_status
    return to_json({'response_code': 1, 'user_status': not u_status})


# 房主开始游戏 user_id room_id
def begin_game(request):
    user_id = int(request.POST['user_id'])
    room_id = int(request.POST['room_id'])
    room = get_room_by_id(room_id)
    if user_id == room.owner:
        f = True
        for u_id in room.users:
            if u_id != room.owner and not room.users_status[u_id]:
                f = False
        if f:
            room.users_status[user_id] = True
            room.status = True
            # 计算布局线程,存入线程
            thread_fields[room_id] = Thread_field(room.users, room_id)
            thread_fields[room_id].start()
            return to_json({'response_code': 1})
        else:
            return to_json({'response_code': -1})
    else:
        return to_json({'response_code': -1})

# # 用户准备 user_id room_id
# def user_ready(request):
#     user_id = request.POST.get('user_id')
#     room_id = request.POST.get('room_id')
#     # 找到此房间
#     room = get_room_by_id(room_id)
#     room.users_status[user_id] = True
#
#
# # 用户取消准备 user_id room_id
# def user_cancel_ready(request):
#     user_id = request.POST.get('user_id')
#     room_id = request.POST.get('room_id')
#     # 找到此房间
#     room = get_room_by_id(room_id)
#     room.users_status[user_id] = False
#
#
# # 开始游戏 owner_id room_id
# def owner_begin(request):
#     owner_id = request.POST.get('owner_id')
#     room_id = request.POST.get('room_id')
#     # 找到此房间
#     room = get_room_by_id(room_id)
#     room.users_status[owner_id] = True
#     all_ready = True
#     if room_id == room.owner:
#         for u in room.users:
#             if not room.users_status[u]:
#                 all_ready = False
#                 break
#         if all_ready:
#             # 全部准备好
#             room.status = True
#             return 0
#         else:
#             # 有人没有准备好
#             return 0
#     else:
#         # 这个人不是房主
#         return 0
#
#
# # 检查是否开始游戏了 room_id
# def check_room_status(request):
#     room_id = request.POST.get('room_id')
#     # 找到此房间
#     room = get_room_by_id(room_id)
#     if room.status:
#         # 已经开始了
#         return 0
#     else:
#         # 还没有开始
#         return 0
