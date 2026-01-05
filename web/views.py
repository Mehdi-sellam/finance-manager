from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.utils.safestring import mark_safe
from .form import (
    LoginForm,
    NamespaceCreateForm,
    NamespaceUpdateForm,
    ChangePasswordForm,
    AccountCreateForm,
    AccountUpdateForm,
    TransactionFilterForm,
    TransactionInForm,
    TransactionOutForm,
    TransactionTransferForm,
    NamespaceSelectForm,
    AccountSelectForm,
)
import json
import requests

# Create your views here.
def _api_request(request, method, path, data=None, params=None):
    url = request.build_absolute_uri(path)
    headers = {
        'Content-Type': 'application/json',
    }
    token = request.session.get('auth_token')
    if token:
        headers['Authorization'] = f'Token {token}'
    try:
        resp = requests.request(method=method, url=url, json=data, params=params, headers=headers, timeout=10)
        if resp.ok:
            try:
                return resp.status_code, (resp.json() if resp.content else None)
            except ValueError:
                return resp.status_code, None
        try:
            err = resp.json()
        except ValueError:
            err = {'detail': resp.reason}
        return resp.status_code, err
    except requests.RequestException:
        return 503, {'detail': 'Service unavailable'}


def _apply_form_errors(form, payload):
    if not isinstance(payload, dict):
        return
    for k, v in payload.items():
        if k == 'detail':
            form.add_error(None, str(v))
        else:
            if isinstance(v, list):
                for msg in v:
                    form.add_error(k if k in form.fields else None, str(msg))
            else:
                form.add_error(k if k in form.fields else None, str(v))


def index(request):
    return render(request, 'web/index.html')


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            status_code, data = _api_request(
                request,
                'POST',
                '/api/auth/login/',
                {
                    'username': form.cleaned_data['username'],
                    'password': form.cleaned_data['password']
                }
            )
            if status_code == 200 and 'token' in data:
                request.session['auth_token'] = data['token']
                request.session['username'] = data.get('username')
                messages.success(request, 'Logged in successfully')
                username = request.session.get('username')
                if request.COOKIES.get(f'pwd_changed_{username}') == '1':
                    return redirect('index')
                return redirect('change-password')
            _apply_form_errors(form, data)
            messages.error(request, 'Login failed')
    else:
        form = LoginForm()
    return render(request, 'web/login.html', {'form': form})


@require_http_methods(["GET", "POST"])
def namespaces(request):
    if not request.session.get('auth_token'):
        return redirect('login')

    create_form = NamespaceCreateForm()
    if request.method == 'POST':
        create_form = NamespaceCreateForm(request.POST)
        if create_form.is_valid():
            status_code, data = _api_request(request, 'POST', '/api/namespaces/', {
                'name': create_form.cleaned_data['name']
            })
            if status_code == 201:
                messages.success(request, 'Namespace created')
                return redirect('namespaces')
            _apply_form_errors(create_form, data)
            messages.error(request, 'Error creating namespace')

    status_code, data = _api_request(request, 'GET', '/api/namespaces/')
    namespaces = []
    if status_code == 200 and isinstance(data, list):
        namespaces = data
    elif isinstance(data, dict):
        messages.error(request, data.get('detail', 'Unable to load namespaces'))

    return render(request, 'web/namespaces_list.html', {
        'namespaces': namespaces,
        'create_form': create_form,
        'username': request.session.get('username')
    })


@require_http_methods(["GET", "POST"])
def namespace_detail(request, pk):
    if not request.session.get('auth_token'):
        return redirect('login')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            status_code, data = _api_request(request, 'DELETE', f'/api/namespaces/{pk}/')
            if status_code == 204:
                messages.success(request, 'Namespace deleted')
                return redirect('namespaces')
            messages.error(request, data.get('detail', 'Error deleting namespace'))
        else:
            form = NamespaceUpdateForm(request.POST)
            if form.is_valid():
                status_code, data = _api_request(request, 'PATCH', f'/api/namespaces/{pk}/', {
                    'new_name': form.cleaned_data['new_name']
                })
                if status_code == 200:
                    messages.success(request, 'Namespace updated')
                    return redirect('namespace-detail', pk=pk)
                _apply_form_errors(form, data)
                messages.error(request, 'Error updating namespace')
            else:
                messages.error(request, 'Invalid input')

    status_code, data = _api_request(request, 'GET', f'/api/namespaces/{pk}/')
    namespace = None
    if status_code == 200:
        namespace = data
    else:
        messages.error(request, data.get('detail', 'Namespace not found'))
        return redirect('namespaces')

    form = NamespaceUpdateForm(initial={'new_name': namespace.get('name', '')})
    # For UX: provide namespace switcher and accounts of selected namespace
    ns_status, ns_data = _api_request(request, 'GET', '/api/namespaces/')
    namespaces = ns_data if ns_status == 200 and isinstance(ns_data, list) else []
    acc_status, acc_data = _api_request(request, 'GET', '/api/accounts/', params={'namespace_id': pk})
    accounts_list = acc_data if acc_status == 200 and isinstance(acc_data, list) else []
    return render(request, 'web/namespaces_detail.html', {
        'namespace': namespace,
        'form': form,
        'namespaces': namespaces,
        'accounts': accounts_list,
        'selected_namespace_id': pk,
        'username': request.session.get('username')
    })


