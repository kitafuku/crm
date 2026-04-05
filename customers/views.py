from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from accounts.models import CustomUser
from .forms import CustomerForm
from .models import Customer


@login_required
def dashboard(request):
    total = Customer.objects.count()
    my_count = Customer.objects.filter(assigned_user=request.user).count()
    recent = Customer.objects.select_related('assigned_user').order_by('-updated_at')[:5]
    corp_count = Customer.objects.filter(attribute='corporate').count()
    indiv_count = Customer.objects.filter(attribute='individual').count()
    gov_count = Customer.objects.filter(attribute='government').count()
    return render(request, 'customers/dashboard.html', {
        'total': total,
        'my_count': my_count,
        'recent': recent,
        'corp_count': corp_count,
        'indiv_count': indiv_count,
        'gov_count': gov_count,
    })


@login_required
def customer_list(request):
    qs = Customer.objects.select_related('assigned_user').order_by('customer_id')

    q = request.GET.get('q', '').strip()
    attribute = request.GET.get('attribute', '')
    assigned = request.GET.get('assigned', '')
    industry = request.GET.get('industry', '')

    if q:
        qs = qs.filter(name__icontains=q)
    if attribute:
        qs = qs.filter(attribute=attribute)
    if assigned:
        qs = qs.filter(assigned_user_id=assigned)
    if industry:
        qs = qs.filter(industry=industry)

    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))

    users = CustomUser.objects.filter(is_active=True).order_by('name')
    industries = Customer.INDUSTRY_CHOICES

    return render(request, 'customers/customer_list.html', {
        'page': page,
        'total_count': qs.count(),
        'q': q,
        'attribute': attribute,
        'assigned': assigned,
        'industry': industry,
        'users': users,
        'industries': industries,
        'attr_choices': Customer.ATTR_CHOICES,
    })


@login_required
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'顧客「{form.instance.name}」を登録しました')
        return redirect('customer_list')
    return render(request, 'customers/customer_form.html', {'form': form, 'action': '登録'})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'顧客「{customer.name}」を更新しました')
        return redirect('customer_list')
    return render(request, 'customers/customer_form.html', {'form': form, 'action': '編集', 'customer': customer})


@login_required
@require_POST
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    name = customer.name
    customer.delete()
    messages.success(request, f'顧客「{name}」を削除しました')
    return redirect('customer_list')
