from django.contrib.auth.backends import ModelBackend
import re
from .models import User


class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户认证后端"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写认证方法,实现多账号登录
        :param request:
        :param username:
        :param password:
        :param kwargs:
        :return:
        """
        # 根据传入的username获取user对象, username可以使手机号亦可以是正好
        user = self.get_user_by_account(username)

        # 检验user是否存在并校验密码是否正确
        if user and user.check_password(password):
            return user


    @staticmethod
    def get_user_by_account(account):
        """
        根据account查询用户
        :param account: 用户名或手机号
        :return:
        """

        try:
            if re.match('^1[3-9]\d{9}$', account):
                # 手机号登录
                user = User.objects.get(mobile=account)
            else:

                # 用户名登录
                user = User.objects.get(username=account)

        except User.DoesNotExist:
            return None
        else:
            return  user
