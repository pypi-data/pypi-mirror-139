from expressmoney.api import *

__all__ = ('LoanAPI', 'PayAPI')

SERVICE_NAME = 'loans'


class LoansContract(Contract):
    OPEN = "OPEN"
    OVERDUE = "OVERDUE"
    STOP_INTEREST = "STOP_INTEREST"
    DEFAULT = "DEFAULT"
    CLOSED = "CLOSED"
    STATUS_CHOICES = {
        (OPEN, gettext_lazy("Open loan")),
        (OVERDUE, gettext_lazy("Overdue loan")),
        (STOP_INTEREST, gettext_lazy("Stop interest loan")),
        (DEFAULT, gettext_lazy("Default loan")),
        (CLOSED, gettext_lazy("Closed loan")),
    }
    OPEN_STATUSES = (OPEN, OVERDUE, STOP_INTEREST, DEFAULT)

    pagination = PaginationContract()
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()

    amount = serializers.DecimalField(max_digits=7, decimal_places=0, allow_null=True)
    period = serializers.IntegerField()
    expiry_date = serializers.DateField()
    expiry_period = serializers.IntegerField()

    interests_charged_date = serializers.DateField(allow_null=True)
    sign = serializers.IntegerField()
    status = serializers.ChoiceField(choices=STATUS_CHOICES)

    body_balance = serializers.DecimalField(max_digits=7, decimal_places=0, allow_null=True)
    body_paid = serializers.DecimalField(max_digits=7, decimal_places=0, allow_null=True)
    interests_total = serializers.DecimalField(max_digits=7, decimal_places=0, allow_null=True)
    interests_paid = serializers.DecimalField(max_digits=7, decimal_places=0, allow_null=True)
    interests_balance = serializers.DecimalField(max_digits=7, decimal_places=0)

    document = serializers.CharField(max_length=256, allow_blank=True)
    comment = serializers.CharField(max_length=2048, allow_blank=True)


class PayContract(Contract):
    bank_card_id = serializers.IntegerField()


class LoanAPI(API):
    _contract = LoansContract
    _service_name = SERVICE_NAME
    _app = 'loans'
    _point = 'loan'


class PayAPI(API):
    _contract = PayContract
    _service_name = 'loans'
    _app = 'loans'
    _point = 'pay'
