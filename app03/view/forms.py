import datetime
import re

from django import forms
from django.core.exceptions import ValidationError

from app03.models import Consumer, Userinfo, Department
from example01.settings import INITIAL_SETTING

depart_id = INITIAL_SETTING['depart_id']


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

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18:
            raise ValidationError('该数值需要大于18！')
        elif age > 100:
            raise ValidationError("不合理的数值！")
        else:
            return age

    def clean_account(self):
        account = int(self.cleaned_data['account'])
        if account < 0:
            raise ValidationError("该数值不能低于0！")
        else:
            return account

    def clean_time(self):
        time = self.cleaned_data['time']
        if time < datetime.date.today() - datetime.timedelta(days=365 * 100):
            raise ValidationError("只能设置为最近100年内时间!")
        else:
            return time

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 重新定义init方法
        for name, field in self.fields.items():
            # if name == "time":
            #     field.widget = forms.DateInput(
            #         attrs={'type': 'date', 'class': 'form-control', 'placeholder': field.label})  # 对某一个单独设置
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}
            if 'depart' in self.fields:
                self.fields['depart'].queryset = Department.objects.exclude(id=depart_id)
    # 循环获得所有字段,并应用css效果


class supermanager(forms.Form):
    name = forms.CharField(label="用户名", widget=forms.TextInput(), required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True), required=True)
    depart = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label="部门",
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}


class supermanager_edit(forms.Form):
    name = forms.CharField(label="用户名", widget=forms.TextInput(), required=True)
    password = forms.CharField(label="原密码", widget=forms.PasswordInput(render_value=True), required=True)
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True), required=True)
    new_password = forms.CharField(label="新密码", widget=forms.PasswordInput(render_value=True), required=True)
    depart = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label="部门",
        required=True
    )

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

    def clean_number(self):
        number = self.cleaned_data.get("number")
        regex = r'^1[3-9]\d{9}$'
        if not re.match(regex, number):
            raise forms.ValidationError("请输入有效的手机号码！")
        return number
