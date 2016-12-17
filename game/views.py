from django.shortcuts import render
from django.template import Context

from game.tool.room_tool import *
from game.tool.tools import to_json


def room_select(request):
    return render(request, 'RoomSelect.html', locals())


# room_id,user_id
def room(request):
    user_id = int(request.POST['user_id'])
    room_id = int(request.POST['room_id'])
    return render(request, 'room.html', Context({'my_id': user_id, 'room_id': room_id}))

