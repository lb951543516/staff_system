from django.shortcuts import render, redirect
from django.urls import reverse

from libs.views import split_page
from staff.models import Staff
from libs.views import login_required


# 员工列表
@login_required
def staffList(request):
    staff_list = Staff.objects.all()

    # 分页
    context = split_page(request, staff_list, 5)
    return render(request, 'staffList.html', context=context)


# 删除员工
@login_required
def staff_delete(request):
    # 删除员工
    sid = request.GET.get('sid')
    staff = Staff.objects.get(pk=sid)
    staff.delete()

    # 获取其他用户
    # staff_list = Staff.objects.all()
    # context = split_page(request, staff_list, 5)
    # return render(request, 'staffList.html', context=context)
    return redirect(reverse('staff:staffList'))


# 修改员工信息
@login_required
def staff_update(request):
    if request.method == "GET":
        # 获取该员工信息
        sid = request.GET.get('sid')
        page = int(request.GET.get('page'))
        staff = Staff.objects.get(pk=sid)
        context = {
            'staff': staff,
            'sid': sid,
            'page': page
        }
        return render(request, 'staff_update.html', context=context)
    else:
        # 获取修改提交的信息
        sid = request.POST.get('sid')
        staff = Staff.objects.get(pk=sid)
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        # 修改数据库
        staff.name = name
        staff.age = age
        staff.gender = gender
        staff.save()

        return redirect(reverse('staff:staffList'))


# 查看员工信息
@login_required
def staff_info(request):
    # 获取该员工信息
    sid = request.GET.get('sid')
    page = int(request.GET.get('page'))
    staff = Staff.objects.get(pk=sid)
    context = {
        'staff': staff,
        'page': page,
    }
    return render(request, 'staff_info.html', context=context)


# 添加员工信息
@login_required
def add_staff(request):
    if request.method == "GET":
        return render(request, 'add_staff.html')
    else:
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        # 信息缺失 无法添加
        if (not name) or (not age) or (not gender):
            context = {
                'error': 0
            }
            return render(request, 'add_staff.html', context=context)

        staff = Staff(name=name, age=age, gender=gender)
        staff.save()

        return redirect(reverse('staff:staffList'))


# 查询员工(查询员工分页存在问题)
@login_required
def search_staff(request):
    # if request.method == "GET":
    #     # # 数据总数
    #     # staff_num = Staff.objects.filter(**search_info).count()
    #     # if staff_num == 0:
    #     #     context = {
    #     #         'error': 0
    #     #     }
    #     #     return render(request, 'search_staff.html', context=context)
    #     # else:
    #     #     staff_list = Staff.objects.filter(**search_info)
    #     #     context = split_page(request, staff_list, 10)
    #     #     return render(request, 'search_staff.html', context=context)
    #     pass
    # else:
    sid = request.POST.get('sid').strip()
    name = request.POST.get('name').strip()
    age = request.POST.get('age').strip()
    gender = request.POST.get('gender').strip()
    if gender == '男':
        gender = 1
    elif gender == '女':
        gender = 0

    # 多条件查询
    search_info = {}
    if sid:
        search_info['id'] = sid
    if name:
        search_info['name'] = name
    if age:
        search_info['age'] = age
    if gender:
        search_info['gender'] = gender

    # return redirect(reverse('staff:search_staff'))

    # 数据总数
    staff_num = Staff.objects.filter(**search_info).count()
    if staff_num == 0:
        context = {
            'error': 0
        }
        return render(request, 'search_staff.html', context=context)
    else:
        staff_list = Staff.objects.filter(**search_info)
        # context = split_page(request, staff_list, 5)
        context = {
            'staffs': staff_list
        }
        return render(request, 'search_staff.html', context=context)
