from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from .forms import BankUserForm, BankAccountForm
from .models import BankUser, BankAccount


@login_required
def list_users(request):
    print(request)
    users = BankUser.objects.filter(owner=request.user)
    return render(request, 'core/home.html', {'users': users})


# @login_required
# def add_user(request):
#     form = BankUserForm(request.POST or None)
#
#     AccountFormSet = inlineformset_factory(BankUser, BankAccount, form=BankAccountForm, fields=('IBAN',), fk_name='bank_user')
#     bankuser = BankUser()
#     formset = AccountFormSet(request.POST or None, instance=bankuser, prefix='form')
#
#     if form.is_valid():
#         prev = form
#         form = form.save(commit=False)
#         form.owner = request.user
#         form.save()
#
#         bankuser = BankUser.objects.get(id=form.id)
#
#         formset = AccountFormSet(request.POST, instance=bankuser, prefix='form')
#         if formset.is_valid():
#             formset.save()
#             return redirect('home')
#         else:
#             bankuser.delete()
#             form = prev
#             # formset._errors = formset.non_form_errors()
#
#     return render(request, 'core/add.html', {'form': form, 'formset': formset})

@login_required
def add_user(request):
    form = BankUserForm(request.POST or None)

    # AccountFormSet = inlineformset_factory(BankUser, BankAccount, form=BankAccountForm, fields=('IBAN',), fk_name='bank_user')
    # bankuser = BankUser()
    # formset = AccountFormSet(request.POST or None, instance=bankuser, prefix='form')

    if form.is_valid():
        prev = form
        form = form.save(commit=False)
        form.owner = request.user
        form.save()

        bankuser = BankUser.objects.get(id=form.id)

        if 'save' in request.POST:
            return redirect('home')
        elif 'save_and_add_ba' in request.POST:
            return redirect('add_bank_account', bankuser.id)

        # formset = AccountFormSet(request.POST, instance=bankuser, prefix='form')
        # if formset.is_valid():
        #     formset.save()
        #     return redirect('home')
        # else:
        #     bankuser.delete()
        #     form = prev
            # formset._errors = formset.non_form_errors()

    return render(request, 'core/add.html', {'form': form})#, 'formset': formset})


@login_required
def add_bank_account(request, id):
    form = BankAccountForm(request.POST or None)

    if form.is_valid():
        form = form.save(commit=False)

        bankuser = BankUser.objects.get(id=id)
        form.bank_user = bankuser
        form.save()

        return redirect('update_user', bankuser.id)

        # formset = AccountFormSet(request.POST, instance=bankuser, prefix='form')
        # if formset.is_valid():
        #     formset.save()
        #     return redirect('home')
        # else:
        #     bankuser.delete()
        #     form = prev
            # formset._errors = formset.non_form_errors()

    return render(request, 'core/add_bank_account.html', {'form': form})#, 'formset': formset})


@login_required
def update_user(request, id):
    if request.POST and 'cancel' in request.POST:
        return redirect('home')

    user = BankUser.objects.get(id=id)
    form = BankUserForm(request.POST or None, instance=user)

    accounts= user.bankaccount_set.all()

    # AccountFormSet = inlineformset_factory(BankUser, BankAccount, fields=('IBAN',))
    # formset = AccountFormSet(request.POST or None, instance=user, prefix='form')

    if form.is_valid(): # and formset.is_valid():
        form.save()
        if 'save' in request.POST:
            return redirect('home')
        elif 'save_and_add_ba' in request.POST:
            return redirect('add_bank_account', user.id)



    return render(request, 'core/add.html',
                  {'form': form, 'user': request.user, 'bank_user': user, 'accounts': accounts})#'formset': formset})


@login_required
def delete_user(request, id):
    user = BankUser.objects.get(id=id)

    if request.method == 'POST':
        if "delete" in request.POST:
            user.delete()
            return redirect('home')
        else:
            return redirect('update_user', id)

    return render(request, 'core/delete_confirm.html', {'user_to_delete': user})
