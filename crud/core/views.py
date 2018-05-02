from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import BankUser, BankAccount
from .forms import BankUserForm
from django.shortcuts import reverse

@login_required
def list_users(request):
    users = BankUser.objects.filter(owner=request.user)
    return render(request, 'core/home.html', {'users': users})


@login_required
def add_user(request):

    form = BankUserForm(request.POST or None)

    if form.is_valid():
        form = form.save(commit=False)
        form.owner = request.user
        form.save()
        return redirect('home')

    return render(request, 'core/add.html', {'form': form})


@login_required
def update_user(request, id):

    user = BankUser.objects.get(id=id)
    form = BankUserForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'core/add.html', {'form': form, 'user': request.user, 'bank_user': user})


@login_required
def delete_user(request, id):

    user = BankUser.objects.get(id=id)
    form = BankUserForm(request.POST or None, instance=user)

    if request.method == 'POST':
        user.delete()
        return redirect('home')

    return render(request, 'core/delete_confirm.html', {'user_to_delete': user})

