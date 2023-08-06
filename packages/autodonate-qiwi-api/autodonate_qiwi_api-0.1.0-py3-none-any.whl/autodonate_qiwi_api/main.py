import autodonate_qiwi_api.types as types
import autodonate_qiwi_api.models as models
from autodonate.lib.utils.logger import get_logger
import requests
import time
import threading


log = get_logger(__name__)


class Qiwi:
    """Object for QIWI API"""
    def __init__(
        self,
        token: str,
        phone: str | int,
        rows: int = 10,
        update_interval: int = 5,
        base_url: str = "https://edge.qiwi.com",
        operation: types.Operation = types.Operation.IN,
        sources: list | tuple = (types.Source.RUB,),
        callback=None,
    ):
        """__init__() method.

        :arg token:
            API key taken from https://qiwi.com/api
        :arg phone:
            QIWI phone number
        :arg rows:
            Rows to fetch from QIWI API
        :arg update_interval:
            How frequently call API?
        :arg base_url:
            Base URL for QIWI API usually you dont need change this
        :arg operation:
            Types of operations to fetch
        :arg sources:
            Currencies to fetch
        :arg callback:
            Callable to call on each transaction.
            Signature:
                >>> def function(tx: autodonate_qiwi_api.types.Transaction)"""
        self.callback = callback
        self.token = token
        self.phone = phone
        self.rows = rows
        self.sources = sources
        self.operation = operation
        self.update_interval = update_interval
        self.headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + token,
        }
        self.unprocessed: list[types.Transaction] = []
        self.base_url = base_url
        self.thread: threading.Thread | None = None

    def generate_link(self) -> str:
        """Generate API link.

        :return API link (str)"""
        sources = "&".join(
            [
                f"sources%5B%{i}5D={self.sources[i].value}"
                for i in range(len(self.sources))
            ]
        )
        url = (
            f"/payment-history/v2/persons/{self.phone}/payments?"
            f"rows={self.rows}&operation={self.operation.value}&{sources}"
        )
        return self.base_url + url

    def tx(self, tx) -> types.Transaction | None:
        """Process individual tx from self._loop()

        :arg tx: dict
        :return autodonate_qiwi_api.types.Transaction or None"""
        try:
            m = models.Payment(txId=tx["txnId"])
            m.save()
            transaction = types.Transaction(
                txId=tx["txnId"],
                personId=tx["personId"],
                date=tx["date"],
                account=tx["account"],
                amount=tx["sum"]["amount"],
                commission=tx["commission"]["amount"],
                total=tx["total"]["amount"],
                comment=tx["comment"],
            )
            if self.callback is not None:
                self.callback(transaction)
            else:
                self.unprocessed.append(transaction)
            return tx
        except:
            return None

    def _loop(self) -> None:
        """Get all updates from QIWI"""
        response = requests.get(self.generate_link(), headers=self.headers)
        response.raise_for_status()
        r = response.json()
        for tx in r["data"]:
            self.tx(tx)
        if self.callback is not None:
            for tx in self.unprocessed:
                self.callback(tx)
            self.unprocessed = []

    def start(self) -> None:
        """Blocking method"""
        while True:
            self._loop()
            time.sleep(self.update_interval)

    def start_thread(self) -> None:
        """Non-blocking method. Launches self.start() in separate thread."""
        if self.thread:
            log.warning("Thread already initialized.")
            return None
        self.thread = threading.Thread(target=self.start)
        self.thread.start()


# Don't create millions of separated objects (and threads). Use only one.
QIWI: Qiwi | None = None


def initialize(*args, **kwargs) -> None:
    """Create Qiwi object and start it"""
    global QIWI
    if QIWI:
        log.warning("QIWI API already initialized.")
        return None
    QIWI = Qiwi(*args, **kwargs)
    QIWI.start_thread()
