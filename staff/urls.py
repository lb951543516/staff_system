from django.conf.urls import url

from staff import views

urlpatterns = [
    # 查看员工列表
    url(r'^staffList/', views.staffList, name='staffList'),

    # 删除员工
    url(r'^staff_delete/', views.staff_delete, name='staff_delete'),

    # 更新员工信息
    url(r'^staff_update/', views.staff_update, name='staff_update'),

    # 查看员工信息
    url(r'^staff_info/', views.staff_info, name='staff_info'),

    # 添加新员工
    url(r'add_staff/', views.add_staff, name='add_staff'),

    # 查询员工
    url(r'search_staff/', views.search_staff, name='search_staff'),

]
