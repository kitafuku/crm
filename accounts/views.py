from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import LoginForm, UserCreateForm, UserEditForm
from .models import CustomUser


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next', 'dashboard'))
    return render(request, 'accounts/login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin:
            messages.error(request, 'この操作には管理者権限が必要です')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def user_list(request):
    users = CustomUser.objects.all().order_by('role', 'name')
    total = users.count()
    admin_count = users.filter(role='admin').count()
    active_count = users.filter(is_active=True).count()
    return render(request, 'accounts/user_list.html', {
        'users': users,
        'total': total,
        'admin_count': admin_count,
        'active_count': active_count,
    })


@admin_required
def user_create(request):
    form = UserCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'ユーザーを登録しました')
        return redirect('user_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'action': '登録'})


@admin_required
def user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    form = UserEditForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'ユーザー情報を更新しました')
        return redirect('user_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'action': '編集', 'target_user': user})


@admin_required
@require_POST
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if user.pk == request.user.pk:
        messages.error(request, '自分自身のアカウントは削除できません')
    else:
        user.delete()
        messages.success(request, 'ユーザーを削除しました')
    return redirect('user_list')
