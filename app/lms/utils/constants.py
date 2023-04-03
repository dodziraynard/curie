import enum

USED_PERMISSION_CODES = [
    "view_dashboard",
    "view_subject",
    "manage_setup",
]


class TransactionType(enum.Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class InvoiceStatus(enum.Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    PAID = "PAID"


class InvoiceItemType(enum.Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"