@require_http_methods(["GET", "POST"])
def change_password(request):
    if not request.session.get('auth_token'):
        return redirect('login')

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            status_code, data = _api_request(request, 'PATCH', '/api/auth/change-password/', {
                'password': form.cleaned_data['password']
            })
            if status_code == 200:
                username = request.session.get('username')
                new_password = form.cleaned_data['password']
                status_code2, data2 = _api_request(request, 'POST', '/api/auth/login/', {
                    'username': username,
                    'password': new_password
                })
                if status_code2 == 200 and 'token' in data2:
                    request.session['auth_token'] = data2['token']
                    messages.success(request, 'Password changed and logged in')
                    resp = redirect('namespaces')
                    resp.set_cookie(f'pwd_changed_{username}', '1', max_age=31536000, samesite='Lax')
                    return resp
                _apply_form_errors(form, data2)
                messages.error(request, 'Re-login failed')
            else:
                _apply_form_errors(form, data)
                messages.error(request, 'Error changing password')
    else:
        form = ChangePasswordForm()
    return render(request, 'web/change_password.html', {'form': form, 'username': request.session.get('username')})


def logout(request):
    request.session.flush()
    messages.success(request, 'Logged out')
    return redirect('login')


@require_http_methods(["GET", "POST"])
def accounts(request):
    if not request.session.get('auth_token'):
        return redirect('login')

    create_form = AccountCreateForm()
    ns_status, ns_data = _api_request(request, 'GET', '/api/namespaces/')
    namespaces = ns_data if ns_status == 200 and isinstance(ns_data, list) else []
    namespace_choices = [(str(ns['id']), ns['name']) for ns in namespaces]
    create_form.fields['namespace_id'].choices = namespace_choices
    ns = request.GET.get('namespace_id')
    if ns:
        create_form.initial['namespace_id'] = ns
    if request.method == 'POST':
        create_form = AccountCreateForm(request.POST)
        create_form.fields['namespace_id'].choices = namespace_choices
        if create_form.is_valid():
            payload = {
                'namespace_id': int(create_form.cleaned_data['namespace_id']),
                'name': create_form.cleaned_data['name'],
                'currency': create_form.cleaned_data['currency'],
            }
            status_code, data = _api_request(request, 'POST', '/api/accounts/', payload)
            if status_code == 201:
                messages.success(request, 'Account created')
                return redirect('accounts')
            _apply_form_errors(create_form, data)
            messages.error(request, 'Error creating account')

    params = {}
    selected_ns = None
    if ns:
        try:
            selected_ns = int(ns)
        except (TypeError, ValueError):
            selected_ns = None
        params['namespace_id'] = ns
    acc_status, acc_data = _api_request(request, 'GET', '/api/accounts/', params=params)
    accounts_list = acc_data if acc_status == 200 and isinstance(acc_data, list) else []
    if acc_status != 200 and isinstance(acc_data, dict):
        messages.error(request, acc_data.get('detail', 'Unable to load accounts'))

    # Group accounts by namespace when not filtered
    grouped = {}
    if not ns:
        for acc in accounts_list:
            key = acc.get('namespace_name') or f"Namespace {acc.get('namespace')}"
            grouped.setdefault(key, []).append(acc)

    return render(request, 'web/accounts_list.html', {
        'accounts': accounts_list,
        'grouped_accounts': grouped,
        'namespaces': namespaces,
        'create_form': create_form,
        'selected_namespace_id': selected_ns,
        'username': request.session.get('username')
    })


