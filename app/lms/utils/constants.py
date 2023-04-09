import enum

USED_PERMISSION_CODES = [
    "view_dashboard",
    "view_subject",
    "manage_setup",
]


class TransactionType(enum.Enum):
    CREDIT = "CREDIT".lower()
    DEBIT = "DEBIT".lower()


class InvoiceStatus(enum.Enum):
    DRAFT = "DRAFT".lower()
    PENDING = "PENDING".lower()
    APPLIED = "APPLIED".lower()


class InvoiceItemType(enum.Enum):
    CREDIT = "CREDIT".lower()
    DEBIT = "DEBIT".lower()


class TransactionDirection(enum.Enum):
    IN = 'IN'.lower()
    OUT = 'OUT'.lower()