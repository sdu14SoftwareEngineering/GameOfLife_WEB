import json

from django.http import HttpResponse


def to_json(dist):
    return HttpResponse(json.dumps(dist))


def field_from_front_end(field):
    '''接受从前端发来的场地，转换成算法接受的样子'''
    target_field = [[0] * 20 for i in range(20)]
    for i, user_points in enumerate(field):
        user_num = i + 1
        for j in user_points:
            target_field[int(j[0])][int(j[1])] = user_num
    return target_field


def field_to_front_end(field):
    '''接受算法结束后的场地，转换成前端接受的样子'''
    target_field = [[], [], [], []]
    for i in range(20):
        for j in range(20):
            if field[i][j] != 0:
                target_field[field[i][j] - 1].append([i, j])
    return target_field