@require_http_methods(["GET", "POST"])
def account_detail(request, pk):
    if not request.session.get('auth_token'):
        return redirect('login')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            status_code, data = _api_request(request, 'DELETE', f'/api/accounts/{pk}/')
            if status_code == 204:
                messages.success(request, 'Account deleted')
                return redirect('accounts')
            messages.error(request, data.get('detail', 'Error deleting account'))
        else:
            form = AccountUpdateForm(request.POST)
            if form.is_valid():
                status_code, data = _api_request(request, 'PATCH', f'/api/accounts/{pk}/', {
                    'name': form.cleaned_data['name']
                })
                if status_code == 200:
                    messages.success(request, 'Account updated')
                    return redirect('account-detail', pk=pk)
                _apply_form_errors(form, data)
                messages.error(request, 'Error updating account')
            else:
                messages.error(request, 'Invalid input')

    status_code, data = _api_request(request, 'GET', f'/api/accounts/{pk}/')
    account = None
    if status_code == 200:
        account = data
    else:
        messages.error(request, data.get('detail', 'Account not found'))
        return redirect('accounts')

    # Fetch transactions related to this account
    t_status, t_data = _api_request(request, 'GET', '/api/transactions/', params={'account_id': pk})
    account_transactions = t_data if t_status == 200 and isinstance(t_data, list) else []

    form = AccountUpdateForm(initial={'name': account.get('name', '')})
    return render(request, 'web/accounts_detail.html', {
        'account': account,
        'form': form,
        'transactions': account_transactions,
        'username': request.session.get('username')
    })


@require_http_methods(["GET"])
def transactions(request):
    if not request.session.get('auth_token'):
        return redirect('login')

    filter_form = TransactionFilterForm(request.GET or None)
    params = {}
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('type'):
            params['type'] = filter_form.cleaned_data['type']
        if filter_form.cleaned_data.get('account_id'):
            params['account_id'] = filter_form.cleaned_data['account_id']
    status_code, data = _api_request(request, 'GET', '/api/transactions/', params=params)
    transactions_list = []
    if status_code == 200 and isinstance(data, list):
        transactions_list = data
    elif isinstance(data, dict):
        messages.error(request, data.get('detail', 'Unable to load transactions'))

    return render(request, 'web/transactions_list.html', {
        'transactions': transactions_list,
        'filter_form': filter_form,
        'username': request.session.get('username')
    })


@require_http_methods(["GET", "POST"])
def transaction_in_create(request):
    if not request.session.get('auth_token'):
        return redirect('login')
    # Build account choices (optionally filter by namespace)
    ns = request.GET.get('namespace_id')
    params = {}
    if ns:
        params['namespace_id'] = ns
    acc_status, acc_data = _api_request(request, 'GET', '/api/accounts/', params=params)
    accounts = acc_data if acc_status == 200 and isinstance(acc_data, list) else []
    choices = [(str(a['id']), f"{a['name']} — {a['balance']} {a['currency']}") for a in accounts]

    form = TransactionInForm()
    form.fields['account_id'].choices = choices
    if request.method == 'POST':
        form = TransactionInForm(request.POST)
        form.fields['account_id'].choices = choices
        if form.is_valid():
            payload = {
                'account_id': int(form.cleaned_data['account_id']),
                'amount': str(form.cleaned_data['amount']),
                'currency': form.cleaned_data['currency'],
                'description': form.cleaned_data.get('description', ''),
            }
            status_code, data = _api_request(request, 'POST', '/api/transactions/in/', payload)
            if status_code == 201:
                messages.success(request, 'IN transaction created')
                return redirect('transactions')
            _apply_form_errors(form, data)
            messages.error(request, 'Error creating IN transaction')
    # Namespaces for selector
    ns_status, ns_data = _api_request(request, 'GET', '/api/namespaces/')
    namespaces = ns_data if ns_status == 200 and isinstance(ns_data, list) else []
    return render(request, 'web/transaction_in_form.html', {
        'form': form,
        'namespaces': namespaces,
        'selected_namespace_id': ns,
        'username': request.session.get('username')
    })


