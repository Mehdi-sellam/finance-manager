from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class NamespaceCreateForm(forms.Form):
    name = forms.CharField(max_length=50)


class NamespaceUpdateForm(forms.Form):
    new_name = forms.CharField(max_length=50)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


CURRENCY_CHOICES = (
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('DZD', 'DZD'),
)


class AccountCreateForm(forms.Form):
    namespace_id = forms.ChoiceField(choices=())
    name = forms.CharField(max_length=50)
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)


class AccountUpdateForm(forms.Form):
    name = forms.CharField(max_length=50)


class TransactionFilterForm(forms.Form):
    type = forms.ChoiceField(choices=(('', 'All'), ('IN', 'IN'), ('OUT', 'OUT'), ('TRANSFER', 'TRANSFER')), required=False)
    account_id = forms.IntegerField(required=False)


class TransactionInForm(forms.Form):
    account_id = forms.ChoiceField(choices=())
    amount = forms.DecimalField(max_digits=19, decimal_places=2)
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)
    description = forms.CharField(required=False)


class TransactionOutForm(forms.Form):
    account_id = forms.ChoiceField(choices=())
    amount = forms.DecimalField(max_digits=19, decimal_places=2)
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)
    description = forms.CharField(required=False)


class TransactionTransferForm(forms.Form):
    source_account_id = forms.ChoiceField(choices=())
    destination_account_id = forms.ChoiceField(choices=())
    source_amount = forms.DecimalField(max_digits=19, decimal_places=2)
    destination_amount = forms.DecimalField(max_digits=19, decimal_places=2)
    description = forms.CharField(required=False)


class NamespaceSelectForm(forms.Form):
    namespace_id = forms.ChoiceField(choices=())


class AccountSelectForm(forms.Form):
    account_id = forms.ChoiceField(choices=())

