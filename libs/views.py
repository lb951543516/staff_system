from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from functools import wraps
from django.urls import reverse


# 分页
def split_page(request, object_list, per_page):
    # 获取当前页码
    get_page = int(request.GET.get('page', 1))

    # 创建分页对象，每页2个
    paginator = Paginator(object_list, per_page)

    # 根据页码从分页器中取出对应页的数据
    try:
        page = paginator.page(get_page)
    except PageNotAnInteger:
        # 不是整数返回第一页数据
        page = paginator.page('1')
        get_page = 1
    except EmptyPage:
        # 当参数页码大于或小于页码范围时,会触发该异常
        if get_page > paginator.num_pages:
            # 大于 获取最后一页数据返回
            page = paginator.page(paginator.num_pages)
        else:
            # 小于 获取第一页
            page = paginator.page(1)

    # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10
    if get_page <= 5:
        if paginator.num_pages >= 10:
            start, end = 1, 10
        else:
            start, end = 1, paginator.num_pages
    # 结束页码范围
    elif get_page > (paginator.num_pages - 5):
        if (paginator.num_pages - 9) > 1:
            start, end = paginator.num_pages - 9, paginator.num_pages
        else:
            start, end = 1, paginator.num_pages

    else:
        start, end = get_page - 4, get_page + 5

    page_range = range(start, end + 1)
    return {'page': page, 'paginator': paginator, 'page_range': page_range}


# 登录认证
def login_required(func):
    @wraps(func)
    # 函数被装饰器装饰后 会变成装饰器的内部函数
    # wraps可以防止发生这种情况，让被装饰的函数保持其本身
    def check_session(request):
        username = request.session.get('username')
        if not username:
            return redirect(reverse('user_op:login'))
        else:
            return func(request)

    return check_session
