from importlib import reload
import sys


def sys_exit_stub(code):
    print("sys.exit(%d)" % code)


def register_stubs():
    sys.exit = sys_exit_stub


register_stubs()

#from tests.test_models import *
#from tests.test_config import *
from tests.test_exporting import *


