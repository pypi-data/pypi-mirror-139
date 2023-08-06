# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phpipam_exporter', 'phpipam_exporter.libs', 'tests']

package_data = \
{'': ['*'], 'phpipam_exporter': ['templates/*'], 'tests': ['results/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'certifi>=2020.12.5,<2021.0.0',
 'click',
 'requests>=2.25.1,<3.0.0',
 'urllib3>=1.26.0,<2.0.0']

entry_points = \
{'console_scripts': ['phpipam_export = phpipam_exporter.cli:main']}

setup_kwargs = {
    'name': 'phpipam-exporter',
    'version': '0.5.0',
    'description': 'Top-level package for phpipam-exporter.',
    'long_description': '.. image:: https://badge.fury.io/py/phpipam-exporter.svg\n    :target: https://badge.fury.io/py/phpipam-exporter\n\n================\nphpipam-exporter\n================\n\nThe generator DHCP, DNS or hosts records from `phpipam <https://phpipam.net/>`_.\n\n\nUsage\n============\n\nAll parameters can be defined as environment variables.\n\n.. list-table:: **Program parameters**\n    :header-rows: 1\n\n    * - Parameter\n      - ENV variable\n      - Required\n      - Description\n    * - ``--subnet / -s``\n      - ``PHPIPAM_SUBNETS``\n      - Yes\n      - Filter output for specific PHPIPAM subnet. Can be used more times (in ``PHPIPAM_SUBNETS``, subnets are separated by coma).\n    * - ``--host``\n      - ``PHPIPAM_HOST``\n      - Yes\n      - phpipam API entrypoint format ``https://<fqdn>/api/<api_id>/`` (e.g. ``https://phpipam.example.com/api/exporter/``)\n    * - ``--token``\n      - ``PHPIPAM_TOKEN``\n      - Yes\n      - phpipam API token.\n    * - ``--format / -f``\n      - ``PHPIPAM_FORMAT``\n      - No (default: ``json``)\n      - Output format. (``dhcpd``, ``dnsmasq``, ``hosts``)\n    * - ``--output / -o``\n      - ``PHPIPAM_OUTPUT``\n      - No (default: ``stdout``)\n      - Output file.\n    * - ``--on-change-action``\n      - ``PHPIPAM_ON_CHANGE_ACTION``\n      - No\n      - Bash command. This command is fired only when the output file is changed. This parameter has to be defined only together with ``--output``. (e.g. ``systemctl reload named``)\n    * - ``--custom-template``\n      - ``PHPIPAM_CUSTOM_TEMPLATE``\n      - No\n      - Path to custom `Jinja <https://jinja2docs.readthedocs.io/en/stable/>`_ template file.\n\n\n\nGenerate API token\n======================\n\nEnable API plugin:  ``Administration > phpIPAM settings > API = On``\n\nCreate token: ``Administration > API > Create API key``\n\n.. list-table:: **Token parameters**\n    :header-rows: 0\n\n    * - ``App ID``\n      - ``exporter``\n    * - ``App permissions``\n      - ``Read``\n    * - ``App security``\n      - ``SSL with App code token``\n\nCopy ``App code`` and use it as ``PHPIPAM_TOKEN``.\n``App ID`` has to be used as part of ``PHPIPAM_HOST``.\n\n.. image:: img/token.png\n\n\n\nHosts file\n============\n.. code-block:: bash\n\n    export PHPIPAM_TOKEN=\'12345678945678912345678a1235\'\n    export PHPIPAM_HOST=\'https://phpipam.example.com/api/exporter/\'\n\n    cat /etc/hosts.static\n      127.0.0.1   localhost localhost.localdomain\n      ::1         localhost localhost.localdomain\n\n\n    phpipam_export -s 192.168.1.0/24 -f dhcpd -o /etc/hosts.dynamic --on-change-action "cat /etc/hosts.static /etc/hosts.dynamic >> /etc/hosts"\n\n\n\nDHCPd\n============\n.. code-block:: bash\n\n    export PHPIPAM_TOKEN=\'12345678945678912345678a1235\'\n    export PHPIPAM_HOST=\'https://phpipam.example.com/api/exporter/\'\n\n    phpipam_export -s 192.168.1.0/24 -f dhcpd -o /etc/dhcp/subnet.conf --on-change-action "systemctl reload dhcpd"\n\n\n**/etc/dhcp/dhcpd.conf**\n\n.. code-block::\n\n    authoritative;\n    ddns-update-style none;\n    default-lease-time 86400;\n    max-lease-time 172800;\n    shared-network "lan" {\n        subnet 192.168.1.0 netmask 255.255.255.0 {\n            option subnet-mask 255.255.255.0;\n            option domain-name-servers 192.168.1.1, 192.168.1.2;\n            option broadcast-address 192.168.1.255;\n            option routers 192.168.1.1;\n            pool {\n                range 192.168.1.254 192.168.1.254;\n                deny unknown-clients;\n                include "/etc/dhcp/subnet.conf";\n            }\n        }\n\n\n\ndnsmasq\n============\n.. code-block:: bash\n\n    export PHPIPAM_TOKEN=\'12345678945678912345678a1235\'\n    export PHPIPAM_HOST=\'https://phpipam.example.com/api/exporter/\'\n\n    phpipam_export -s 192.168.1.0/24 -f dnsmasq -o /etc/dnsmasq.d/subnet.conf --on-change-action "systemctl reload dnsmasq"\n\n\n\njson format\n============\n.. code-block:: bash\n\n    export PHPIPAM_TOKEN=\'12345678945678912345678a1235\'\n    export PHPIPAM_HOST=\'https://phpipam.example.com/api/exporter/\'\n\n    phpipam_export -s 192.168.1.0/24 -f json\n\n\n\nCustom template\n=======================\nWe can create a custom `Jinja <https://jinja2docs.readthedocs.io/en/stable/>`_ template file and use it for formating output data. The addresses are stored in the ``addresses`` template variable. Attributes of each device are described here `3.4 Addresses controller <https://phpipam.net/api-documentation/>`_ or we can use ``json`` format to get all attributes.\n\n\n.. code-block:: bash\n\n    export PHPIPAM_TOKEN=\'12345678945678912345678a1235\'\n    export PHPIPAM_HOST=\'https://phpipam.example.com/api/exporter/\'\n\n    phpipam_export -s 192.168.1.0/24 --custom-template ansible_inventory.j2  -o /ansible-project/inventory.yml\n',
    'author': 'Martin Korbel',
    'author_email': 'git@blackserver.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BlackSmith/phpipam_exporter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
