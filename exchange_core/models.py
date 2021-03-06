import uuid
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from model_utils import Choices
from model_utils.models import TimeStampedModel
from cities.models import Country, Region, City
from extended_choices import Choices as EChoices
from simple_history.models import HistoricalRecords

from exchange_core.managers import CustomUserManager
from exchange_core.choices import (BR_BANKS_CHOICES, BR_ACCOUNT_TYPES_CHOICES, CURRENCY_TYPE_CHOICES,
                                   CHECKING_TYPE, STATE_CHOICES, ACTIVE_STATE)


def get_file_path(instance, filename):
    return '{}.{}'.format(uuid.uuid4(), filename.split('.')[-1])


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Users(TimeStampedModel, AbstractUser, BaseModel):
    STATUS = EChoices(
        ('created', 'created', _("Created")),
        ('inactive', 'inactive', _("Inactive")),
        ('approved_documentation', 'approved_documentation', _("Approved documentation")),
        ('disapproved_documentation', 'disapproved_documentation', _("Disapproved documentation")),
    )

    TYPE = EChoices(
        ('person', 'person', _("Person")),
        ('company', 'company', _("Company")),
    )

    status = models.CharField(max_length=30, default=STATUS.created, choices=STATUS.choices, verbose_name=_("Status"))
    avatar = models.ImageField(upload_to=get_file_path, blank=True, verbose_name=_("Avatar"))
    profile = JSONField(null=True, blank=True, default=dict, verbose_name=_("Profile data"))
    type = models.CharField(max_length=11, choices=TYPE.choices, default=TYPE.person, null=True, blank=False, verbose_name=_("Type"))
    document_1 = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name=_("Document 1"))
    document_2 = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name=_("Document 2"))
    mobile_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Mobile phone"))

    objects = CustomUserManager()
    is_test = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status
        if self.profile is None:
            self.profile = {}

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    # Retorna Yes/No se o usuario tem uma conta bancaria associada a sua conta BRL
    @property
    def has_br_bank_account(self):
        br_account = self.accounts.get(
            currency__code=settings.BRL_CURRENCY_CODE)
        return 'yes' if br_account.bank_accounts.exists() else 'no'

    @property
    def br_bank_account(self):
        br_account = self.accounts.get(
            currency__code=settings.BRL_CURRENCY_CODE)
        if br_account.bank_accounts.exists():
            return br_account.bank_accounts.first()


class Addresses(TimeStampedModel, BaseModel):
    TYPES = Choices('account')

    user = models.ForeignKey(Users, related_name='addresses', on_delete=models.CASCADE, verbose_name=_("User"))
    country = models.ForeignKey(Country, related_name='addresses', on_delete=models.CASCADE, verbose_name=_("Country"))
    region = models.ForeignKey(Region, related_name='addresses', on_delete=models.CASCADE, verbose_name=_("State"))
    city = models.ForeignKey(City, related_name='addresses', on_delete=models.CASCADE, verbose_name=_("City"))
    address = models.CharField(max_length=100, verbose_name=_("Address"))
    number = models.CharField(max_length=20, verbose_name=_("Number"))
    neighborhood = models.CharField(max_length=50, verbose_name=_("Neighborhood"))
    zipcode = models.CharField(max_length=10, verbose_name=_("Zipcode"))
    complement = models.CharField(max_length=50, null=True, verbose_name=_("Complement"))
    type = models.CharField(max_length=20, choices=TYPES, default=TYPES.account, verbose_name=_("Type"))

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


class Companies(TimeStampedModel, BaseModel):
    user = models.ForeignKey(Users, related_name='companies', on_delete=models.CASCADE, verbose_name=_("User"))
    name = models.CharField(max_length=100, verbose_name=_("Fancy name"))
    document_1 = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Document 1"))
    document_2 = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Document 2"))

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")


