import re

from django import http
from django.contrib.auth import authenticate
from django.contrib.auth.views import login, logout
from django.db import DatabaseError
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from apps.users.models import User
from utils.response_code import RETCODE


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        return render(request, 'register.html')

    def post(self, request):
        """
        实现用户注册
        :param request: 请求对象
        :return: 注册结果
        """
        # 1, 获取参数
        #1.0 获取用户名
        username = request.POST.get('username')
        # 1.1 获取密码
        password = request.POST.get('password')
        # 1.2 获取确认密码
        password2 = request.POST.get('password2')
        # 1.3 获取手机号
        mobile = request.POST.get('mobile')
        # 获取用户是否同意协议
        allow = request.POST.get('allow')
        # 2, 检校参数
        # 2.0 获取参数是否为空
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseBadRequest('缺少参数')
        # 2.1 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return http.HttpResponseBadRequest('请输入5-20个字符的用户名')
        # 2.2 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseBadRequest('请输入8-20位的字符串')
        # 2.3 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseBadRequest('两个输入的密码不一致')
        # 2.4 判断手机号格式是否正确
        if not re.match(r'^1[3-9]\d{9}', mobile):
            return http.HttpResponseBadRequest('请输入正确的手机号')
        # 2.5 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseBadRequest('请勾选用户协议')


        # 3, 导入数据库中
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        # 实现状态保持
        login(request, user)

        # 4, 返回结果
        return redirect(reverse('index:index'))


class UsernameCountView(View):
    """判断用户名是否重复使用"""

    def get(self, request, username):
        """

        :param request:
        :param username:
        :return:
        """
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code':RETCODE.OK, 'errmsg': 'OK', 'count': count})



class MobileCountView(View):
    """判断手机号是否重复注册"""

    def get(self, request, mobile):
        """

        :param request:
        :param mobile:
        :return:
        """
        count= User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'code':RETCODE.OK, 'errmsg': 'OK', 'count': count})


class  Loginview(View):
    """登录页面"""
    def get(self,request):
         """
        提供登录页面
         :param request:
         :return:
         """
         return render(request, 'login.html')


    def post(self, request):
        """
        登录逻辑,
        :param request:
        :return:
        """

        # 接受参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')


        # 检验参数
        # 判断参数是否齐全
        if not all([username,password]):
            return http.HttpResponseBadRequest('缺少必传参数')

        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return render(request, 'login.html', {'account_errmsg': '请输入正确的用户名或手机号'})
        # 判断密码是否正确
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return render(request, 'login.html',{'account_errmsg': '密码最少8位, 最长20位'})

        # 认证登录用户
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})

        #实现状态保持
        login(request, user)
        # 设置状态保持的周期
        if remembered != 'on':
            # 没有记住用户: 浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            # 记住用户: None表示两周后过期
            request.session.set_expiry(None)
        # 响应登录结果
        response = redirect(reverse('index:index'))


        # 注册是用户名写入到cookie,有限期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        return response


class LoginOut(View):
    """退出登录"""

    def get(self, request):
        """
        实现退出登录, 清除session
        :param request:
        :return:
        """
        # 清除session
        logout(request)

        # 退出登录, 重定向到登录页面
        response = redirect(reverse('index:index'))

        # 退出登录时清除cookie中的username
        response.delete_cookie('username')

        return response






















