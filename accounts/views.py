from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    """用户注册"""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)  # 注册后自动登录
            messages.success(request, '注册成功！欢迎加入！')
            return redirect('blogs:index')

    return render(request, 'registration/register.html', {'form': form})