class Currencies(TimeStampedModel, BaseModel):
    TYPES = EChoices(
        ('checking', 'checking', _("Checking")),
        ('investment', 'investment', _("Investment"))
    )

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    code = models.CharField(max_length=10, verbose_name=_("Code"))
    prefix = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("Prefix"), help_text=_("This will be appended before the amount of this currency in the entire system"))
    sufix = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("Sufix"), help_text=_("This will be appended after the amount of this currency in the entire system"))
    is_fiat = models.BooleanField(default=False, verbose_name=_("Is FIAT"), help_text=_("Mark this field if the currency is a fiduciary one"))
    type = models.CharField(max_length=20, choices=CURRENCY_TYPE_CHOICES, default=CHECKING_TYPE, verbose_name=_("Type"))
    icon = models.ImageField(upload_to=get_file_path, null=True, blank=True, verbose_name=_("Icon"))
    state = models.CharField(max_length=30, default=ACTIVE_STATE, choices=STATE_CHOICES, verbose_name=_("Status"))
    withdraw_min = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0'), verbose_name=_("Withdraw Min"))
    withdraw_max = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('1000000.00'), verbose_name=_("Withdraw Max"))
    withdraw_fee = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0'), verbose_name=_("Withdraw Percent Fee"))
    withdraw_fixed_fee = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0'), verbose_name=_("Withdraw Fixed Fee"))
    withdraw_receive_hours = models.IntegerField(default=48, verbose_name=_("Withdraw receive hours"))
    withdraw_auto_approve = models.BooleanField(default=False, verbose_name=_("Auto approve withdraw"), help_text=_("Mark this if the withdraw must be automatically approved by the system"))

    # Transfer between system accounts
    tbsa_fee = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0'), verbose_name=_("TBSA Percent Fee"), help_text=_("Transfer between system accounts"))
    tbsa_fixed_fee = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0'), verbose_name=_("TBSA Fixed Fee"), help_text=_("Transfer between system accounts"))

    order = models.IntegerField(default=100, verbose_name=_("Order"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")
        ordering = ['name']
        unique_together = (('code', 'type'),)

    def __str__(self):
        return self.name + ' - ' + self.type_title

    @property
    def type_title(self):
        return self.type.title()

    @property
    def dict(self):
        return {
            'withdraw_min': self.withdraw_min,
            'withdraw_max': self.withdraw_max,
            'withdraw_fee': self.withdraw_fee,
            'withdraw_fixed_fee': self.withdraw_fixed_fee,
            'withdraw_receive_hours': self.withdraw_receive_hours,
            'tbsa_fee': self.tbsa_fee,
            'tbsa_fixed_fee': self.tbsa_fixed_fee
        }


class Accounts(TimeStampedModel, BaseModel):
    currency = models.ForeignKey(Currencies, related_name='accounts', verbose_name=_("Currency"), on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name='accounts', null=True, verbose_name=_("User"), on_delete=models.CASCADE)
    deposit = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'), verbose_name=_("Deposit"))
    reserved = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'), verbose_name=_("Reserved"))
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Address"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        ordering = ['currency__name']

    def __str__(self):
        return '{}/{} - {}/{}'.format(self.user.name, self.user.username, self.currency.code,  self.currency.type.title())

    @property
    def balance(self):
        return self.deposit + self.reserved

    def takeout(self, amount):
        self.deposit -= amount
        self.save()

    def to_deposit(self, amount):
        self.deposit += amount
        self.save()


class BankAccounts(TimeStampedModel, BaseModel):
    bank = models.CharField(max_length=10, choices=BR_BANKS_CHOICES, verbose_name=_("Bank"))
    agency = models.CharField(max_length=10, verbose_name=_("Agency"))
    agency_digit = models.CharField(max_length=5, null=True, verbose_name=_("Digit"))
    account_type = models.CharField(max_length=20, choices=BR_ACCOUNT_TYPES_CHOICES, verbose_name=_("Account type"))
    account_number = models.CharField(max_length=20, verbose_name=_("Account number"))
    account_number_digit = models.CharField(max_length=5, null=True, verbose_name=_("Digit"))
    account = models.ForeignKey(Accounts, related_name='bank_accounts', on_delete=models.CASCADE, verbose_name=_("Account"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Bank account")
        verbose_name_plural = _("Bank accounts")


# Base class para saques
class BaseWithdraw(BaseModel):
    STATUS = EChoices(
        ('requested', 'requested', _("Requested")),
        ('reversed', 'reversed', _("Reversed")),
        ('paid', 'paid', _("Paid"))
    )

    deposit = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'), verbose_name=_("Deposit"))
    reserved = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'), verbose_name=_("Reserved"))
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'), verbose_name=_("Amount"))
    fee = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'), verbose_name=_("Fee"))
    status = models.CharField(max_length=20, default=STATUS.requested, choices=STATUS, verbose_name=_("Status"))
    tx_id = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Transaction id"))
    description = models.CharField(max_length=100, null=True, verbose_name=_("Description"))

    # Valor do saque com desconto do fee cobrado
    @property
    def net_amount(self):
        return abs(self.amount) - abs(self.fee)

    class Meta:
        abstract = True


# Saques bancários
class BankWithdraw(TimeStampedModel, BaseWithdraw):
    bank = models.CharField(max_length=10, choices=BR_BANKS_CHOICES, verbose_name=_("Bank"))
    agency = models.CharField(max_length=10, verbose_name=_("Agency"))
    agency_digit = models.CharField(max_length=5, null=True, verbose_name=_("Digit"))
    account_type = models.CharField(max_length=20, choices=BR_ACCOUNT_TYPES_CHOICES, verbose_name=_("Account type"))
    account_number = models.CharField(max_length=20, verbose_name=_("Account number"))
    account_number_digit = models.CharField(max_length=5, null=True, verbose_name=_("Digit"))
    account = models.ForeignKey(Accounts, related_name='bank_withdraw',on_delete=models.CASCADE, verbose_name=_("Account"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Withdrawal - Fiat")
        verbose_name_plural = _("Withdrawals - Fiat")


# Saques de criptomoedas
class CryptoWithdraw(TimeStampedModel, BaseWithdraw):
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    account = models.ForeignKey(Accounts, related_name='crypto_withdraw', verbose_name=_("Account"), on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Withdrawal - Cryptocurrency")
        verbose_name_plural = _("Withdrawals - Cryptocurrency")


# Documentos
class Documents(TimeStampedModel, BaseModel):
    TYPES = EChoices(
        ('id_front', 'id_front', _("ID front")),
        ('id_back', 'id_back', _("ID back")),
        ('selfie', 'selfie', _("Selfie with ID")),
        ('social_contract', 'social_contract', _("Social contract")),
        ('residence', 'residence', _("Proof of address"))
    )
    STATUS = EChoices(
        ('pending', 'pending', _("Pending")),
        ('disapproved', 'disapproved', _("Disapproved")),
        ('approved', 'approved', _("Approved"))
    )

    user = models.ForeignKey(Users, related_name='documents', verbose_name=_("User"), on_delete=models.CASCADE)
    file = models.ImageField(upload_to=get_file_path, verbose_name=_("File"))
    type = models.CharField(max_length=20, choices=TYPES, verbose_name=_("Type"))
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS.pending, verbose_name=_("Status"))
    reason = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Disapproved reason"))

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        ordering = ['status']


# Account statement
class Statement(TimeStampedModel, BaseModel):
    TYPES = EChoices(
        ('deposit', 'deposit', _("Deposit")),
        ('reversed', 'reversed', _("Reversed")),
        ('withdraw', 'withdraw', _("Withdraw")),
        ('income', 'income', _("Income")),
        ('investment', 'investment', _("Investment")),
        ('tbsa', 'tbsa', _("TBSA")),
        ('course_subscription', 'course_subscription', _("Course Subscription")),
        ('advisor_card_request', 'advisor_card_request', _("Advisor Card Request"))
    )

    account = models.ForeignKey(Accounts, related_name='statement', on_delete=models.CASCADE, verbose_name=_("Account"))
    description = models.CharField(max_length=100, verbose_name=_("Description"))
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'), verbose_name=_("Amount"))
    type = models.CharField(max_length=30, choices=TYPES, verbose_name=_("Type"))
    tx_id = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Transaction id"))
    fk = models.UUIDField(null=True, blank=True, editable=False, verbose_name=_("Foreign key"))

    class Meta:
        verbose_name = _("Statement")
        verbose_name_plural = _("Statement")
