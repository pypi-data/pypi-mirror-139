# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ydotool']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyydotool',
    'version': '1.0.0',
    'description': 'Python bindings to ydotool',
    'long_description': '# PyYdotool\n\nPython bindings for [`ydotool`](https://github.com/ReimuNotMoe/ydotool) >= 1.0.1\n\nThis project was inspired by [pyxdotool](https://github.com/cphyc/pyxdotool)\n\nAll `ydotool` commands are chainable.\n\n# Example\n```python\nfrom ydotool import YdoTool\nydo = YdoTool().key("29:1", "56:1", "59:1", "59:0", "56:0", "29:0") # press and release \'LeftCtrl+LeftAlt+F1\'\nydo.sleep(0.5).type("echo \'foo bar\'")\n# execution is done here\nydo.exec()\n```\n\n# Requirements\n- Ydotool >= 1.0.1\n\n- Access to `/dev/uinput` device is required. It can be set by adding `udev` rules.<br>\nExample tested for Fedora:\n    #### **`/etc/udev/rules.d/60-uinput.rules`**\n    ```shell\n    KERNEL=="uinput", SUBSYSTEM=="misc", TAG+="uaccess", OPTIONS+="static_node=uinput"\n    ```\n\n    This rules will allow regular user logged in to the machine to access `uinput` device. ',
    'author': 'Jerzy Drozdz',
    'author_email': 'jerzy.drozdz@jdsieci.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/jdsieci/pyydotool',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
