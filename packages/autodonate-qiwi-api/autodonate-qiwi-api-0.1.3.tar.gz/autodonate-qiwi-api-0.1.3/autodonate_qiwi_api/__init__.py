import autodonate_qiwi_api.types
from autodonate.lib.context_processors import register_variable

__version__ = "0.1.3"
__all__ = ["QIWI", "initialize", "types"]

# Don't create millions of separated objects (and threads). Use only one.
QIWI = None


def initialize(*args, **kwargs) -> None:
    """Create Qiwi object and start it."""
    from autodonate_qiwi_api.main import Qiwi

    global QIWI
    if QIWI:
        log.warning("QIWI API already initialized.")
        return None
    register_variable("QIWI_API_INSTALLED", True)
    QIWI = Qiwi(*args, **kwargs)
    QIWI.start_thread()
