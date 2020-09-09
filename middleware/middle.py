from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class Login_required(MiddlewareMixin):
    def process_request(self, request):
        url = request.path
        print(url)
        white_list = ['/user_op/login/', '/user_op/register/']
        username = request.session.get('username')
        if not username:
            if not (url in white_list):
                return redirect(reverse('user_op:login'))
