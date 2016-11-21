from django.conf.urls import url
from django.contrib import admin

from game import views
from game.method import in_room
from game.method import user, in_game, ready_game

urlpatterns = [
    url(r'^admin', admin.site.urls),  # 系统自带
    url(r'^$', views.room_select),  # 首页
    url(r'^room', views.room),
    url(r'^login$', user.login),  # 登录
    url(r'^login_by_cookie', user.login_by_cookie),  # 通过cookie登录
    url(r'^get_rooms$', in_room.get_rooms),  # 获得分页信息
    url(r'^new_room$', in_room.new_room),  # 新建房间
    url(r'^join_room_by_id$', in_room.join_room_by_id),  # 进入指定房间
    url(r'^join_room_random$', in_room.join_room_random),  # 进入指定房间
    url(r'^exit_room_by_id$', in_room.exit_room_by_id),  # 进入指定房间
    url(r'^check_room_status$', ready_game.check_room_status),  # 检查是否开始
    url(r'^user_ready$', ready_game.user_ready),  # 用户准备
    url(r'^user_cancel_ready$', ready_game.user_cancel_ready),  # 用户取消准备
    url(r'^owner_begin$', ready_game.owner_begin),  # 房主开始

    url(r'^get_field_test', in_game.get_field_test),  # 获得页面信息
]
