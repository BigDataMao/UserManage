from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 获取当前用户访问的url
        if request.path_info in ["/login/", "/image/code/", "/captcha/"]:
            return None
        # 判断当前用户是否已经登录
        if request.session.get("username"):
            return None
        return redirect("/login/")

