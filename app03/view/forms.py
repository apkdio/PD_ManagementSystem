from django import forms

from app03.models import Consumer
from app03.models import Userinfo


# 以下是一个modelform表单
class user(forms.ModelForm):
    # name= forms.CharField(min_length=3,label="用户名") 对name添加条件验证
    class Meta:
        model = Userinfo
        fields = "__all__"
        # 如果只想让表单有一部分数据
        # fields=["name","age","gender"]
        # 对某些数据改变样式
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 重新定义init方法
        for name, field in self.fields.items():
            # if name == "time":
            #     field.widget = forms.DateInput(
            #         attrs={'type': 'date', 'class': 'form-control', 'placeholder': field.label})  # 对某一个单独设置
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}
    # 循环获得所有字段,并应用css效果


class supermanager(forms.Form):
    name = forms.CharField(label="用户名", widget=forms.TextInput(), required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 重新定义init方法
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}


class supermanager_edit(forms.Form):
    name = forms.CharField(label="用户名", widget=forms.TextInput(), required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True), required=True)
    new_password = forms.CharField(label="新密码", widget=forms.PasswordInput(render_value=True), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 重新定义init方法
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}


class manager(forms.Form):
    name = forms.CharField(label="用户名", widget=forms.TextInput(), required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)
    code = forms.CharField(label="验证码", widget=forms.TextInput(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 重新定义init方法
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}


class consumer(forms.ModelForm):
    class Meta:
        model = Consumer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}
