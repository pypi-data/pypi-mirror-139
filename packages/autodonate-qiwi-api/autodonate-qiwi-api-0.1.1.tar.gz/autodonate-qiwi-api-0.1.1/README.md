# Qiwi API

Qiwi API для Autodonate плагинов.

# Использование:
```python
import autodonate_qiwi_api


def payment_received(tx: autodonate_qiwi_api.types.Transaction):
    print(f"Payment from {tx.account} with amount {tx.total} received!")


autodonate_qiwi_api.initialize(
    token="abracadabra",
    phone=7900000000,
    callback=payment_received,
)
```

Так же модуль объявляет `QIWI_API_INSTALLED` глобальную переменную 
в templates, так что Вы можете с лёгкостью проверять загруженность 
модуля.

```html
{% if QIWI_API_INSTALLED %}
    <h1>Приём доната в Qiwi</h1>
    <button>Оплатить</button>
{% endif %}
```