@require_http_methods(["GET", "POST"])
def transaction_out_create(request):
    if not request.session.get('auth_token'):
        return redirect('login')
    ns = request.GET.get('namespace_id')
    params = {}
    if ns:
        params['namespace_id'] = ns
    acc_status, acc_data = _api_request(request, 'GET', '/api/accounts/', params=params)
    accounts = acc_data if acc_status == 200 and isinstance(acc_data, list) else []
    choices = [(str(a['id']), f"{a['name']} — {a['balance']} {a['currency']}") for a in accounts]

    form = TransactionOutForm()
    form.fields['account_id'].choices = choices
    if request.method == 'POST':
        form = TransactionOutForm(request.POST)
        form.fields['account_id'].choices = choices
        if form.is_valid():
            payload = {
                'account_id': int(form.cleaned_data['account_id']),
                'amount': str(form.cleaned_data['amount']),
                'currency': form.cleaned_data['currency'],
                'description': form.cleaned_data.get('description', ''),
            }
            status_code, data = _api_request(request, 'POST', '/api/transactions/out/', payload)
            if status_code == 201:
                messages.success(request, 'OUT transaction created')
                return redirect('transactions')
            _apply_form_errors(form, data)
            messages.error(request, 'Error creating OUT transaction')
    ns_status, ns_data = _api_request(request, 'GET', '/api/namespaces/')
    namespaces = ns_data if ns_status == 200 and isinstance(ns_data, list) else []
    return render(request, 'web/transaction_out_form.html', {
        'form': form,
        'namespaces': namespaces,
        'selected_namespace_id': ns,
        'username': request.session.get('username')
    })


@require_http_methods(["GET", "POST"])
def transaction_transfer_create(request):
    if not request.session.get('auth_token'):
        return redirect('login')
    # Build account choices for source and destination
    ns = request.GET.get('namespace_id')
    params = {}
    if ns:
        params['namespace_id'] = ns
    acc_status, acc_data = _api_request(request, 'GET', '/api/accounts/', params=params)
    accounts = acc_data if acc_status == 200 and isinstance(acc_data, list) else []
    choices = [(str(a['id']), f"{a['name']} — {a['balance']} {a['currency']}") for a in accounts]

    form = TransactionTransferForm()
    form.fields['source_account_id'].choices = choices
    form.fields['destination_account_id'].choices = choices
    if request.method == 'POST':
        form = TransactionTransferForm(request.POST)
        form.fields['source_account_id'].choices = choices
        form.fields['destination_account_id'].choices = choices
        if form.is_valid():
            payload = {
                'source_account_id': int(form.cleaned_data['source_account_id']),
                'destination_account_id': int(form.cleaned_data['destination_account_id']),
                'source_amount': str(form.cleaned_data['source_amount']),
                'destination_amount': str(form.cleaned_data['destination_amount']),
                'description': form.cleaned_data.get('description', ''),
            }
            status_code, data = _api_request(request, 'POST', '/api/transactions/transfer/', payload)
            if status_code == 201:
                rate_msg = ''
                if isinstance(data, dict):
                    src_rate = data.get('source_currency_rate')
                    dst_rate = data.get('destination_currency_rate')
                    if src_rate is not None and dst_rate is not None:
                        rate_msg = f" (rates: src {src_rate}, dst {dst_rate})"
                messages.success(request, f'TRANSFER transaction created{rate_msg}')
                return redirect('transactions')
            _apply_form_errors(form, data)
            messages.error(request, 'Error creating TRANSFER transaction')
    return render(request, 'web/transaction_transfer_form.html', {
        'form': form,
        'username': request.session.get('username')
    })


