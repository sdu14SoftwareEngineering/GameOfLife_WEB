from game.tool.room_tool import *


# 用户准备 user_id room_id
def user_ready(request):
    user_id = request.POST.get('user_id')
    room_id = request.POST.get('room_id')
    # 找到此房间
    room = get_room_by_id(room_id)
    room.users_status[user_id] = True


# 用户取消准备 user_id room_id
def user_cancel_ready(request):
    user_id = request.POST.get('user_id')
    room_id = request.POST.get('room_id')
    # 找到此房间
    room = get_room_by_id(room_id)
    room.users_status[user_id] = False


# 开始游戏 owner_id room_id
def owner_begin(request):
    owner_id = request.POST.get('owner_id')
    room_id = request.POST.get('room_id')
    # 找到此房间
    room = get_room_by_id(room_id)
    room.users_status[owner_id] = True
    all_ready = True
    if room_id == room.owner:
        for u in room.users:
            if not room.users_status[u]:
                all_ready = False
                break
        if all_ready:
            # 全部准备好
            room.status = True
            return 0
        else:
            # 有人没有准备好
            return 0
    else:
        # 这个人不是房主
        return 0


# 检查是否开始游戏了 room_id
def check_room_status(request):
    room_id = request.POST.get('room_id')
    # 找到此房间
    room = get_room_by_id(room_id)
    if room.status:
        # 已经开始了
        return 0
    else:
        # 还没有开始
        return 0
