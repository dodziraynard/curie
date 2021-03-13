from . base import *
from . test import *
try:
    from . prod import *
except ImportError:
    pass
try:
    from . local_settings import *
except ImportError:
    pass
