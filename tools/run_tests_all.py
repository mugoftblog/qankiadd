from importlib import reload
from dataprov.google import *
from tests.stubs.dataprov.google import *
import sys


def sys_exit_stub(code):
    print("sys.exit(%d)" % code)


def register_stubs():
    sys.exit = sys_exit_stub
    GoogleFactory.__init__ = GoogleFactoryStub.__init__


register_stubs()

from tests.test_models import *
from tests.test_config import *
from tests.test_exporting import *
from tests.test_keylistener import *


