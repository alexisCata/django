from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import BankUserForm, BankAccountForm
from .models import BankUser, BankAccount


@login_required
def list_users(request):
    """
    return all the users to home screen
    :param request: 
    :return: 
    """
    users = BankUser.objects.all()
    return render(request, 'core/home.html', {'users': users, 'user': request.user})


@login_required
def add_user(request):
    """
    add new bankuser object
    :param request: 
    :return: 
    """
    form = BankUserForm(request.POST or None)

    if form.is_valid():
        form = form.save(commit=False)
        form.owner = request.user
        form.save()

        bankuser = BankUser.objects.get(id=form.id)

        if 'save' in request.POST:
            return redirect('home')
        elif 'save_and_add_ba' in request.POST:
            return redirect('add_bank_account', bankuser.id)

    return render(request, 'core/user.html', {'form': form})


@login_required
def add_bank_account(request, id):
    """
    delete bankaccount object 
    :param request: 
    :param id: bankuser_id 
    :return: 
    """
    form = BankAccountForm(request.POST or None)

    if form.is_valid():
        form = form.save(commit=False)

        bankuser = BankUser.objects.get(id=id)
        form.bank_user = bankuser
        form.save()

        return redirect('update_user', bankuser.id)

    return render(request, 'core/add_bank_account.html', {'form': form})


@login_required
def delete_bank_account(request, id):
    """
    delete bankaccount object 
    :param request: 
    :param id: bankuser_id 
    :return: 
    """
    account = BankAccount.objects.get(id=id)
    user_id = account.bank_user.id

    if request.method == 'POST':
        if "delete" in request.POST:
            account.delete()
        return redirect('update_user', user_id)

    return render(request, 'core/delete_confirm.html', {'account_to_delete': account})


@login_required
def update_user(request, id):
    """
    update bankuser data
    :param request: 
    :param id: 
    :return: 
    """
    if request.POST and 'cancel' in request.POST:
        return redirect('home')

    user = BankUser.objects.get(id=id)
    form = BankUserForm(request.POST or None, instance=user)

    accounts = user.bankaccount_set.all()

    if form.is_valid():
        form.save()
        if 'save' in request.POST:
            return redirect('home')
        elif 'save_and_add_ba' in request.POST:
            return redirect('add_bank_account', user.id)

    return render(request, 'core/user.html',
                  {'form': form, 'user': request.user, 'bank_user': user, 'accounts': accounts})


@login_required
def delete_user(request, id):
    """
    delete bankuser
    :param request: 
    :param id: 
    :return: 
    """
    user = BankUser.objects.get(id=id)

    if request.method == 'POST':
        if "delete" in request.POST:
            user.delete()
            return redirect('home')
        else:
            return redirect('update_user', id)

    return render(request, 'core/delete_confirm.html', {'user_to_delete': user})
