from django.shortcuts import render, redirect
from django.urls import reverse

from user_operation.models import User


def login(request):
    if request.method == "POST":
        # 获取登录信息
        username = request.POST.get('username')
        password = request.POST.get('password')
        yzm = int(request.POST.get('yzm'))
        # 验证验证码是否正确
        if yzm == 0:
            context = {
                'error': 2
            }
            return render(request, 'login.html', context=context)

        # user库中查询是否存在，密码是否相同
        user_num = User.objects.filter(username=username).count()
        if user_num == 0:
            context = {
                'error': 1
            }
            return render(request, 'login.html', context=context)
        else:
            user = User.objects.filter(username=username)[0]
            if user.password != password:
                context = {
                    'error': 0
                }
                return render(request, 'login.html', context=context)
            else:
                # 设置session 登录成功
                request.session['username'] = username

                return redirect(reverse('staff:staffList'))
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        # 获取注册信息
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        # 判断密码
        if not password or password2 != password or not 6 <= len(password) <= 12:
            context = {
                'error': 1
            }
            return render(request, 'register.html', context=context)
        # 判断用户名
        user_num = User.objects.filter(username=username).count()
        if user_num == 1 or not 6 <= len(username) <= 12:
            context = {
                'error': 0
            }
            return render(request, 'register.html', context=context)

        # 信息添加到user数据库
        user = User(username=username, password=password, age=age, gender=gender)
        user.save()
        return redirect(reverse('user_op:login'))
    else:
        return render(request, 'register.html')


def logout(request):
    response = redirect(reverse('user_op:login'))
    # 删除session
    request.session.flush()
    return response
