from django.shortcuts import render


def room_select(request):
    return render(request, 'RoomSelect.html', locals())


# room_id,user_id
def room(request):
    return render(request, 'room.html', locals())
