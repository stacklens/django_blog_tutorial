# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
#引入UserCreationForm
from django.contrib.auth.forms import UserCreationForm
# 引入 Profile 模型
from .models import Profile

# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 注册用户表单
class UserRegisterForm(UserCreationForm):
    # 添加email到默认的UserCreationForm
    email = forms.EmailField(label = "Email")

    class Meta:
        model = User
        fields = ('username', 'email',)


# Profile的表单类
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # 定义表单包含的字段
        fields = ('phone', 'avatar', 'bio')
