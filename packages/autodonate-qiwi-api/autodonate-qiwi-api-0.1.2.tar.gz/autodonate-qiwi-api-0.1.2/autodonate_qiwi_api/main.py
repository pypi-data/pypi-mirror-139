from autodonate_qiwi_api import types, models
from autodonate.lib.utils.logger import get_logger
from requests import get
from time import sleep
from threading import Thread


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
        """__init__ method.

        Args:
            token: API key taken from https://qiwi.com/api.
            phone: QIWI phone number.
            rows: Rows to fetch from QIWI API.
            update_interval: How frequently call API?
            base_url: Base URL for QIWI API usually you dont need change this.
            operation: Types of operations to fetch.
            sources: Currencies to fetch.
            callback: Callable to call on each transaction.
        """
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
        self.thread: Thread | None = None

    def generate_link(self) -> str:
        """Generate API link.

        Returns:
            API link.
        """
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
        """Process individual tx from self._loop().

        Args:
            tx: dict.
        
        Returns:
            autodonate_qiwi_api.types.Transaction or None.
        """
        try:
            m = models.Payment(tx_id=tx["txn_id"])
            m.save()
            transaction = types.Transaction(
                tx_id=tx["txn_id"],
                person_id=tx["person_id"],
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
        """Get all updates from QIWI."""
        response = get(self.generate_link(), headers=self.headers)
        response.raise_for_status()
        r = response.json()
        for tx in r["data"]:
            self.tx(tx)
        if self.callback is not None:
            for tx in self.unprocessed:
                self.callback(tx)
            self.unprocessed = []

    def start(self) -> None:
        """Blocking method."""
        while True:
            self._loop()
            sleep(self.update_interval)

    def start_thread(self) -> None:
        """Non-blocking method. Launches self.start() in separate thread."""
        if self.thread:
            log.warning("Thread already initialized.")
            return None
        self.thread = Thread(target=self.start)
        self.thread.start()
