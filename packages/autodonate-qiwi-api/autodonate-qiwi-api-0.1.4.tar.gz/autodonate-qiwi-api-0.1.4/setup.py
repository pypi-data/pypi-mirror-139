# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autodonate_qiwi_api', 'autodonate_qiwi_api.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.2,<5.0.0',
 'autodonate>=0.1.0-alpha.0,<0.2.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'autodonate-qiwi-api',
    'version': '0.1.4',
    'description': 'QIWI API for Autodonate',
    'long_description': '# Qiwi API\n\nQiwi API для Autodonate плагинов.\n\n# Использование:\n```python\nimport autodonate_qiwi_api\n\n\ndef payment_received(tx: autodonate_qiwi_api.types.Transaction):\n    print(f"Payment from {tx.account} with amount {tx.total} received!")\n\n\nautodonate_qiwi_api.initialize(\n    token="abracadabra",\n    phone=7900000000,\n    callback=payment_received,\n)\n```\n\nТак же модуль объявляет `QIWI_API_INSTALLED` глобальную переменную \nв templates, так что Вы можете с лёгкостью проверять загруженность \nмодуля.\n\n```html\n{% if QIWI_API_INSTALLED %}\n    <h1>Приём доната в Qiwi</h1>\n    <button>Оплатить</button>\n{% endif %}\n```\n',
    'author': 'firesquare',
    'author_email': 'team@firesquare.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fire-squad/autodonate-qiwi-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
