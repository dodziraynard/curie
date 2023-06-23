import enum

USED_PERMISSION_CODES = [
    "view_dashboard",
    "view_subject",
    "manage_setup",
]


class TransactionStatusMessages(enum.Enum):
    PENDING = 'Transaction is pending'
    SUCCESS = 'Transaction successful'
    FAILED = 'Transaction failed'


class TransactionStatus(enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class TransactionType(enum.Enum):
    CREDIT = "CREDIT".lower()
    DEBIT = "DEBIT".lower()


class InvoiceStatus(enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    APPLIED = "applied"


class InvoiceItemType(enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class TransactionDirection(enum.Enum):
    IN = 'IN'.lower()
    OUT = 'OUT'.lower()
    
class TaskType(enum.Enum):
    ACADEMIC_RECORD = "ACADEMIC_RECORD".lower()
    CLASS_TEACHER_REPORT = "CLASS_TEACHER_REPORT".lower()
    ASSITANT_HEAD_SIGNATURE = "ASSITANT_HEAD_SIGNATURE".lower()
    HOUE_MASTER_REPORT = "HOUE_MASTER_REPORT".lower()
    OTHER = "OTHER".lower()
    
class TaskStatus(enum.Enum):
    PENDING = "PENDING".lower()
    IN_PROCESS = "IN_PROCESS".lower()
    COMPLETED = "COMPLETED".lower()
    WARNING = "WARNING".lower()
    OVERDUE = "OVERDUE".lower()
