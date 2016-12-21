from game import models
from game.tool.tools import *


# 登录 username
def login(request):
    username = request.POST['username']
    # 查询,无结果就注册
    find_user = models.User.objects.filter(username=username)
    if not find_user:
        find_user = models.User.objects.create(username=username, win=0, fail=0)
    else:
        find_user = find_user[0]

    # 写读cookie
    user_cookie = {
        'id': find_user.id,
        'name': find_user.username,
        'win': find_user.win,
        'fail': find_user.fail
    }
    response = to_json({
        'response_code': 1, 'id': find_user.id,
        'name': find_user.username,
        'win': find_user.win,
        'fail': find_user.fail
    })
    if not request.COOKIES:
        response.set_cookie('user_cookie', user_cookie)
    return response


# 登录
def login_by_cookie(request):
    cookie = request.COOKIES
    if not cookie:
        return to_json({'response_code': -1})
    else:
        print(cookie)
        user_cookie = eval(cookie["user_cookie"])
        user_id = user_cookie['id']
        # 查询,无结果就注册
        find_user = models.User.objects.filter(id=user_id)
        if not find_user:
            find_user = models.User.objects.create(id=user_id, user_name=user_cookie['name'])
        else:
            find_user = find_user[0]

        # 读cookie
        response = to_json({
            'response_code': 1,
            'id': find_user.id,
            'name': find_user.username,
            'win': find_user.win,
            'fail': find_user.fail
        })
        response.set_cookie('user_cookie', user_cookie)
        return response