@require_http_methods(["GET", "POST"])
def transaction_transfer_wizard(request):
    if not request.session.get('auth_token'):
        return redirect('login')

    step = int(request.GET.get('step') or 1)
    # Step 1: select source namespace
    if step == 1:
        status, namespaces = _api_request(request, 'GET', '/api/namespaces/')
        choices = []
        if status == 200 and isinstance(namespaces, list):
            choices = [(str(ns['id']), ns['name']) for ns in namespaces]
        form = NamespaceSelectForm()
        form.fields['namespace_id'].choices = choices
        if request.method == 'POST':
            form = NamespaceSelectForm(request.POST)
            form.fields['namespace_id'].choices = choices
            if form.is_valid():
                request.session['transfer_src_ns_id'] = int(form.cleaned_data['namespace_id'])
                return redirect('/transactions/transfer/wizard/?step=2')
        return render(request, 'web/transfer_wizard.html', {'step': step, 'form': form, 'username': request.session.get('username')})

    # Step 2: select source account from selected namespace
    if step == 2:
        src_ns = request.session.get('transfer_src_ns_id')
        if not src_ns:
            return redirect('/transactions/transfer/wizard/?step=1')
        status, accounts = _api_request(request, 'GET', '/api/accounts/', params={'namespace_id': src_ns})
        choices = []
        if status == 200 and isinstance(accounts, list):
            choices = [(str(a['id']), f"{a['name']} — {a['balance']} {a['currency']}") for a in accounts]
        form = AccountSelectForm()
        form.fields['account_id'].choices = choices
        if request.method == 'POST':
            form = AccountSelectForm(request.POST)
            form.fields['account_id'].choices = choices
            if form.is_valid():
                request.session['transfer_src_acc_id'] = int(form.cleaned_data['account_id'])
                return redirect('/transactions/transfer/wizard/?step=3')
        return render(request, 'web/transfer_wizard.html', {'step': step, 'form': form, 'username': request.session.get('username')})

    # Step 3: select destination namespace
    if step == 3:
        status, namespaces = _api_request(request, 'GET', '/api/namespaces/')
        choices = []
        if status == 200 and isinstance(namespaces, list):
            choices = [(str(ns['id']), ns['name']) for ns in namespaces]
        form = NamespaceSelectForm()
        form.fields['namespace_id'].choices = choices
        if request.method == 'POST':
            form = NamespaceSelectForm(request.POST)
            form.fields['namespace_id'].choices = choices
            if form.is_valid():
                request.session['transfer_dst_ns_id'] = int(form.cleaned_data['namespace_id'])
                return redirect('/transactions/transfer/wizard/?step=4')
        return render(request, 'web/transfer_wizard.html', {'step': step, 'form': form, 'username': request.session.get('username')})

    # Step 4: select destination account
    if step == 4:
        dst_ns = request.session.get('transfer_dst_ns_id')
        if not dst_ns:
            return redirect('/transactions/transfer/wizard/?step=3')
        status, accounts = _api_request(request, 'GET', '/api/accounts/', params={'namespace_id': dst_ns})
        choices = []
        if status == 200 and isinstance(accounts, list):
            choices = [(str(a['id']), f"{a['name']} — {a['balance']} {a['currency']}") for a in accounts]
        form = AccountSelectForm()
        form.fields['account_id'].choices = choices
        if request.method == 'POST':
            form = AccountSelectForm(request.POST)
            form.fields['account_id'].choices = choices
            if form.is_valid():
                request.session['transfer_dst_acc_id'] = int(form.cleaned_data['account_id'])
                return redirect('/transactions/transfer/wizard/?step=5')
        return render(request, 'web/transfer_wizard.html', {'step': step, 'form': form, 'username': request.session.get('username')})

    # Step 5: amounts and confirm
    if step == 5:
        form = TransactionTransferForm()
        # For UX, hide account selects; they’re already chosen; only show amounts and description
        del form.fields['source_account_id']
        del form.fields['destination_account_id']
        if request.method == 'POST':
            # Use a lightweight amounts form by reading posted fields directly
            try:
                src_amount = request.POST.get('source_amount')
                dst_amount = request.POST.get('destination_amount')
                description = request.POST.get('description', '')
                payload = {
                    'source_account_id': request.session.get('transfer_src_acc_id'),
                    'destination_account_id': request.session.get('transfer_dst_acc_id'),
                    'source_amount': str(src_amount),
                    'destination_amount': str(dst_amount),
                    'description': description,
                }
                status_code, data = _api_request(request, 'POST', '/api/transactions/transfer/', payload)
                if status_code == 201:
                    src_rate = data.get('source_currency_rate') if isinstance(data, dict) else None
                    dst_rate = data.get('destination_currency_rate') if isinstance(data, dict) else None
                    rate_msg = ''
                    if src_rate is not None and dst_rate is not None:
                        rate_msg = f" (rates: src {src_rate}, dst {dst_rate})"
                    messages.success(request, f'TRANSFER transaction created{rate_msg}')
                    # Clear wizard session state
                    for k in ['transfer_src_ns_id','transfer_src_acc_id','transfer_dst_ns_id','transfer_dst_acc_id']:
                        request.session.pop(k, None)
                    return redirect('transactions')
                messages.error(request, 'Error creating TRANSFER transaction')
            except Exception:
                messages.error(request, 'Invalid input')
        return render(request, 'web/transfer_wizard.html', {'step': step, 'form': form, 'username': request.session.get('username')})

    # Fallback to step 1
    return redirect('/transactions/transfer/wizard/?step=1')
