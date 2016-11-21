from game.models import User

# 存储在内存中的所有房间
rooms_list = []


class Room(object):
    id = int  # 房间id
    name = str  # 房间名
    owner = int  # 房主id
    users = []  # 成员id
    users_status = {}  # 成员准备状态
    status = False  # 状态

    def __init__(self, id, name):
        self.id = id
        self.name = name


# 获取全部房间
def get_all_rooms():
    return rooms_list


# 获取某个房间 id
def get_room_by_id(id):
    for room in rooms_list:
        if room.id == id:
            return room
    return None


# 获取某个房间name
def get_room_by_name(name):
    for room in rooms_list:
        if room.name == name:
            return room
    return None


# 添加
def add_room(new_room):
    rooms_list.append(new_room)
    return 1


# 删除
def del_room(id):
    for room in rooms_list:
        if room.id == id:
            rooms_list.remove(room)
            return 1
    return -1
