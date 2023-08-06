import django
django.setup()

from autodonate_qiwi_api.main import QIWI, initialize
import autodonate_qiwi_api.types
from autodonate.lib.context_processors import register_variable

__version__ = "0.1.1"
__all__ = ["QIWI", "initialize", "types"]

register_variable("QIWI_API_INSTALLED", True)
